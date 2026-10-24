"""Focused two-width merger smoke; not the parent acceptance matrix."""
import argparse, json, re, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

p=argparse.ArgumentParser()
p.add_argument('--label',required=True)
p.add_argument('--base',default='http://127.0.0.1:8129')
a=p.parse_args()
out=Path('.scratch/convenios') / ('integration-smoke-'+a.label)
out.mkdir(exist_ok=True)
r={'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'base':a.base,'checks':[],'page_errors':[],'request_errors':[],'widths':[375,1440],'motion':'no-preference','limits':'Focused merge smoke only; full combined matrix belongs to parent.'}
def check(name,ok,detail=None):
    r['checks'].append({'name':name,'ok':bool(ok),'detail':detail})
    print(('PASS ' if ok else 'FAIL ')+name,flush=True)

with sync_playwright() as pw:
    b=pw.chromium.launch()
    r['browser']=b.version
    for w in r['widths']:
        ctx=b.new_context(viewport={'width':w,'height':900},reduced_motion='no-preference')
        pg=ctx.new_page()
        pg.on('pageerror',lambda e:r['page_errors'].append(str(e)))
        pg.on('requestfailed',lambda req:r['request_errors'].append({'url':req.url,'error':req.failure}))
        pg.on('response',lambda res:res.status>=400 and r['request_errors'].append({'url':res.url,'status':res.status}))
        pg.goto(a.base+'/case-studies/convenios.html',wait_until='networkidle')
        pg.evaluate('document.fonts.ready')
        seen=set()
        steps=[]
        pg.mouse.move(100,450)
        for _ in range(110):
            state=pg.evaluate('''() => ({y:scrollY,h:document.documentElement.scrollHeight,sections:[...document.querySelectorAll('main section')].map(s=>({id:s.getAttribute('aria-labelledby'),top:s.getBoundingClientRect().top,bottom:s.getBoundingClientRect().bottom,opacity:+getComputedStyle(s).opacity}))})''')
            steps.append(state)
            seen.update(s['id'] for s in state['sections'] if s['top']<900 and s['bottom']>64 and s['opacity']>.99)
            if state['y']+900>=state['h']-2: break
            pg.mouse.wheel(0,400)
            pg.wait_for_timeout(550)
        check(f'{w}: sections visible during ordinary wheel traversal',set(s['id'] for s in state['sections'])<=seen,sorted(seen))
        (out/f'wheel-{w}.json').write_text(json.dumps(steps,indent=2),encoding='utf-8')
        pg.wait_for_function("[...document.querySelectorAll('main img')].every(i=>i.complete && i.naturalWidth>0)")
        state=pg.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth,rows:[...document.querySelectorAll('article')].map(a=>({id:a.getAttribute('aria-labelledby'),text:a.innerText,images:a.querySelectorAll('img').length,first:a.firstElementChild.contains(a.querySelector('h3')),links:a.querySelectorAll('a').length,alt:a.querySelector('img')?.alt})),images:[...document.querySelectorAll('main img')].map(i=>({src:i.getAttribute('src'),natural:[i.naturalWidth,i.naturalHeight],box:[i.getBoundingClientRect().width,i.getBoundingClientRect().height]}))})''')
        r[str(w)]=state
        check(f'{w}: card/network/accounts/library sequence',[x['id'] for x in state['rows']]==['convenios-card','convenios-network','convenios-accounts','convenios-components'])
        check(f'{w}: no horizontal overflow',not state['overflow'])
        check(f'{w}: one image and explanation first for every row',all(x['images']==1 and x['first'] and x['alt'] for x in state['rows']))
        check(f'{w}: no raw-image links in rows',all(x['links']==0 for x in state['rows']))
        text=' '.join(x['text'] for x in state['rows'])
        check(f'{w}: all three ticket copy changes present','without logging out' in text and 'Results appear on a map' in text and 'list view' in text and 'predates Harmony' in text)
        for row in pg.get_by_role('article').all():
            row.scroll_into_view_if_needed()
            pg.wait_for_timeout(600)
            layout=row.evaluate('''a=>{const c=a.firstElementChild.getBoundingClientRect(),i=a.querySelector('img').getBoundingClientRect();return {order:innerWidth>768 || c.bottom<=i.top+1,noOverlap:c.right<=i.left+1 || i.right<=c.left+1 || c.bottom<=i.top+1 || i.bottom<=c.top+1}}''')
            check(f"{w}: {row.get_attribute('aria-labelledby')} layout",layout['order'] and layout['noOverlap'],layout)
        lib=pg.get_by_role('article').filter(has=pg.get_by_role('heading',name='A component library of its own.'))
        if lib.count()==0:
            lib=pg.locator('article[aria-labelledby="convenios-components"]')
        lib.scroll_into_view_if_needed()
        pg.wait_for_timeout(600)
        lib.screenshot(path=str(out/f'library-{w}.png'))
        lib.get_by_role('img').screenshot(path=str(out/f'library-image-{w}.png'))
        for name,heading in [('network','Find care in the provider network.'),('accounts','Make room for more than one account.')]:
            row=pg.get_by_role('article').filter(has=pg.get_by_role('heading',name=heading))
            row.scroll_into_view_if_needed()
            pg.wait_for_timeout(550)
            row.screenshot(path=str(out/f'{name}-{w}.png'))
        check(f'{w}: preserved store links and contact',pg.get_by_role('link',name=re.compile('Google Play')).count()==1 and pg.get_by_role('link',name=re.compile('App Store')).count()==1 and pg.locator('form').count()==1)
        ctx.close()
    b.close()
check('no JavaScript page errors',not r['page_errors'],r['page_errors'])
check('no failed requests or HTTP errors',not r['request_errors'],r['request_errors'])
r['summary']={'passed':sum(x['ok'] for x in r['checks']),'failed':sum(not x['ok'] for x in r['checks'])}
(out/'results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(r['summary'],flush=True)
raise SystemExit(bool(r['summary']['failed']))
