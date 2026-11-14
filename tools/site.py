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
NAV = {'tools': tools, 'sections': sections}

NAVJS = r'''/* Menu du site : généré par tools/site.py */
(function(){
var NAV=__NAV__;
var root=document.querySelector('script[src$="nav.js"]').getAttribute('src').replace('nav.js','');
var here=(location.pathname.split('/').pop()||'index.html').replace('.html','');
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function link(p){var on=p[0]===here;return '<a href="'+root+'units/'+p[0]+'.html"'+(on?' aria-current="page"':'')+'>'+esc(p[1])+'</a>';}
var d=document.createElement('div');d.id='drawer';d.className='drawer';d.hidden=true;
d.innerHTML='<div class="drawer-bg" data-close></div><nav class="drawer-panel" role="dialog" aria-modal="true" aria-label="Menu du site">'+
 '<div class="drawer-head"><a class="brand" href="'+root+'index.html"><img src="'+root+'favicon.svg" alt="" width="26" height="26">AZ-104 <span>en images</span></a><button class="icon-btn" type="button" data-close aria-label="Fermer le menu">✕</button></div>'+
 '<input class="drawer-q" type="search" placeholder="Chercher une page…" aria-label="Chercher une page" autocomplete="off">'+
 '<div class="drawer-body"><a class="drawer-home'+(here==='index'?'" aria-current="page':'')+'" href="'+root+'index.html">🏠 Sommaire</a>'+
 '<p class="drawer-sec">Outils</p><div class="drawer-tools">'+NAV.tools.map(link).join('')+'</div>'+
 NAV.sections.map(function(s){var open=s.p.some(function(p){return p[0]===here;});
   return '<details class="drawer-grp"'+(open?' open':'')+'><summary>'+esc(s.t)+'<span>'+s.p.length+'</span></summary>'+s.p.map(link).join('')+'</details>';}).join('')+
 '<p class="drawer-empty" hidden>Aucune page trouvée.</p></div></nav>';
document.body.appendChild(d);
var btn=document.getElementById('menuBtn'),q=d.querySelector('.drawer-q'),last=null;
function open(){last=document.activeElement;d.hidden=false;document.documentElement.classList.add('noscroll');if(btn)btn.setAttribute('aria-expanded','true');
  requestAnimationFrame(function(){d.classList.add('in');});setTimeout(function(){var c=d.querySelector('[aria-current]');if(c)c.scrollIntoView({block:'center'});if(matchMedia('(pointer:fine)').matches)q.focus();},60);}
function close(){d.classList.remove('in');document.documentElement.classList.remove('noscroll');if(btn)btn.setAttribute('aria-expanded','false');
  setTimeout(function(){d.hidden=true;},200);if(last&&last.focus)last.focus();}
if(btn)btn.addEventListener('click',open);
var fab=document.getElementById('fab');if(fab){fab.addEventListener('click',function(e){e.preventDefault();open();});}
d.addEventListener('click',function(e){if(e.target.closest('[data-close]'))close();});
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
    open(f, 'w', encoding='utf-8').write(s)
print('pages:', len(glob.glob(R + 'units/*.html')) + 1, '| sections:', [ (s['t'], len(s['p'])) for s in sections ], '| outils:', len(tools))
