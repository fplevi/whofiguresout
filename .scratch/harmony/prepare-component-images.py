"""Ticket 02: copy labelled source selections without resizing source pixels.

Adds only this slice's records to the shared manifest; retains other records.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

DEST = Path('assets/images/harmony/editorial')
MANIFEST = Path('.scratch/harmony/image-manifest.json')
records = []


def plate(source, name, size, fragments, purpose):
    source_path = Path('assets/images/harmony') / source
    original = Image.open(source_path).convert('RGB')
    result = Image.new('RGB', size, '#1e1e1e')
    for rectangle, position in fragments:
        result.paste(original.crop(rectangle), position)
    path = DEST / name
    result.save(path, optimize=True)
    records.append({
        'ticket': '02', 'source': source_path.as_posix(),
        'sourceDimensions': list(original.size),
        'sourceSha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'derivative': path.as_posix(), 'dimensions': list(size),
        'derivativeSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'format': 'PNG, lossless RGB, optimize=True; no resizing or text redrawing',
        'fragments': [{'crop': rect, 'pasteAt': pos} for rect, pos in fragments],
        'background': '#1e1e1e', 'bytes': path.stat().st_size,
        'purpose': purpose,
    })


plate('buttons.png', 'button-standard-solid-outline-normal-small.png', (400, 687), [
    ((160, 32, 560, 380), (0, 0)),
    ((160, 655, 560, 970), (0, 372)),
], 'Standard solid/outline selections, NormalSize above SmallSize; source names, '
   'text/dropdown/icon-only examples and state treatments retained. The gutter '
   'separates selections. Original overlapping Figma names remain unaltered.')

plate('components.png', 'portal-intranet-profile-navigation.png', (300, 670), [
    ((60, 402, 360, 725), (0, 0)),
    ((1100, 402, 1400, 725), (0, 347)),
], 'PortalProfileButton and IntranetProfileButton selections in that order; '
   'complete context names, account trigger, menu entries and exit action retained. '
   'The gutter separates source selections, not an application layout. Excludes '
   'the unfinished responsive panels cut off at the source bottom.')

manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
replaced = {r['derivative'] for r in records}
manifest['derivatives'] = [r for r in manifest['derivatives'] if r['derivative'] not in replaced] + records
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
