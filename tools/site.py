"""Applique l'en-tête, le favicon et le menu à toutes les pages, et régénère nav.js.
À relancer après avoir ajouté une page (et après lex.py / exam.py)."""
import re, os, glob, json, html
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
idx = open(R + 'index.html', encoding='utf-8').read()

# --- données du menu, lues dans le sommaire ---
sections, cur = [], None
tools = []
for m in re.finditer(r'<p class="mod">(.*?)</p>|<a class="card unit[^"]*" href="units/([a-z0-9-]+)\.html"[^>]*>(?:<span[^>]*>[^<]*</span>)?<div><b>(.*?)</b>', idx):
    if m.group(1):
        cur = {'t': html.unescape(m.group(1)), 'p': []}; sections.append(cur)
    else:
        slug, t = m.group(2), html.unescape(re.sub(r'<[^>]+>', '', m.group(3)))
        t = re.sub(r'^(Modules?|Module)\s*:\s*', '', t)
        t = t[0].upper() + t[1:]
        (cur['p'] if cur else tools).append([slug, t])
DKEYS = ['pre', 'id', 'ne', 'st', 'co', 'mo']
DINFO = {'pre': ('📐', ''), 'id': ('🔐', '20–25 %'), 'ne': ('🌐', '15–20 %'), 'st': ('🗄️', '15–20 %'), 'co': ('🖥️', '20–25 %'), 'mo': ('📊', '10–15 %')}
PAGEDOM = {}
for k, sec in zip(DKEYS, sections):
    sec['k'] = k; sec['i'] = DINFO[k][0]; sec['w'] = DINFO[k][1]
    for slug, _ in sec['p']: PAGEDOM.setdefault(slug, k)
NAV = {'tools': tools, 'sections': sections}

