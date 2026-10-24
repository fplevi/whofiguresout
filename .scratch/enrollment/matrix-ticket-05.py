"""Current integrated Enrollment page matrix, adapted from existing Enrollment/Billing QA.

Uses qa-ticket-05.py's ENROLLMENT_QA_URL/OUT overrides.
No real contact submission or external mocks.
"""
import importlib.util
import json
import platform
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
spec = importlib.util.spec_from_file_location('ticket05', Path(__file__).with_name('qa-ticket-05.py'))
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
from playwright.sync_api import sync_playwright

OUT, URL = qa.OUT, qa.URL
ORIGIN = '{0.scheme}://{0.netloc}'.format(urlsplit(URL))
ROOT = Path(__file__).resolve().parents[2]
PROTECTED = ['header', '.cs-header', '.cs-hero-image', '[aria-labelledby="enrollment-problem"]',
             '[aria-labelledby="enrollment-role"]', '[aria-labelledby="enrollment-outcome"]', '.cs-next', '#contact']
R = {'baseline':'f8f9034', 'checks':[], 'matrix':[], 'pageErrors':[], 'failedRequests':[], 'contactPosts':[]}


def check(name, ok, detail=None):
    R['checks'].append({'name':name,'passed':bool(ok),'detail':detail})
    if not ok:
        print('FAIL', name, detail, flush=True)


def surfaces(page):
    result = {s:page.locator(s).evaluate('''e=>{
      const copy=e.cloneNode(true);copy.removeAttribute('style');return copy.outerHTML;
    }''') for s in PROTECTED}
    result['analyticsAndAuthoredScripts'] = page.locator('script').evaluate_all('''els=>els
      .filter(e=>!e.src || e.src.includes(location.host) || /googletagmanager|clarity/.test(e.src))
      .map(e=>e.outerHTML)''')
    result['decisionArguments'] = page.locator('.cs-decision__left').evaluate_all('els=>els.map(e=>e.outerHTML)')
    return result


def wheel_from_top(page, motion):
    start = page.evaluate('scrollY')
    page.mouse.move(100,350)
    seen, trace = set(), []
    selector = 'main > section, main h3, main figure, .cs-next'
    for _ in range(180):
        candidates = page.locator(selector).evaluate_all('''els=>els.filter(e=>{
          const r=e.getBoundingClientRect();return r.top<innerHeight && r.bottom>80;
        }).map(e=>e.getAttribute('aria-labelledby')||e.id||e.className)''')
        if any(c not in seen for c in candidates):
            page.wait_for_timeout(570 if motion=='no-preference' else 30)
        visible = page.locator(selector).evaluate_all('''els=>els.filter(e=>{
          const r=e.getBoundingClientRect();let visible=r.top<innerHeight&&r.bottom>80;
          for(let n=e;n;n=n.parentElement){const s=getComputedStyle(n);
            if(+s.opacity<.99||s.visibility==='hidden')visible=false;}
          return visible;
        }).map(e=>e.getAttribute('aria-labelledby')||e.id||e.className)''')
        seen.update(visible)
        trace.append(page.evaluate('scrollY'))
        if page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'):
            break
        page.mouse.wheel(0,300)
        page.wait_for_timeout(90)
    expected = page.locator(selector).evaluate_all('els=>els.map(e=>e.getAttribute("aria-labelledby")||e.id||e.className)')
    hidden = page.locator('main > section').evaluate_all('els=>els.filter(e=>+getComputedStyle(e).opacity<.99).map(e=>e.getAttribute("aria-labelledby"))')
    return {'startY':start,'input':'mouse.wheel(0,300)','positions':trace,
            'bottomReached':page.evaluate('scrollY+innerHeight>=document.documentElement.scrollHeight-2'),
            'seen':sorted(seen),'missing':[e for e in expected if e not in seen],'hiddenAtEnd':hidden}


def contrast(page):
    # Computed sRGB foreground alpha is composited over every ancestor background.
    return page.locator('figure figcaption h4, figure figcaption p, .enrollment-discovery__copy').evaluate_all(r'''els=>{
      const rgba=s=>{const a=s.match(/[\d.]+/g).map(Number);return [...a.slice(0,3),a[3]??1]};
      const over=(a,b)=>a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3]));
      const lum=c=>c.map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4)
        .reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
      return els.map(e=>{
        const chain=[];for(let n=e;n;n=n.parentElement)chain.unshift(n);
        let bg=[255,255,255];for(const n of chain)bg=over(rgba(getComputedStyle(n).backgroundColor),bg);
        const s=getComputedStyle(e),fg=over(rgba(s.color),bg),a=lum(fg),b=lum(bg);
        return {text:e.textContent.trim(),cssColor:s.color,background:bg,compositedForeground:fg,
          ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05),fontSize:s.fontSize};
      });
    }''')


