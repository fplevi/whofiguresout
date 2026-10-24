"""Ticket-specific adaptation of final_checks.py: preservation, assets, measured contrast."""
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
import re
import subprocess
import sys
from PIL import Image

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(os.environ.get('ENROLLMENT_QA_OUT', str(ROOT / '.scratch/enrollment/qa/ticket-03')))
OUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('ENROLLMENT_QA_URL', 'http://127.0.0.1:8123/case-studies/enrollment.html')
ORIGIN = '{0.scheme}://{0.netloc}'.format(urlsplit(URL))


def rgba(css):
    values = [float(v) for v in re.findall(r'[\d.]+', css)]
    return values[:3] + [values[3] if len(values) > 3 else 1]


def over(fg, bg):
    return [fg[i] * fg[3] + bg[i] * (1 - fg[3]) for i in range(3)] + [1]


def luminance(color):
    rgb = [v / 255 for v in color[:3]]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * k for v, k in zip(linear, [.2126, .7152, .0722]))


def contrast(fg, bg):
    a, b = sorted([luminance(over(fg, bg)), luminance(bg)])
    return (b + .05) / (a + .05)


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 375, 'height': 700}, reduced_motion='reduce')
    page.goto(URL, wait_until='domcontentloaded')
    page.evaluate('document.fonts.ready')
    colors = page.evaluate('''() => ({
      body: getComputedStyle(document.body).backgroundColor,
      guidance: getComputedStyle(document.querySelector('#enrollment-comparison-help')).color,
      label: getComputedStyle(document.querySelector('.cs-compare__label')).color,
      labelBackground: getComputedStyle(document.querySelector('.cs-compare__label')).backgroundColor,
      handle: getComputedStyle(document.querySelector('.cs-compare__handle'), '::after').color,
      handleBackground: getComputedStyle(document.querySelector('.cs-compare__handle'), '::before').backgroundColor
    })''')
    measurements = {
        'guidance': contrast(rgba(colors['guidance']), rgba(colors['body'])),
        'labelWorstWhiteImage': contrast(rgba(colors['label']), over(rgba(colors['labelBackground']), [255, 255, 255, 1])),
        'handleArrows': contrast(rgba(colors['handle']), rgba(colors['handleBackground'])),
    }
    orientation = page.locator('.enrollment-discovery__copy, .enrollment-journey-evidence p, .enrollment-submission-evidence p').evaluate_all('''es => es.map(e => ({
        color:getComputedStyle(e).color, text:e.textContent.trim(),
        backgrounds:(()=>{const a=[];for(let n=e;n&&n!==document.body;n=n.parentElement)a.push(getComputedStyle(n).backgroundColor);return a;})()
    }))''')
    for index, item in enumerate(orientation):
        assert all(rgba(bg)[3] == 0 for bg in item['backgrounds']), item
        measurements[f'integratedOrientation{index + 1}'] = contrast(rgba(item['color']), rgba(colors['body']))
    (OUT / 'contrast.json').write_text(json.dumps({'computedColors': colors, 'ratios': measurements,
        'method': 'WCAG relative sRGB luminance; alpha composited on computed body; label tested over worst-case white raster; handle arrows over white disc.'}, indent=2), encoding='utf-8')
    for name, value in measurements.items():
        minimum = 3 if name == 'handleArrows' else 4.5
        assert value >= minimum, (name, value, minimum)
    print('PASS measured contrast', measurements)
    destinations = []
    for selector, suffix in [('.cs-header__back', '/'), ('.nav__logo', '/'),
                             ('.nav__link:has-text("Work")', '/#work'),
                             ('.nav__link:has-text("Contact")', '/#contact'),
                             ('.nav__link:has-text("About")', '/#about'),
                             ('.cs-next__link', '/case-studies/convenios.html')]:
        page.goto(URL, wait_until='domcontentloaded')
        page.locator(selector).click()
        page.wait_for_url(ORIGIN + suffix)
        destinations.append(page.url)
    print('PASS actual navigation, back and next-project clicks')
    contrast_matrix = []
    for motion in ['no-preference', 'reduce']:
        page.emulate_media(reduced_motion=motion)
        for width in [320, 375, 768, 1440]:
            page.set_viewport_size({'width': width, 'height': 900 if width == 1440 else 700})
            page.goto(URL, wait_until='domcontentloaded')
            page.evaluate('document.fonts.ready')
            rendered = page.locator('.enrollment-comparison__guidance, .enrollment-discovery__copy, .enrollment-journey-evidence p, .enrollment-submission-evidence p').evaluate_all('''es => es.map(e => ({
                color:getComputedStyle(e).color, body:getComputedStyle(document.body).backgroundColor,
                font:getComputedStyle(e).fontSize,
                backgrounds:(()=>{const a=[];for(let n=e;n&&n!==document.body;n=n.parentElement)a.push(getComputedStyle(n).backgroundColor);return a;})()
            }))''')
            for item in rendered:
                assert all(rgba(bg)[3] == 0 for bg in item['backgrounds']), item
                item['ratio'] = contrast(rgba(item['color']), rgba(item['body']))
                assert item['ratio'] >= 4.5 and item['font'] == '16px', item
            assert len(rendered) == 10, 'Three comparison instructions plus seven evidence explanations'
            contrast_matrix.append({'width':width, 'height':900 if width == 1440 else 700, 'motion':motion, 'explanations':rendered})
    (OUT / 'contrast-matrix.json').write_text(json.dumps(contrast_matrix, indent=2), encoding='utf-8')
    print('PASS measured contrast and 16px guidance across all eight viewport/motion cases')
    browser.close()