NAVJS = r'''/* Menu du site : généré par tools/site.py */
(function(){
var NAV=__NAV__;
var root=document.querySelector('script[src$="nav.js"]').getAttribute('src').replace('nav.js','');
var here=(location.pathname.split('/').pop()||'index.html').replace('.html','');
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function link(p){var on=p[0]===here;return '<a href="'+root+'units/'+p[0]+'.html"'+(on?' aria-current="page"':'')+'>'+esc(p[1])+'</a>';}
/* « Sur cette page » : les h2 de la page */
function slugify(t){return t.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)||'s';}
var hs=[].slice.call(document.querySelectorAll('main h2'));
hs.forEach(function(h,i){if(!h.id){var id=slugify(h.textContent),k=id,n=2;while(document.getElementById(k))k=id+'-'+(n++);h.id=k;}});
function toc(){if(hs.length<3)return '';return '<details class="drawer-grp drawer-toc" open><summary><i aria-hidden="true">📍</i>Sur cette page<span>'+hs.length+'</span></summary>'+
  hs.map(function(h){return '<a href="#'+h.id+'" data-close>'+esc(h.textContent.replace(/^[^\wÀ-ÿ]+/,'').trim())+'</a>';}).join('')+'</details>';}
var d=document.createElement('div');d.id='drawer';d.className='drawer';d.hidden=true;
d.innerHTML='<div class="drawer-bg" data-close></div><nav class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu du site">'+
 '<div class="drawer-head"><a class="brand" href="'+root+'index.html"><img src="'+root+'favicon.svg" alt="" width="26" height="26">AZ-104 <span>en images</span></a><button class="icon-btn" type="button" data-close aria-label="Fermer le menu">✕</button></div>'+
 '<input class="drawer-q" type="search" placeholder="Chercher une page…" aria-label="Chercher une page" autocomplete="off">'+
 '<div class="drawer-body">'+toc()+'<a class="drawer-home'+(here==='index'?'" aria-current="page':'')+'" href="'+root+'index.html">🏠 Sommaire</a>'+
 '<p class="drawer-sec">Outils</p><div class="drawer-tools">'+NAV.tools.map(link).join('')+'</div>'+
 NAV.sections.map(function(s){var open=s.p.some(function(p){return p[0]===here;});
   return '<details class="drawer-grp" data-dom="'+s.k+'"'+(open?' open':'')+'><summary><i aria-hidden="true">'+s.i+'</i>'+esc(s.t.replace(/^\d+\s*·\s*/,''))+'<span>'+s.p.length+'</span></summary>'+s.p.map(link).join('')+'</details>';}).join('')+
 '<p class="drawer-empty" hidden>Aucune page trouvée.</p></div></nav>';
document.body.appendChild(d);
var btn=document.getElementById('menuBtn'),q=d.querySelector('.drawer-q'),last=null;
function open(){last=document.activeElement;d.hidden=false;document.documentElement.classList.add('noscroll');if(btn)btn.setAttribute('aria-expanded','true');
  requestAnimationFrame(function(){d.classList.add('in');});setTimeout(function(){var c=d.querySelector('[aria-current]');if(c)c.scrollIntoView({block:'center'});if(matchMedia('(pointer:fine)').matches)q.focus();},60);}
function close(){d.classList.remove('in');document.documentElement.classList.remove('noscroll');if(btn)btn.setAttribute('aria-expanded','false');
  setTimeout(function(){d.hidden=true;},200);if(last&&last.focus)last.focus();}
if(btn)btn.addEventListener('click',open);
var fab=document.getElementById('fab');if(fab){fab.addEventListener('click',function(e){e.preventDefault();open();});}
d.addEventListener('click',function(e){var c=e.target.closest('[data-close]');if(!c)return;
  if(c.tagName==='A'){var t=document.getElementById(c.getAttribute('href').slice(1));e.preventDefault();close();
    if(t){var det=t.closest('details');if(det)det.open=true;setTimeout(function(){t.scrollIntoView({behavior:'smooth',block:'start'});history.replaceState(null,'','#'+t.id);},210);}return;}
  close();});
/* barre d'onglets mobile */
var tb=document.createElement('nav');tb.className='tabbar';tb.setAttribute('aria-label','Navigation rapide');
function tab(href,ic,lb,on){return '<a href="'+href+'"'+(on?' aria-current="page"':'')+'><i aria-hidden="true">'+ic+'</i>'+lb+'</a>';}
tb.innerHTML=tab(root+'index.html','🏠','Accueil',here==='index')+tab(root+'units/examen-blanc.html','📝','Examen',here==='examen-blanc')+
  tab(root+'units/lexique.html','📖','Lexique',here==='lexique')+'<button type="button" class="tab-menu" aria-controls="drawer"><i aria-hidden="true">☰</i>Menu</button>';
document.body.appendChild(tb);document.body.classList.add('has-tabbar');
tb.querySelector('.tab-menu').addEventListener('click',open);
/* barre de lecture */
if(document.querySelector('.page-hero')){var rb=document.createElement('div');rb.className='readbar';rb.setAttribute('aria-hidden','true');document.body.appendChild(rb);
  var tick=false;function upd(){tick=false;var h=document.documentElement,m=h.scrollHeight-h.clientHeight;rb.style.transform='scaleX('+(m>0?Math.min(1,h.scrollTop/m):0)+')';}
  addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd);}},{passive:true});upd();}
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'&&!d.hidden)close();
  if(e.key==='Tab'&&!d.hidden){var f=d.querySelectorAll('a[href],button,input,summary'),a=[].filter.call(f,function(x){return x.offsetParent!==null;});
    if(!a.length)return;var first=a[0],end=a[a.length-1];
    if(e.shiftKey&&document.activeElement===first){e.preventDefault();end.focus();}else if(!e.shiftKey&&document.activeElement===end){e.preventDefault();first.focus();}}
});
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');}
q.addEventListener('input',function(){var w=norm(q.value.trim()),any=false;
  d.querySelectorAll('.drawer-grp').forEach(function(g){var n=0;g.querySelectorAll('a').forEach(function(a){var ok=!w||norm(a.textContent).indexOf(w)>=0;a.hidden=!ok;if(ok)n++;});
    g.hidden=!n;if(w)g.open=!!n;if(n)any=true;});
  var nt=0;d.querySelectorAll('.drawer-tools a').forEach(function(a){var ok=!w||norm(a.textContent).indexOf(w)>=0;a.hidden=!ok;if(ok){any=true;nt++;}});
  d.querySelector('.drawer-sec').hidden=!nt;
  d.querySelector('.drawer-empty').hidden=any;});
/* icône du bouton thème */
var r=document.documentElement,t=document.getElementById('theme');
function dark(){return r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;}
function icon(){if(!t)return;var dk=dark();t.textContent=dk?'☀️':'🌙';t.setAttribute('aria-label',dk?'Passer au thème clair':'Passer au thème sombre');
  var m=document.querySelector('meta[name="theme-color"]');if(m)m.content=dk?'#0f141c':'#ffffff';}
if(t){t.addEventListener('click',function(){setTimeout(icon,0);});icon();}
})();
'''
# --- chiffres du sommaire ---
lexs=open(R+'units/lexique.html',encoding='utf-8').read()
nterms=lexs[lexs.index('var L='):].split('\n')[0].count('"t":')
exs=open(R+'units/examen-blanc.html',encoding='utf-8').read()
nq=exs[exs.index('var Q='):].split('\n')[0].count('"q":')
npages=sum(len(x['p']) for x in sections)
for k,v in (('pages',npages),('terms',nterms),('questions',nq)):
    idx=re.sub(r'(<b data-stat="%s">)\d+(</b>)'%k, r'\g<1>%d\g<2>'%v, idx)
