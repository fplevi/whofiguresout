"""Converte as imagens de conteúdo dos cases para AVIF + WebP responsivos (padrão da foto do About).

Para cada imagem medida em ../evidence/image-inventory.json (exceto as que já são AVIF e pôsteres):
- gera <slug>-<w>.avif (q62) e <slug>-<w>.webp (q82) ao lado do original, w = 800 e até 1600 px
  (sem ampliar; imagens com até 800 px ganham um único tamanho);
- <img> solta vira <picture class="img-sources"> (display: contents, layout inalterado) com
  <source type="image/avif"> + <img src/srcset em WebP>, mantendo width/height/alt/loading/class;
- <picture> com direção de arte (Harmony) ganha <source> AVIF/WebP por mídia.
`sizes` vem das larguras exibidas medidas (desktop 1350 px, mobile 412 px).
Os originais ficam no repositório, sem referência. Idempotente: só toca src que ainda aponta
para o original. Preserva CRLF/LF de cada HTML. Uso: python -I convert-images.py <raiz-do-site>
"""
import json, re, sys, unicodedata
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

ROOT = Path(sys.argv[1])
INV = json.loads((Path(__file__).parent / '../evidence/image-inventory.json').read_text(encoding='utf8'))
PAGES = ['billing', 'convenios', 'burger-king', 'enrollment', 'harmony']
AVIF_Q, WEBP_Q = 62, 82
CR, LF = chr(13), chr(10)


def slug(stem):
    s = unicodedata.normalize('NFKD', stem).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def encode(src_rel):
    """Gera variantes; devolve [(w, avif_rel, webp_rel)] relativos à raiz do site."""
    src = ROOT / src_rel.lstrip('/')
    im = Image.open(src)
    im.load()
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    if alpha and im.getchannel('A').getextrema()[0] == 255:
        im = im.convert('RGB')
    widths = sorted({min(im.width, 800), min(im.width, 1600)})
    out = []
    for w in widths:
        x = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        base = src.with_name(f'{slug(src.stem)}-{w}')
        x.save(base.with_name(base.name + '.avif'), 'AVIF', quality=AVIF_Q)
        x.save(base.with_name(base.name + '.webp'), 'WEBP', quality=WEBP_Q, method=6)
        rel = '/' + base.relative_to(ROOT).as_posix()
        out.append((w, rel + '.avif', rel + '.webp'))
    return out


def sizes_for(item, kind):
    d = item['need'].get('desktop')
    m = item['need'].get('mobile')
    mvw = min(round(m / 1.75 / 412 * 100), 100) if m else 100
    if kind == 'desktop-only':
        return f'{d}px'
    if kind == 'mobile-only':
        return f'{mvw}vw'
    return f'(max-width: 768px) {mvw}vw, {d or 800}px'


def srcset(variants, idx, prefix):
    return ', '.join(f'{prefix}{v[idx].lstrip("/")} {v[0]}w' for v in variants)


inv = {i['src']: i for i in INV if i.get('ext') != 'avif' and not i['src'].endswith('-poster.webp')}
variants = {}
report = []


def get_variants(src_rel):
    if src_rel not in variants:
        variants[src_rel] = encode(src_rel)
        report.append((src_rel, variants[src_rel]))
    return variants[src_rel]


def rel_of(url):
    return '/' + unquote(url.replace('../', '', 1))


for page in PAGES:
    path = ROOT / 'case-studies' / f'{page}.html'
    html = path.read_bytes().decode('utf8')
    eol = CR + LF if CR + LF in html else LF
    prefix = '../'

    # 1) <source media=... srcset="X"> dentro de <picture> (direção de arte, desktop)
    def repl_source(m):
        tag, url = m.group(0), m.group(2)
        src_rel = rel_of(url)
        if src_rel not in inv:
            return tag
        v = get_variants(src_rel)
        s = sizes_for(inv[src_rel], 'desktop-only')
        indent = re.match(r'[ \t]*', tag).group(0)
        rest = re.sub(r'\s*srcset="[^"]*"', '', tag.strip())
        rest = rest[len('<source'):].rstrip('/>').strip()
        return (f'{indent}<source type="image/avif" {rest} srcset="{srcset(v, 1, prefix)}" sizes="{s}" />{eol}'
                f'{indent}<source type="image/webp" {rest} srcset="{srcset(v, 2, prefix)}" sizes="{s}" />')

    html = re.sub(r'[ \t]*<source (media="[^"]*") srcset="(\.\./assets/images/[^"]+\.(?:png|jpe?g|webp))"[^>]*/>',
                  repl_source, html)

    # 2) <img src="X">: dentro de <picture> ganha source AVIF + srcset; solta ganha wrapper
    out, pos = [], 0
    for m in re.finditer(r'(?m)^([ \t]*)(<img [^>]*?src="(\.\./assets/images/[^"]+\.(?:png|jpe?g|webp))"[^>]*?/?>)', html):
        indent, tag, url = m.group(1), m.group(2), m.group(3)
        src_rel = rel_of(url)
        if src_rel not in inv:
            continue
        before = html[:m.start()]
        in_picture = before.rfind('<picture') > before.rfind('</picture>')
        v = get_variants(src_rel)
        item = inv[src_rel]
        kind = 'mobile-only' if in_picture and item['need'].get('desktop') is None else 'both'
        s = sizes_for(item, kind)
        small = v[0][2].lstrip('/')
        new_img = tag.replace(f'src="{url}"', f'src="{prefix}{small}" srcset="{srcset(v, 2, prefix)}" sizes="{s}"', 1)
        avif = f'<source type="image/avif" srcset="{srcset(v, 1, prefix)}" sizes="{s}" />'
        if in_picture:
            block = f'{indent}{avif}{eol}{indent}{new_img}'
        else:
            block = (f'{indent}<picture class="img-sources">{eol}{indent}  {avif}{eol}'
                     f'{indent}  {new_img}{eol}{indent}</picture>')
        out.append(html[pos:m.start()])
        out.append(block)
        pos = m.end()
    out.append(html[pos:])
    path.write_bytes(''.join(out).encode('utf8'))

total_o = total_n = 0
for src_rel, v in report:
    o = (ROOT / src_rel.lstrip('/')).stat().st_size
    big = (ROOT / v[-1][1].lstrip('/')).stat().st_size
    total_o += o
    total_n += big
    print(f'{o // 1024:5}K -> avif {"/".join(str(x[0]) for x in v)}w maior {big // 1024}K  {src_rel}')
print(f'{len(report)} imagens: {total_o // 1024}K originais -> {total_n // 1024}K (maior AVIF de cada)')
