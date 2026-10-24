"""Ticket 04: unchanged Storybook source fragments; no resize or redrawing."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'assets/images/harmony/storybook-2.png'
source = Image.open(ROOT / SOURCE).convert('RGB')
records = []
selections = [
    ('storybook-button-properties-wide.png', (1920, 980), [
        ([0, 220, 1920, 1200], [0, 0])],
     'Button preview above the original property table; retains Controls, Name/Control headings, onPress, children, variant, and the visible sm/md size choices. Removes only upper toolbar and empty preview space.'),
    ('storybook-button-selected-properties-mobile.png', (350, 640), [
        ([1230, 250, 1460, 400], [60, 0]),
        ([24, 590, 156, 642], [16, 174]),
        ([32, 676, 210, 738], [0, 230]),
        ([700, 676, 860, 738], [190, 230]),
        ([32, 846, 210, 938], [0, 292]),
        ([700, 846, 860, 938], [190, 292]),
        ([32, 960, 210, 1052], [0, 384]),
        ([700, 960, 860, 1052], [190, 384]),
        ([32, 1080, 210, 1196], [0, 476]),
        ([700, 1080, 860, 1196], [190, 476])],
     'Editorial excerpts: Button preview, Controls label, then paired original Name/Control columns for children=Button, variant=solid, and visible size sm/md. Columns remain paired by source y-coordinate; gutters separate selections. Omits onPress, count, other tabs, and blank canvas. Does not reconstruct a Storybook screen or infer additional size options.')]
for name, dimensions, fragments, purpose in selections:
    output = Image.new('RGB', dimensions, '#222324')
    for crop, at in fragments:
        output.paste(source.crop(crop), tuple(at))
    destination = 'assets/images/harmony/editorial/' + name
    output.save(ROOT / destination, optimize=True)
    data = (ROOT / destination).read_bytes()
    records.append({'source': SOURCE, 'sourceDimensions': list(source.size),
        'sourceSha256': hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest(),
        'derivative': destination, 'dimensions': list(dimensions),
        'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
        'format': 'PNG, lossless RGB, optimize=True; no resize or redrawing',
        'background': '#222324', 'fragments': [{'crop': c, 'pasteAt': a} for c, a in fragments],
        'purposeAndRetainedContext': purpose})
(ROOT / '.scratch/harmony/storybook-image-manifest.json').write_text(json.dumps({
    'coordinateSystem': '(x0,y0,x1,y1), right and bottom exclusive; pasteAt=(x,y)',
    'derivatives': records}, indent=2) + '\n', encoding='utf-8')
