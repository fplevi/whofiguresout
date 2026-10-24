"""Reproduce ticket 01's transparent presentation crop and asset record."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'assets/images/convenios/convenios-provider-network.png'
OUTPUT = 'assets/images/convenios/convenios-provider-network-crop.webp'
# Pillow coordinates: left/top inclusive, right/bottom exclusive. Retains the
# complete phone, header, map pins, list-view control and bottom navigation.
BOUNDS = (330, 48, 760, 734)

original = Image.open(ROOT / SOURCE).convert('RGBA')
crop = original.crop(BOUNDS)
crop.save(ROOT / OUTPUT, 'WEBP', lossless=True, exact=True)
decoded = Image.open(ROOT / OUTPUT).convert('RGBA')
assert decoded.tobytes() == crop.tobytes()
assert decoded.getchannel('A').getextrema() == (0, 255)
record = {
    'ticket': '01-rede-credenciada',
    'coordinate_system': 'pixels; left/top inclusive, right/bottom exclusive',
    'assets': [{
        'source': SOURCE,
        'source_dimensions': list(original.size),
        'source_sha256': hashlib.sha256((ROOT / SOURCE).read_bytes()).hexdigest(),
        'output': OUTPUT,
        'crop_bounds': list(BOUNDS),
        'dimensions': list(decoded.size),
        'format': 'WebP, lossless RGBA, exact transparent pixels',
        'purpose': 'Remove empty presentation margins and faint extended shadow so the complete provider-network phone is legible; retain map results, Voltar para lista, new-search control and bottom navigation.',
        'original_unchanged': True,
        'unchanged': False,
        'decoded_pixels_equal_source_crop': True,
    }, {
        'source': 'assets/images/convenios/convenios-card.webp',
        'output': 'assets/images/convenios/convenios-card.webp',
        'crop_bounds': [0, 0, 758, 1031],
        'dimensions': [758, 1031],
        'format': 'WebP RGBA (existing)',
        'purpose': 'Preserved composite card evidence for view, copy and share; only unsupported biometric-login wording removed.',
        'unchanged': True,
    }, {
        'source': 'assets/images/convenios/convenios-home.webp',
        'output': 'assets/images/convenios/convenios-home.webp',
        'crop_bounds': [0, 0, 818, 1025],
        'dimensions': [818, 1025],
        'format': 'WebP RGBA (existing)',
        'purpose': 'Preserved home in the hero; home card also unchanged.',
        'unchanged': True,
    }],
}
dest = ROOT / '.scratch/convenios/assets/01-network.json'
dest.parent.mkdir(exist_ok=True)
dest.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf8')
print(json.dumps(record['assets'][0], indent=2))