manifest = json.loads((ROOT / '.scratch/enrollment/presentation-assets-03.json').read_text(encoding='utf-8'))
baseline_html = subprocess.check_output(['git', 'show', 'f8f9034:case-studies/enrollment.html'], cwd=ROOT).decode('utf-8')
current_html = (ROOT / 'case-studies/enrollment.html').read_text(encoding='utf-8')
assert re.search(r'<head>[\s\S]*?</head>', baseline_html).group() == re.search(r'<head>[\s\S]*?</head>', current_html).group(), 'Authored head and analytics declarations preserved'
for item in manifest['assets']:
    source = ROOT / item['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sha256']
    assert source.read_bytes() == subprocess.check_output(['git', 'show', f'f8f9034:{item["source"]}'], cwd=ROOT)
originals = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'f8f9034', 'assets/images/enrollment'], cwd=ROOT, text=True).splitlines()
for original in originals:
    assert (ROOT / original).read_bytes() == subprocess.check_output(['git', 'show', f'f8f9034:{original}'], cwd=ROOT), original
submission = json.loads((ROOT / '.scratch/enrollment/presentation-assets-05.json').read_text(encoding='utf-8'))
source = ROOT / submission['source']
assert hashlib.sha256(source.read_bytes()).hexdigest() == submission['sourceSHA256']
crop = Image.open(source).convert('RGBA').crop(tuple(submission['cropBoundsXYXY']))
derivative = Image.open(ROOT / submission['presentation']).convert('RGBA')
assert crop.size == derivative.size == tuple(submission['presentationDimensions'])
assert crop.tobytes() == derivative.tobytes(), 'Submission derivative must retain exact source crop pixels'
preservation_ref = os.environ.get('ENROLLMENT_PRESERVATION_REVISION', 'b5e9f6b')
assert not subprocess.check_output(['git', 'diff', preservation_ref, '--',
    'assets/js', 'assets/css/case-study.css', 'assets/css/global.css',
    '.scratch/enrollment/issues/01-metric-definition.md'], cwd=ROOT), 'Originals/shared behavior/issue01 preserved'
result = {'preservationRevision': preservation_ref, 'assetIntegrityAndManifest': True, 'originalsByteUnchanged': len(originals), 'submissionCropPixelIdentity': True, 'issue01Unchanged': True, 'sharedStylesAndScriptsUnchanged': True, 'authoredHeadAndAnalyticsUnchanged': True,
          'orientationContrastMatrixCases': len(contrast_matrix),
          'proposalGrowthPercent': (1105 - 408) / 408 * 100, 'contrast': measurements,
          'clickedDestinations': destinations}
(OUT / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('PASS originals, traceable manifest, shared styles/scripts and issue01')
