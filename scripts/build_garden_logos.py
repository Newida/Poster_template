#!/usr/bin/env python3
"""Convert existing logo artwork to cropped PDFs without alpha soft masks.

The Lamarr mark retains its original SVG paths. For raster partner logos, the
original alpha silhouette becomes a PDF clipping path around the existing
light-theme RGB artwork. No paper-colored rectangle or PNG transparency is
painted. This makes the artwork reusable over the actual poster background.
"""

from pathlib import Path
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zlib

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "themes/japanese-garden/assets/logos"
SOURCES = {
    "tu-dortmund": "tu-dortmund-logo-claim-de",
    "fraunhofer-iais": "fraunhofer-iais",
    "fraunhofer-iml": "fraunhofer-iml",
    "uni-bonn": "uni_bonn-footer",
    "nrw": "NRWLogo-footer",
    "bftr": "BFTR-footer",
}
# The previous light-theme PNGs recolored neutral pixels throughout each
# logo. Keep original colors inside emblems (including white details) while
# retaining the legible dark wordmarks outside them. Coordinates are in the
# untrimmed original images, with the origin at their top left.
ORIGINAL_EMBLEMS = {
    "fraunhofer-iml": (0, 0, 38, 52),
    "uni-bonn": (1197, 0, 1967, 790),
    "nrw": (650, 0, 827, 185),
    "bftr": (0, 0, 205, 367),
}


def stream(dictionary, data):
    compressed = zlib.compress(data)
    return (f"<< {dictionary} /Filter /FlateDecode /Length {len(compressed)} >>\n"
            "stream\n").encode() + compressed + b"\nendstream"


def write_pdf(path, objects):
    document = bytearray(b"%PDF-1.3\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(document))
        document.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(document)
    document.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        document.extend(f"{offset:010d} 00000 n \n".encode())
    document.extend((f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
                     f"startxref\n{xref}\n%%EOF\n").encode())
    path.write_bytes(document)


def raster_logo(name, original):
    with Image.open(ROOT / "logos" / f"{original}.png") as source:
        alpha = source.convert("RGBA").getchannel("A")
        # Use a hard geometric silhouette, avoiding printer-sensitive /SMask.
        mask = alpha.point(lambda value: 255 if value >= 128 else 0)
        bbox = mask.getbbox()
        if bbox is None:
            raise ValueError(f"Empty logo: {original}")
        width, height = mask.size
        rows = mask.tobytes()
        original_rgb = source.convert("RGB").tobytes()
    with Image.open(ROOT / "logos/print-safe-light" / f"{name}.png") as source:
        if source.size != (width, height):
            raise ValueError(f"RGB/alpha size mismatch: {name}")
        rgb = source.convert("RGB").tobytes()

    left, top, right, bottom = bbox
    commands = ["q", f"1 0 0 1 {-left} {bottom-height} cm"]
    for y in range(top, bottom):
        x = left
        while x < right:
            if not rows[y * width + x]:
                x += 1
                continue
            start = x
            while x < right and rows[y * width + x]:
                x += 1
            commands.append(f"{start} {height-y-1} {x-start} 1 re")
    commands.extend(["W n", "q", f"{width} 0 0 {height} 0 0 cm", "/Logo Do", "Q"])
    if name in ORIGINAL_EMBLEMS:
        x0, y0, x1, y1 = ORIGINAL_EMBLEMS[name]
        commands.extend([f"{x0} {height-y1} {x1-x0} {y1-y0} re W n",
                         f"{width} 0 0 {height} 0 0 cm", "/Original Do"])
    commands.append("Q")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {right-left} {bottom-top}] "
         "/Resources << /XObject << /Logo 5 0 R /Original 6 0 R >> >> "
         "/Contents 4 0 R >>").encode(),
        stream("", "\n".join(commands).encode()),
        stream(f"/Type /XObject /Subtype /Image /Width {width} /Height {height} "
               "/ColorSpace /DeviceRGB /BitsPerComponent 8", rgb),
        stream(f"/Type /XObject /Subtype /Image /Width {width} /Height {height} "
               "/ColorSpace /DeviceRGB /BitsPerComponent 8", original_rgb),
    ]
    write_pdf(OUTPUT / f"{name}.pdf", objects)


def lamarr_logo():
    tree = ET.parse(ROOT / "logos/lamarr-logo-template.svg")
    root = tree.getroot()
    # Crop the original vector artwork to its visible bounds (including a
    # sub-unit margin); the source's large empty canvas is not a logo border.
    root.set("viewBox", "72 77 582 250")
    root.set("width", "582")
    root.set("height", "250")
    root.set("fill", "#0F233D")
    with tempfile.TemporaryDirectory(prefix="garden-logo-") as directory:
        svg = Path(directory) / "lamarr.svg"
        tree.write(svg, encoding="utf-8", xml_declaration=True)
        subprocess.run(["mutool", "convert", "-o", str(OUTPUT / "lamarr.pdf"),
                        str(svg)], check=True)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    lamarr_logo()
    for name, original in SOURCES.items():
        raster_logo(name, original)
    print(f"Wrote seven cropped, soft-mask-free logo PDFs to {OUTPUT}")


if __name__ == "__main__":
    main()
