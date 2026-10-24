"""Swap a case header to the word-search hero. Usage: apply.py <case> <words.json>"""
import io, json, re, sys
case, spec = sys.argv[1], json.load(io.open(sys.argv[2], encoding='utf-8'))
p = f'case-studies/{case}.html'
raw = io.open(p, encoding='utf-8', newline='').read()
CRLF, LF = '\r\n', '\n'
eol = CRLF if CRLF in raw else LF
s = raw.replace(CRLF, LF)

def rep(a, b, regex=False):
    global s
    n = len(re.findall(a, s)) if regex else s.count(a)
    assert n == 1, (n, a[:80])
    s = re.sub(a, b, s) if regex else s.replace(a, b)

def item(w, disp, cat, cap):
    blank = ' '.join('_' * len(w))
    return f'''          <li class="wsh__item" data-word="{w}">
            <button type="button" class="wsh__chip" disabled><span class="wsh__term-blank" aria-hidden="true">{blank}</span><span class="wsh__term-text">{disp}</span></button>
            <span class="wsh__cat">{cat}</span>
            <span class="wsh__caption">{cap}</span>
          </li>
'''

game = f'''
      <div class="wsh__game" role="group" aria-labelledby="wsh-kicker">
        <div class="wsh__game-head">
          <p class="wsh__kicker" id="wsh-kicker">The case in five words</p>
          <p class="wsh__count" aria-live="polite"></p>
        </div>
        <div class="wsh__grid" aria-hidden="true"></div>
        <ul class="wsh__legend" role="list">
{''.join(item(*w) for w in spec['words'])}        </ul>
        <div class="wsh__footer">
          <button type="button" class="wsh__reveal">Reveal all</button>
        </div>
      </div>
'''
css = f'../assets/css/{spec["css_after"]}'
rep(f'  <link rel="stylesheet" href="{css}" />\n',
    f'  <link rel="stylesheet" href="{css}" />\n  <link rel="stylesheet" href="../assets/css/case-hero-wordsearch.css" />\n')
# header_open: [comment, section attrs after class] when a page deviates from the default markup
comment, attrs = spec.get('header_open', ['Case Header', ''])
rep(f'    <!-- {comment} -->\n    <section class="cs-header"{attrs}>',
    f'    <!-- Case Header: word-search hero (assets/js/case-hero-wordsearch.js) -->\n    <section class="cs-header wsh"{attrs} data-cols="24" data-rows="7" data-cols-mobile="12" data-rows-mobile="12" data-seed="{spec.get("seed", 7)}">')
rep(r'(<p class="cs-header__hook">.*?</p>\n)(\n      <div class="cs-meta")', lambda m: m.group(1) + game + m.group(2), regex=True)
rep(spec['hero_block'], '')
rep('  <script src="../assets/js/scroll-animations.js" type="module"></script>\n',
    '  <script src="../assets/js/scroll-animations.js" type="module"></script>\n  <script src="../assets/js/case-hero-wordsearch.js" type="module"></script>\n')
for a, b in spec.get('extra', []):
    rep(a, b)
io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(LF, eol))
print('ok', p, repr(eol))
