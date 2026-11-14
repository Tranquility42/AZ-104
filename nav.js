/* Menu du site : généré par tools/site.py */
(function(){
var NAV={"tools": [["examen-blanc", "Examen blanc"], ["lexique", "Lexique"], ["commandes", "Mes commandes"]], "sections": [{"t": "1 · Prérequis", "p": [["arm-templates", "Déployer avec des modèles ARM JSON"]], "k": "pre", "i": "📐", "w": ""}, {"t": "2 · Identités et gouvernance", "p": [["entra-vs-adds", "Comparer Microsoft Entra ID et AD DS"], ["entra-domain-services", "Microsoft Entra Domain Services"], ["identites", "Créer, configurer et gérer des identités"], ["architecture", "Composants architecturaux d'Azure"], ["azure-policy", "Initiatives Azure Policy"], ["rbac", "Sécuriser l'accès avec Azure RBAC"]], "k": "id", "i": "🔐", "w": "20–25 %"}, {"t": "3 · Réseaux", "p": [["reseaux-virtuels", "Configurer des réseaux virtuels"], ["nsg", "Groupes de sécurité réseau"], ["azure-dns", "Héberger un domaine sur Azure DNS"], ["peering", "Peering de réseaux virtuels"], ["routes", "Contrôler le trafic avec des routes"], ["load-balancer", "Introduction à Azure Load Balancer"]], "k": "ne", "i": "🌐", "w": "15–20 %"}, {"t": "4 · Stockage", "p": [["comptes-stockage", "Configurer des comptes de stockage"], ["stockage-blob", "Configurer le Stockage Blob"], ["securite-stockage", "Sécurité du Stockage Azure"], ["azure-files", "Azure Files et File Sync"], ["lab07", "🧩 Plan du labo 07 : gérer le stockage"]], "k": "st", "i": "🗄️", "w": "15–20 %"}, {"t": "5 · Calcul", "p": [["machines-virtuelles", "Présentation des machines virtuelles"], ["disponibilite-vm", "Disponibilité des machines virtuelles"], ["plans-app-service", "Plans App Service"], ["app-service", "Configurer App Service"], ["container-instances", "Container Instances"]], "k": "co", "i": "🖥️", "w": "20–25 %"}, {"t": "6 · Supervision et sauvegarde", "p": [["sauvegarde-azure", "Sauvegarde Azure et protection des VM"], ["azure-monitor-vm", "Surveiller les VM avec Azure Monitor"]], "k": "mo", "i": "📊", "w": "10–15 %"}]};
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
