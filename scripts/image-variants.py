"""Generate AVIF + WebP variants of a content image and print the srcset strings to paste.

Usage: python scripts/image-variants.py <image> [<image> ...]
Requires Pillow with AVIF support (pip install pillow).

For each image, writes <slug>-<w>.avif (quality 62) and <slug>-<w>.webp (quality 82) next to it,
with w = 800 and up to 1600 px (never upscaled; images up to 800 px get a single size).
The original stays as the source file and is no longer referenced by the page.
Markup rules live in docs/agents/images.md.
"""
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image

AVIF_QUALITY, WEBP_QUALITY = 62, 82


def slug(stem):
    s = unicodedata.normalize('NFKD', stem).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def variants(src):
    im = Image.open(src)
    im.load()
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    if alpha and im.getchannel('A').getextrema()[0] == 255:
        im = im.convert('RGB')  # fully opaque: drop the unused alpha channel
    out = []
    for w in sorted({min(im.width, 800), min(im.width, 1600)}):
        x = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        base = src.with_name(f'{slug(src.stem)}-{w}')
        avif, webp = base.with_name(base.name + '.avif'), base.with_name(base.name + '.webp')
        x.save(avif, 'AVIF', quality=AVIF_QUALITY)
        x.save(webp, 'WEBP', quality=WEBP_QUALITY, method=6)
        out.append((w, avif, webp))
    return im.size, out


for arg in sys.argv[1:]:
    src = Path(arg)
    (w0, h0), out = variants(src)
    print(f'\n{src}  ({w0}x{h0}, {src.stat().st_size // 1024} KB)')
    for w, avif, webp in out:
        print(f'  {w}w  avif {avif.stat().st_size // 1024} KB  webp {webp.stat().st_size // 1024} KB')
    if len(out) == 1:
        print(f'  avif srcset: {out[0][1].name}')
        print(f'  img src:     {out[0][2].name}   (single size: no srcset/sizes on the <img>)')
    else:
        print('  avif srcset: ' + ', '.join(f'{a.name} {w}w' for w, a, _ in out))
        print('  webp srcset: ' + ', '.join(f'{p.name} {w}w' for w, _, p in out))
        print(f'  img src:     {out[0][2].name}')
