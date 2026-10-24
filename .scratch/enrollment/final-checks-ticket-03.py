"""Ticket-specific adaptation of final_checks.py: preservation, assets, measured contrast."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(os.environ['TEMP']) / 'portfolio-convenios-qa'))
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.scratch/enrollment/qa/ticket-03'


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
    page.goto('http://127.0.0.1:8123/case-studies/enrollment.html', wait_until='domcontentloaded')
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
        page.goto('http://127.0.0.1:8123/case-studies/enrollment.html', wait_until='domcontentloaded')
        page.locator(selector).click()
        page.wait_for_url('http://127.0.0.1:8123' + suffix)
        destinations.append(page.url)
    print('PASS actual navigation, back and next-project clicks')
    browser.close()

manifest = json.loads((ROOT / '.scratch/enrollment/presentation-assets-03.json').read_text(encoding='utf-8'))
baseline_html = subprocess.check_output(['git', 'show', 'f8f9034:case-studies/enrollment.html'], cwd=ROOT).decode('utf-8')
current_html = (ROOT / 'case-studies/enrollment.html').read_text(encoding='utf-8')
assert re.search(r'<head>[\s\S]*?</head>', baseline_html).group() == re.search(r'<head>[\s\S]*?</head>', current_html).group(), 'Authored head and analytics declarations preserved'
for item in manifest['assets']:
    source = ROOT / item['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sha256']
    assert source.read_bytes() == subprocess.check_output(['git', 'show', f'f8f9034:{item["source"]}'], cwd=ROOT)
assert not subprocess.check_output(['git', 'diff', 'f8f9034', '--', 'assets/images/enrollment',
    'assets/js', 'assets/css/case-study.css', 'assets/css/global.css',
    '.scratch/enrollment/issues/01-metric-definition.md'], cwd=ROOT), 'Originals/shared behavior/issue01 preserved'
result = {'assetIntegrityAndManifest': True, 'issue01Unchanged': True, 'sharedStylesAndScriptsUnchanged': True, 'authoredHeadAndAnalyticsUnchanged': True,
          'proposalGrowthPercent': (1105 - 408) / 408 * 100, 'contrast': measurements,
          'clickedDestinations': destinations}
(OUT / 'final-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print('PASS originals, traceable manifest, shared styles/scripts and issue01')