def comparison(page, label):
    slider = page.get_by_role('slider')
    check(label+' one comparator', slider.count()==1)
    page.locator('.cs-header__back').focus()
    page.keyboard.press('Tab')
    check(label+' Tab enters comparator', slider.evaluate('e=>e===document.activeElement'))
    page.wait_for_timeout(180)
    focus = slider.evaluate('''e=>{
      const s=getComputedStyle(e),p=getComputedStyle(e.parentElement);
      return {name:e.getAttribute('aria-label'),opacity:s.opacity,outline:s.outline,
        parentOutline:p.outline,parentShadow:p.boxShadow,focusVisible:e.matches(':focus-visible')};
    }''')
    values=[]
    for key,value in [('Home',0),('ArrowRight',1),('End',100),('ArrowLeft',99)]:
        page.keyboard.press(key)
        page.wait_for_timeout(120)
        reveal=slider.evaluate('''e=>{
          const c=e.parentElement;return {clip:getComputedStyle(c.querySelector('.cs-compare__before')).clipPath,
            left:parseFloat(getComputedStyle(c.querySelector('.cs-compare__handle')).left),width:c.clientWidth};
        }''')
        check(label+' '+key+' value and visible reveal', int(slider.input_value())==value
              and reveal['clip']==f'inset(0px {100-value}% 0px 0px)'
              and abs(reveal['left']/reveal['width']*100-value)<1, reveal)
        values.append({'key':key,'value':slider.input_value(),**reveal})
    page.keyboard.press('Tab')
    check(label+' Tab exits comparator', page.locator('.cs-next__link').evaluate('e=>e===document.activeElement'))
    slider.evaluate('e=>e.scrollIntoView({block:"start",behavior:"instant"})')
    page.evaluate('scrollBy(0,-110)')
    page.wait_for_timeout(600)
    box=slider.bounding_box()
    y=max(150,box['y']+min(120,box['height']/2))
    check(label+' pointer/touch point below nav within viewport',80<y<page.viewport_size['height'])
    page.mouse.click(box['x']+box['width']*.25,y)
    pointer=int(slider.input_value())
    check(label+' pointer sets quarter reveal',15<=pointer<=35)
    page.touchscreen.tap(box['x']+box['width']*.75,y)
    touch=int(slider.input_value())
    check(label+' touch sets three-quarter reveal',65<=touch<=85)
    relocated=slider.locator('xpath=ancestor::figure').count()>0
    if relocated:
        check(label+' relocated comparator meaningfully named',focus['name'] not in ['',None,'Comparison slider'])
        check(label+' relocated comparator visible keyboard focus',focus['focusVisible'] and
              ((focus['opacity']!='0' and not focus['outline'].startswith('0px')) or not focus['parentOutline'].startswith('0px')))
    return {'keyboard':values,'focus':focus,'pointerValue':pointer,'emulatedTouchValue':touch,
            'relocated':relocated,'pendingTicket03':not relocated}


