"""Faithful ticket 03 source selections; no resize, sharpening, or UI generation."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'assets/images/harmony/templates.png'
source = Image.open(ROOT / SOURCE).convert('RGB')
records = []
selections = [
    ('template-compositions-configuration-wide.png', (1826, 892), [([80, 108, 1906, 1000], [0, 0])],
     'Retain form, list, loading, selected success composition and adjacent configuration panel in their original spatial relationship; remove only peripheral canvas/chrome.'),
    ('template-card-success-configuration-mobile.png', (296, 1012), [
        ([96, 508, 386, 744], [3, 0]),
        ([812, 540, 1108, 772], [0, 260]),
        ([1634, 108, 1906, 604], [12, 516])],
     'Stack three identified excerpts: List/CardView, selected success layout with selection boundary, and Success configuration through Row06. Preserve SwitchProfile, breadcrumb level, alert and content-row controls; dark gutters distinguish the excerpts. This is an editorial selection, not the original Figma layout.')]
for name, dimensions, fragments, purpose in selections:
    output = Image.new('RGB', dimensions, '#1e1e1e')
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
        'background': '#1e1e1e', 'fragments': [{'crop': c, 'pasteAt': a} for c, a in fragments],
        'purposeAndRetainedContext': purpose})
(ROOT / '.scratch/harmony/template-image-manifest.json').write_text(json.dumps({
    'coordinateSystem': '(x0,y0,x1,y1), right and bottom exclusive; pasteAt=(x,y)',
    'derivatives': records}, indent=2) + '\n', encoding='utf-8')
