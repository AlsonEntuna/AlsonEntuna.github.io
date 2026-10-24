"""Image helper for the site.

Usage (needs Pillow: `pip install pillow`):
  python tools/images.py convert path/to/photo.jpg [...]
      Writes assets/img/<name>.webp (max 1600px wide) and
      assets/img/<name>-600.webp (600px wide, for cards and thumbnails).
  python tools/images.py annotate
      Adds width/height (and a srcset when a -600 version exists) to every
      <img> in the site's .html files that points at assets/img/.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
FULL_W, SMALL_W, QUALITY = 1600, 600, 80


def clean_name(path: Path) -> str:
    """'ac-valhalla-1440x900.jpg' -> 'ac-valhalla' (drops Mobirise size suffixes)."""
    stem = path.stem.lower()
    stem = re.sub(r"\.(jpe?g|png)", "", stem)
    while True:
        new = re.sub(r"-\d+x\d+$", "", stem)
        if new == stem:
            return stem
        stem = new


def save(img, width, dest):
    from PIL import Image
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    img.save(dest, "WEBP", quality=QUALITY, method=6)


def convert(paths):
    from PIL import Image, ImageOps
    OUT.mkdir(parents=True, exist_ok=True)
    for p in map(Path, paths):
        name = clean_name(p)
        with Image.open(p) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGBA" if img.mode in ("RGBA", "LA", "P") else "RGB")
            save(img, FULL_W, OUT / f"{name}.webp")
            if img.width > SMALL_W * 1.3:
                save(img, SMALL_W, OUT / f"{name}-600.webp")
        print(f"{p.name} -> {name}.webp")


IMG_TAG = re.compile(r"<img\b[^>]*>")


def annotate():
    from PIL import Image
    for page in ROOT.glob("*.html"):
        text = page.read_text(encoding="utf-8")

        def fix(m):
            tag = m.group(0)
            src = re.search(r'src="(assets/img/[^"]+\.webp)"', tag)
            if not src:
                return tag
            file = ROOT / src.group(1)
            if not file.exists():
                print(f"  missing: {src.group(1)} in {page.name}")
                return tag
            if "width=" not in tag:
                with Image.open(file) as im:
                    w, h = im.size
                tag = tag.replace("<img", f'<img width="{w}" height="{h}"', 1)
            small = file.with_name(file.stem + "-600.webp")
            if "srcset=" not in tag and small.exists() and not file.stem.endswith("-600"):
                with Image.open(file) as im:
                    w = im.width
                rel = src.group(1)
                tag = tag.replace(
                    f'src="{rel}"',
                    f'src="{rel}" srcset="{rel[:-5]}-600.webp 600w, {rel} {w}w"',
                    1,
                )
            return tag

        new = IMG_TAG.sub(fix, text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            print(f"annotated {page.name}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["help"]
    if cmd == "convert":
        convert(args)
    elif cmd == "annotate":
        annotate()
    else:
        print(__doc__)