open(R+'index.html','w',encoding='utf-8').write(idx)
open(R + 'nav.js', 'w', encoding='utf-8').write(NAVJS.replace('__NAV__', json.dumps(NAV, ensure_ascii=False)))

def header(root):
    return ('<header class="top"><div class="wrap">\n'
            f'  <a class="brand" href="{root}index.html"><img src="{root}favicon.svg" alt="" width="28" height="28">AZ-104 <span>en images</span></a>\n'
            '  <div class="top-actions"><button class="icon-btn" id="theme" type="button" aria-label="Changer de thème">🌙</button>'
            '<button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="drawer"><span aria-hidden="true">☰</span> Menu</button></div>\n'
            '</div></header>')

def headlinks(root):
    return (f'<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">\n'
            f'<link rel="icon" href="{root}favicon-32.png" sizes="32x32" type="image/png">\n'
            f'<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">\n'
            '<meta name="theme-color" content="#ffffff">\n')

for f in [R + 'index.html'] + sorted(glob.glob(R + 'units/*.html')):
    root = '' if f.endswith('/index.html') and '/units/' not in f else '../'
    s = open(f, encoding='utf-8').read()
    s = re.sub(r'<link rel="icon"[^>]*>\n|<link rel="apple-touch-icon"[^>]*>\n|<meta name="theme-color"[^>]*>\n', '', s)
    s = s.replace('<link rel="stylesheet"', headlinks(root) + '<link rel="stylesheet"', 1)
    s = re.sub(r'<header class="top">.*?</header>', lambda m: header(root), s, count=1, flags=re.S)
    s = re.sub(r'\n?<script src="(\.\./)?nav\.js"( defer)?></script>', '', s)
    s = s.replace('</body>', f'<script src="{root}nav.js"></script>\n</body>', 1)
    s = s.replace('aria-label="Retour au sommaire">☰ Sommaire</a>', 'aria-label="Ouvrir le menu">☰ Menu</a>')
    # polices : Inter (texte) + Plus Jakarta Sans (titres)
    s = re.sub(r'<link href="https://fonts.googleapis.com/css2\?[^"]*" rel="stylesheet">',
               '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">', s, count=1)
    if 'fonts.gstatic.com' not in s:
        s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', 1)
    s = s.replace('<meta name="viewport" content="width=device-width,initial-scale=1">', '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">')
    # domaine de la page (couleur)
    slug = os.path.basename(f)[:-5]
    dom = PAGEDOM.get(slug, 'tools' if '/units/' in f else 'home')
    s = re.sub(r'<body[^>]*>', '<body data-dom="%s">' % dom, s, count=1)
    # en-tête illustré des pages d'unité
    if '/units/' in f and 'class="page-hero"' not in s and dom in DINFO:
        sec = next(x for x in sections if x.get('k') == dom)
        def wrap(m):
            pill = '<span class="dom-pill">%s %s</span>' % (sec['i'], re.sub(r'^\d+\s*·\s*', '', sec['t']))
            return '<header class="page-hero" data-ico="%s">\n  %s\n  %s</header>' % (sec['i'], pill, m.group(0))
        s = re.sub(r'<nav class="crumbs".*?</nav>\s*<h1>.*?</h1>\s*<p class="lede">.*?</p>(\s*<div class="meta">.*?</div>)?', wrap, s, count=1, flags=re.S)
    open(f, 'w', encoding='utf-8').write(s)
print('pages:', len(glob.glob(R + 'units/*.html')) + 1, '| sections:', [ (s['t'], len(s['p'])) for s in sections ], '| outils:', len(tools))