with sync_playwright() as p:
    browser=p.chromium.launch()
    R['environment']={'os':platform.platform(),'python':platform.python_version(),'browser':'Chromium '+browser.version,
                      'url':URL,'headless':True,'deviceScaleFactor':1,'emulatedTouch':True}
    baseline=subprocess.check_output(['git','show','f8f9034:case-studies/enrollment.html'],cwd=ROOT).decode('utf-8')
    bp=browser.new_page(reduced_motion='reduce')
    bp.route(URL,lambda route:route.fulfill(status=200,content_type='text/html',body=baseline))
    bp.goto(URL,wait_until='networkidle')
    protected=surfaces(bp)
    bp.close()
    for width in [320,375,768,1440]:
        for motion in ['no-preference','reduce']:
            height=900 if width==1440 else 700
            label=f'{width}x{height}/{motion}'
            ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion=motion,has_touch=True)
            page=ctx.new_page()
            page.on('pageerror',lambda e,l=label:R['pageErrors'].append({'matrix':l,'error':str(e)}))
            page.on('requestfailed',lambda r,l=label:R['failedRequests'].append({'matrix':l,'url':r.url,'failure':r.failure}))
            page.on('response',lambda r,l=label:r.status>=400 and R['failedRequests'].append({'matrix':l,'url':r.url,'status':r.status}))
            page.on('request',lambda r:r.method=='POST' and 'formspree' in r.url and R['contactPosts'].append(r.url))
            page.goto(URL,wait_until='networkidle')
            page.evaluate('document.fonts.ready')
            matches={s:surfaces(page)[s]==v for s,v in protected.items()}
            check(label+' protected surfaces match f8f9034',all(matches.values()),matches)
            if motion=='reduce':
                check(label+' reduced content immediately available',page.locator('main > section').evaluate_all('els=>els.every(e=>+getComputedStyle(e).opacity===1)'))
            wheel=wheel_from_top(page,motion)
            check(label+' all narrative visible during real wheel traversal from top',wheel['startY']==0 and wheel['bottomReached'] and not wheel['missing'] and not wheel['hiddenAtEnd'],wheel)
            page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
            qa.story(page)
            check(label+' submission story passes',True)
            images=page.locator('img').evaluate_all('''els=>els.map(i=>{
              const r=i.getBoundingClientRect();return {src:i.getAttribute('src'),alt:i.alt,natural:[i.naturalWidth,i.naturalHeight],
                intrinsic:[+i.getAttribute('width'),+i.getAttribute('height')],rendered:[r.width,r.height],loading:i.loading,decoding:i.decoding};
            })''')
            check(label+' all images ready, proportional, lazy, async, intrinsic and named',all(i['natural']==i['intrinsic'] and abs(i['rendered'][0]/i['rendered'][1]-i['natural'][0]/i['natural'][1])<.01
                  and i['loading']=='lazy' and i['decoding']=='async' and i['alt'] for i in images),images)
            figures=page.locator('figure').evaluate_all('''els=>els.map(f=>{
              const c=f.querySelector('figcaption'),i=f.querySelector('img'),cr=c.getBoundingClientRect(),ir=i.getBoundingClientRect();
              return {name:f.getAttribute('aria-labelledby'),images:f.querySelectorAll('img').length,
                domCopyFirst:!!(c.compareDocumentPosition(i)&Node.DOCUMENT_POSITION_FOLLOWING),copyAbove:cr.bottom<=ir.top+.5};
            })''')
            check(label+' explanations before images without overlap',all(f['domCopyFirst'] and f['copyAbove'] for f in figures),figures)
            check(label+' no horizontal overflow',page.evaluate('document.documentElement.scrollWidth')==width)
            outside=page.locator('main *').evaluate_all('''els=>els.filter(e=>{
              const r=e.getBoundingClientRect();return r.width>0&&(r.left<-.5||r.right>innerWidth+.5)&&!e.closest('.sr-only');
            }).map(e=>e.tagName+'.'+e.className)''')
            check(label+' no viewport-edge clipping',not outside,outside)
            textfit=page.locator('figure figcaption h4,figure figcaption p,.enrollment-discovery__copy,.cs-stat__number').evaluate_all('els=>els.every(e=>e.scrollWidth<=e.clientWidth+1)')
            check(label+' explanation and metrics fit',textfit)
            ratios=contrast(page)
            check(label+' measured explanation contrast and body size',bool(ratios) and all(c['ratio']>=4.5 and float(c['fontSize'][:-2])>=16 for c in ratios),ratios)
            # Inspect each currently integrated evidence at this width, after real traversal.
            for i in range(page.locator('figure').count()):
                figure=page.locator('figure').nth(i)
                name=figure.get_attribute('aria-labelledby')
                figure.screenshot(path=str(OUT/f'{name}-{width}-{motion}.png'),style='.nav{visibility:hidden!important}')
            board=page.locator('[aria-labelledby="enrollment-discovery"]')
            if board.count():
                board.screenshot(path=str(OUT/f'discovery-{width}-{motion}.png'),style='.nav{visibility:hidden!important}')
            comp=comparison(page,label)
            page.locator('#name').focus()
            page.keyboard.press('Tab')
            check(label+' contact name to email',page.locator('#email').evaluate('e=>e===document.activeElement'))
            page.keyboard.press('Tab')
            check(label+' contact email to message',page.locator('#message').evaluate('e=>e===document.activeElement'))
            check(label+' preserved navigation destinations',page.locator('.nav a').evaluate_all('els=>els.map(e=>e.getAttribute("href"))')==['../','../#work','../#contact','../#about'])
            page.locator('.cs-next__link').click()
            check(label+' next project opens',page.url.endswith('/case-studies/convenios.html'))
            page.go_back(wait_until='networkidle')
            page.locator('.cs-header__back').click()
            check(label+' back to work opens root',page.url.rstrip('/')==ORIGIN)
            R['matrix'].append({'width':width,'height':height,'motion':motion,'wheel':wheel,'images':images,
                               'figures':figures,'comparison':comp,'contrast':ratios})
            ctx.close()
            print('DONE',label,flush=True)
    browser.close()
check('no application errors',not R['pageErrors'],R['pageErrors'])
local=[r for r in R['failedRequests'] if r['url'].startswith(ORIGIN+'/')]
check('no local failed assets',not local,local)
check('no actual contact POST',not R['contactPosts'],R['contactPosts'])
R['summary']={'passed':sum(c['passed'] for c in R['checks']),'failed':sum(not c['passed'] for c in R['checks'])}
(OUT/'matrix.json').write_text(json.dumps(R,indent=2),encoding='utf-8')
print(json.dumps(R['summary']))
assert R['summary']['failed']==0
