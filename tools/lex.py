import re,glob,json,html,unicodedata
R=__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))+'/'
idx=open(R+'index.html').read()
sec={};cur=None;titles={}
for m in re.finditer(r'<p class="mod">(.*?)</p>|href="units/([a-z0-9-]+)\.html"',idx):
    if m.group(1): cur=re.sub(r'^\d+\s*·\s*','',html.unescape(m.group(1)))
    elif cur: sec.setdefault(m.group(2),cur)
def clean(x):
    x=re.sub(r'<[^>]+>','',x); return html.unescape(x).strip()
def norm(x): return ''.join(c for c in unicodedata.normalize('NFD',x.lower()) if unicodedata.category(c)!='Mn')
order=[]
for m in re.finditer(r'href="units/([a-z0-9-]+)\.html"',idx):
    if m.group(1) not in order: order.append(m.group(1))
E={}
for slug in order:
    try: s=open(R+'units/'+slug+'.html').read()
    except: continue
    t=re.search(r'<title>(.*?)</title>',s).group(1); titles[slug]=html.unescape(t)
    m=re.search(r'<h2[^>]*>\s*Lexique.*?</h2>(.*?)</table>',s,re.S)
    if not m: continue
    for row in re.findall(r'<tr>(.*?)</tr>',m.group(1),re.S):
        c=[clean(x) for x in re.findall(r'<td[^>]*>(.*?)</td>',row,re.S)]
        if len(c)<3: continue
        k=norm(c[0])
        if k in E:
            if slug not in E[k]['p']: E[k]['p'].append(slug)
            if len(c[2])>len(E[k]['d']): E[k]['d']=c[2]
        else: E[k]={'t':c[0],'en':c[1],'d':c[2],'p':[slug],'s':sec.get(slug,'')}
L=sorted(E.values(),key=lambda e:norm(e['t']))
print(len(L),'termes')
cmd=open(R+'units/commandes.html').read()
head=cmd[:cmd.index('<style>')].replace('<title>Mes commandes Azure</title>','<title>Lexique AZ-104</title>')
style=cmd[cmd.index('<style>'):cmd.index('</style>')]+'''
.letter{font-size:13px;font-weight:700;color:var(--cloud);margin:16px 0 2px;letter-spacing:.05em}
.term{padding:12px 16px}
.term .h{display:flex;flex-wrap:wrap;gap:4px 10px;align-items:baseline}
.term b{font-size:16px}
.term .en{font-size:13px;color:var(--muted);font-style:italic}
.term .d{font-size:14.5px;margin:6px 0 0}
.term .meta2{display:flex;flex-wrap:wrap;gap:6px 12px;margin-top:6px;font-size:13px;color:var(--muted)}
.list{gap:8px}
</style>'''
headerpart=cmd[cmd.index('</style>')+8:cmd.index('<main class="wrap">')]
theme_js=cmd[cmd.index('<script>'):cmd.index("var TOOLS=")]
body='''<main class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane"><a class="crumb-home" href="../index.html">🏠 Accueil</a><span class="sep">›</span><span class="here">Lexique</span></nav>
  <h1>Lexique AZ-104</h1>
  <p class="lede">Tous les termes et sigles des pages du site, réunis et classés de A à Z. Tape un mot en français ou en anglais (ex. « SAS », « zone », « peering ») ou filtre par section.</p>
  <div class="search" role="search">
    <span class="ico" aria-hidden="true">🔎</span>
    <input id="q" type="search" placeholder="Chercher un terme, un sigle, une définition…" autocomplete="off" aria-label="Chercher un terme">
  </div>
  <div>
    <div class="filters" id="themes" aria-label="Filtrer par section"></div>
    <p class="count" id="count" aria-live="polite"></p>
  </div>
  <div class="list" id="list"></div>
  <footer>Généré à partir des lexiques de chaque page. Mis à jour à chaque nouveau module.</footer>
  <a class="fab-home" id="fab" href="../index.html" aria-label="Retour au sommaire">☰ Sommaire</a>
</main>
'''
js='var L='+json.dumps(L,ensure_ascii=False)+';\nvar PAGES='+json.dumps(titles,ensure_ascii=False)+';\n'+r'''
var state={q:'',th:''};
try{var s=JSON.parse(sessionStorage.getItem('lex-filtres')||'null');if(s)state=s;}catch(e){}
function norm(s){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function hl(text,words){var h=esc(text);words.forEach(function(w){if(w.length<2)return;var re=new RegExp('('+w.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');h=h.replace(re,'<mark>$1</mark>');});return h;}
var themes=[];L.forEach(function(x){if(x.s&&themes.indexOf(x.s)<0)themes.push(x.s);});
var list=document.getElementById('list'),q=document.getElementById('q');
function chips(){var el=document.getElementById('themes');el.innerHTML='';
  [['','Toutes']].concat(themes.map(function(t){return [t,t];})).forEach(function(it){
    var b=document.createElement('button');b.type='button';b.className='f';b.textContent=it[1];
    b.setAttribute('aria-pressed',state.th===it[0]);b.onclick=function(){state.th=it[0];render();};el.appendChild(b);});}
function render(){
  try{sessionStorage.setItem('lex-filtres',JSON.stringify(state));}catch(e){}
  chips();
  var words=norm(state.q).split(/\s+/).filter(Boolean),raw=state.q.split(/\s+/).filter(Boolean);
  var res=L.filter(function(x){
    if(state.th&&x.s!==state.th)return false;
    var hay=norm([x.t,x.en,x.d].join(' '));
    return words.every(function(w){return hay.indexOf(w)>=0;});});
  document.getElementById('count').textContent=res.length+' terme'+(res.length>1?'s':'')+' sur '+L.length;
  list.innerHTML=res.length?'':'<div class="empty">Aucun terme trouvé. Essaie un autre mot.</div>';
  var last='';
  res.forEach(function(x){
    var l=norm(x.t).charAt(0).toUpperCase();if(!/[A-Z]/.test(l))l='#';
    if(l!==last){var h=document.createElement('div');h.className='letter';h.textContent=l;list.appendChild(h);last=l;}
    var d=document.createElement('div');d.className='card term';
    d.innerHTML='<div class="h"><b>'+hl(x.t,raw)+'</b>'+(x.en&&x.en!=='—'&&x.en!==x.t?'<span class="en">'+hl(x.en,raw)+'</span>':'')+'</div>'+
      '<p class="d">'+hl(x.d,raw)+'</p><div class="meta2"><span>'+esc(x.s)+'</span>'+
      x.p.map(function(p){return '<a href="'+p+'.html">'+esc(PAGES[p]||p)+'</a>';}).join(' · ')+'</div>';
    list.appendChild(d);});
}
q.value=state.q;
q.addEventListener('input',function(){state.q=q.value;render();});
document.addEventListener('keydown',function(e){if(e.key==='/'&&document.activeElement!==q){e.preventDefault();q.focus();}});
render();
(function(){var f=document.getElementById('fab');if(!f)return;function u(){f.classList.toggle('show',window.scrollY>600);}addEventListener('scroll',u,{passive:true});u();})();
</script>
</body>
</html>
'''
open(R+'units/lexique.html','w').write(head+style+headerpart+body+theme_js+js)
