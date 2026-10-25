"""Ajusta srcset/sizes gerados por convert-images.py para não alterar o tamanho intrínseco.

Com descritores `w`, o tamanho intrínseco da imagem passa a ser o valor de `sizes`; isso muda o
layout de imagens com `width: auto` (Harmony). Então:
- variante única ("x.webp 296w"): remove o descritor e o `sizes` (intrínseco = tamanho real);
  numa <img> cujo srcset é só o próprio src, remove srcset e sizes;
- <source media="(min-width: 1025px)"> com várias larguras: `sizes` = largura natural do original
  (o max-width: 100% limita ao contêiner, como antes).
Preserva CRLF/LF. Uso: python fix-srcset-intrinsic.py <raiz-do-site>
"""
import re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(sys.argv[1])
PAGES = ['billing', 'convenios', 'burger-king', 'enrollment', 'harmony']
ORIG_EXT = ('.png', '.jpg', '.jpeg', '.webp')


def original_width(variant_url):
    """../assets/images/x/slug-800.avif -> largura do original (procura arquivo de mesmo slug)."""
    p = ROOT / variant_url.replace('../', '', 1)
    stem = re.sub(r'-\d+$', '', p.stem)
    for f in p.parent.iterdir():
        if f.suffix.lower() in ORIG_EXT and re.sub(r'[^a-z0-9]+', '-', f.stem.lower()).strip('-') == stem:
            return Image.open(f).width
    raise FileNotFoundError(variant_url)


def fix_tag(tag):
    m = re.search(r'srcset="([^"]+)"', tag)
    if not m:
        return tag
    entries = [e.strip() for e in m.group(1).split(',')]
    if len(entries) == 1:
        url = entries[0].rsplit(' ', 1)[0]
        src = re.search(r'\ssrc="([^"]+)"', tag)
        if tag.startswith('<img') and src and src.group(1) == url:
            tag = re.sub(r'\s+srcset="[^"]*"', '', tag)
        else:
            tag = tag.replace(m.group(0), f'srcset="{url}"')
        return re.sub(r'\s+sizes="[^"]*"', '', tag)
    if tag.startswith('<source') and 'media="(min-width: 1025px)"' in tag:
        w = original_width(entries[0].rsplit(' ', 1)[0])
        tag = re.sub(r'sizes="[^"]*"', f'sizes="{w}px"', tag)
    return tag


for page in PAGES:
    path = ROOT / 'case-studies' / f'{page}.html'
    html = path.read_bytes().decode('utf8')
    new = re.sub(r'<(?:img|source) [^>]*srcset="[^"]*"[^>]*>', lambda m: fix_tag(m.group(0)), html)
    if new != html:
        path.write_bytes(new.encode('utf8'))
        print('ajustado', page)
