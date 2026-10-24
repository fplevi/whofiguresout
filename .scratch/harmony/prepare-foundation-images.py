"""Faithful editorial selections; never resize or modify source pixels.

Mobile plates juxtapose labelled source fragments, with explicit gutters.
They are selections, not reconstructions of the original application layout.
"""
from pathlib import Path
import hashlib
import json
from PIL import Image

DEST = Path('assets/images/harmony/editorial')
DEST.mkdir(parents=True, exist_ok=True)
records = []


def plate(source, name, size, fragments, background):
    original = Image.open(Path('assets/images/harmony') / source).convert('RGB')
    result = Image.new('RGB', size, background)
    for rectangle, position in fragments:
        result.paste(original.crop(rectangle), position)
    result.save(DEST / name, optimize=True)
    records.append({
        'source': f'assets/images/harmony/{source}', 'sourceDimensions': original.size,
        'sourceSha256': hashlib.sha256((Path('assets/images/harmony') / source).read_bytes()).hexdigest(),
        'derivative': str(DEST / name).replace('\\', '/'), 'dimensions': size,
        'format': 'PNG, lossless RGB, optimize=True; no resizing or text redrawing',
        'fragments': [{'crop': rect, 'pasteAt': pos} for rect, pos in fragments],
        'background': background, 'bytes': (DEST / name).stat().st_size,
    })


plate('color=primitives.png', 'primitive-primary-secondary-scales.png', (1360, 548),
      [((130, 510, 1490, 1058), (0, 0))], '#0d0f13')
plate('color=primitives.png', 'primitive-selected-light-steps-mobile.png', (296, 480), [
    ((140, 520, 265, 552), (16, 16)),
    ((140, 570, 404, 732), (16, 60)),
    ((140, 825, 285, 862), (16, 254)),
    ((140, 876, 404, 1038), (16, 302)),
], '#0d0f13')

plate('semantic-tokerns.png', 'semantic-surface-border-roles.png', (1440, 554),
      [((135, 454, 1575, 1008), (0, 0))], '#0d0f13')
plate('semantic-tokerns.png', 'semantic-default-soft-roles-mobile.png', (344, 508), [
    ((148, 464, 268, 497), (16, 16)),
    ((148, 510, 460, 695), (16, 62)),
    ((148, 768, 260, 798), (16, 275)),
    ((148, 810, 460, 995), (16, 317)),
], '#0d0f13')

# Repeat the same source Name column beside each intact mode column. Gutters
# explicitly separate the three selected views; values are never rewritten.
fragments = []
for row, left in enumerate([815, 1180, 1548]):
    top = 16 + row * 504
    fragments += [((450, 60, 680, 540), (16, top)),
                  ((left, 60, left + 205, 540), (246, top))]
plate('variables.png', 'responsive-mode-selections-mobile.png', (467, 1520),
      fragments, '#151515')

Path('.scratch/harmony/image-manifest.json').write_text(
    json.dumps({'coordinateSystem': '(x0,y0,x1,y1), right and bottom exclusive; pasteAt=(x,y)',
                'derivatives': records}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
