import sys,json
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from bank import Q
from coach import H
R=__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__)))+'/'
cmd=open(R+'units/commandes.html').read()
head=cmd[:cmd.index('<style>')].replace('<title>Mes commandes Azure</title>','<title>Examen blanc AZ-104</title>')
headerpart=cmd[cmd.index('</style>')+8:cmd.index('<main class="wrap">')]
theme_js=cmd[cmd.index('<script>'):cmd.index("var TOOLS=")]
css=r'''<style>
.modes{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));margin-top:12px}
.mode{all:unset;box-sizing:border-box;cursor:pointer;display:block;padding:16px;border-radius:14px;border:1.5px solid var(--line);background:var(--surface)}
.mode:hover,.mode:focus-visible{border-color:var(--cloud)}
.mode b{display:block;font-size:17px}.mode span{display:block;font-size:14px;color:var(--muted);margin-top:4px}
.chipsel{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.f{all:unset;cursor:pointer;font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--muted)}
.f[aria-pressed="true"]{background:var(--cloud);border-color:var(--cloud);color:#fff}
.btn{all:unset;box-sizing:border-box;cursor:pointer;font-weight:700;font-size:15px;padding:11px 18px;border-radius:12px;background:var(--cloud);color:#fff;text-align:center}
.btn.sec{background:var(--surface);color:var(--text);border:1.5px solid var(--line)}
.btn.warn{background:var(--onprem)}
.btn:focus-visible,.f:focus-visible,.opt:focus-visible{outline:2px solid var(--cloud);outline-offset:2px}
.btn[disabled]{opacity:.45;cursor:default}
.bar{position:sticky;top:61px;z-index:6;background:var(--bg);padding:10px 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--line)}
.timer{font-variant-numeric:tabular-nums;font-weight:700;font-size:18px;padding:6px 12px;border-radius:10px;background:var(--cloud-soft)}
.timer.low{background:var(--onprem-soft);color:var(--onprem)}
.prog{flex:1;min-width:120px;font-size:14px;color:var(--muted)}
.qcard{margin-top:14px;padding:18px}
.qmeta{display:flex;flex-wrap:wrap;gap:6px 10px;font-size:13px;color:var(--muted);margin-bottom:8px}
.dom{font-weight:700;color:var(--cloud)}
.qtext{font-size:17px;line-height:1.5;margin:0 0 12px}
.hint{font-size:13px;color:var(--muted);margin:-6px 0 10px}
.opts{display:grid;gap:8px}
.opt{all:unset;box-sizing:border-box;cursor:pointer;display:grid;grid-template-columns:28px minmax(0,1fr);gap:10px;align-items:start;padding:12px 14px;border-radius:12px;border:1.5px solid var(--line);background:var(--surface);font-size:15.5px;line-height:1.45}
.opt .k{width:26px;height:26px;border-radius:50%;border:1.5px solid var(--line);display:grid;place-items:center;font-size:13px;font-weight:700}
.opt.m .k{border-radius:6px}
.opt[aria-checked="true"]{border-color:var(--cloud);background:var(--cloud-soft)}
.opt[aria-checked="true"] .k{background:var(--cloud);border-color:var(--cloud);color:#fff}
.nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.nav .btn{flex:1;min-width:90px;white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(38px,1fr));gap:6px;margin-top:14px}
.cell{all:unset;cursor:pointer;box-sizing:border-box;height:38px;border-radius:9px;border:1.5px solid var(--line);display:grid;place-items:center;font-size:13px;font-weight:700;background:var(--surface);position:relative}
.cell.done{background:var(--cloud-soft);border-color:var(--cloud)}
.cell.cur{outline:2.5px solid var(--text);outline-offset:1px}
.cell.flag::after{content:'';position:absolute;top:3px;right:3px;width:7px;height:7px;border-radius:50%;background:var(--onprem)}
.legend{font-size:12.5px;color:var(--muted);margin-top:6px}
.score{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
.big{font-size:44px;font-weight:800;line-height:1}
.pass{font-weight:700;padding:5px 12px;border-radius:999px}
.pass.ok{background:var(--ok-soft);color:var(--ok)}.pass.ko{background:var(--onprem-soft);color:var(--onprem)}
.drow{display:grid;grid-template-columns:minmax(0,1fr) 70px;gap:4px 10px;align-items:center;font-size:14px;margin-top:8px}
.track{grid-column:1/-1;height:8px;border-radius:99px;background:var(--surface-2);overflow:hidden}
.track i{display:block;height:100%;background:var(--cloud)}
.rev{padding:14px 16px;margin-top:10px}
.rev.bad{border-left:4px solid var(--onprem)}.rev.good{border-left:4px solid var(--ok)}
.rev ul{margin:8px 0 0;padding-left:18px;font-size:14.5px}
.rev li.right{color:var(--ok);font-weight:600}.rev li.wrongpick{color:var(--onprem);text-decoration:line-through}
.rev .ex{font-size:14px;margin:8px 0 0}
.hist{width:100%;border-collapse:collapse;font-size:14px}
.hist th,.hist td{padding:8px 6px;border-bottom:1px solid var(--line);text-align:left}
.hist td.n{font-variant-numeric:tabular-nums}
.spark{display:flex;align-items:flex-end;gap:4px;height:80px;margin-top:10px;border-bottom:1px dashed var(--line);position:relative}
.spark i{flex:1;max-width:26px;border-radius:4px 4px 0 0;background:var(--cloud)}
.spark i.ko{background:var(--onprem)}
.spark .line{position:absolute;left:0;right:0;border-top:2px dashed var(--ok)}
.stats{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14px;color:var(--muted);margin-top:8px}
.stats b{color:var(--text)}
.mode.one{border-style:dashed;border-color:color-mix(in srgb,var(--tf) 45%,var(--line))}
.mode.one b::before{content:'🧭 '}
.setup{margin-top:12px;border-color:var(--tf)}
.setup h3{margin:0 0 4px}
.setup .lab{font-size:13px;font-weight:700;color:var(--muted);margin:12px 0 0}
.tools2{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.tools2 .btn{padding:9px 14px;font-size:14px}
.coach{margin-top:12px;padding:12px 14px;border-radius:12px;font-size:15px;line-height:1.5}
.coach.hintbox{background:var(--warn-soft);border:1px solid color-mix(in srgb,var(--warn) 35%,transparent)}
.coach.ok{background:var(--ok-soft);border:1px solid color-mix(in srgb,var(--ok) 35%,transparent)}
.coach.ko{background:var(--onprem-soft);border:1px solid color-mix(in srgb,var(--onprem) 35%,transparent)}
.coach.tip{background:var(--tf-soft);border:1px solid color-mix(in srgb,var(--tf) 35%,transparent)}
.coach b.t{display:block;font-size:13px;letter-spacing:.02em;text-transform:uppercase;margin-bottom:2px}
.opt.right{border-color:var(--ok);background:var(--ok-soft)}
.opt.right .k{background:var(--ok);border-color:var(--ok);color:#fff}
.opt.wrong{border-color:var(--onprem);background:var(--onprem-soft)}
.opt.wrong .k{background:var(--onprem);border-color:var(--onprem);color:#fff}
.opt[disabled]{cursor:default}
.pscore{font-weight:700;font-variant-numeric:tabular-nums}
[hidden]{display:none!important}
</style>
'''
body=r'''<main class="wrap">
  <nav class="crumbs" aria-label="Fil d'Ariane"><a class="crumb-home" href="../index.html">🏠 Accueil</a><span class="sep">›</span><span class="here">Examen blanc</span></nav>

  <!-- ACCUEIL -->
  <section id="v-home">
    <h1>Examen blanc AZ-104</h1>
    <p class="lede">Des questions originales au format de l'examen : mises en situation, réponses multiples, séries « La solution atteint-elle l'objectif ? ». Les domaines sont tirés selon les poids officiels. Score sur 1000, réussite à 700.</p>
    <div class="card" id="resume" hidden style="margin-top:14px;border-color:var(--cloud)">
      <h3 style="margin-top:0">⏸️ Un examen est en cours</h3>
      <p id="resumeTxt" style="font-size:14px;margin:0 0 10px"></p>
      <div class="nav" style="margin-top:0"><button class="btn" id="bResume" type="button">Reprendre</button><button class="btn sec" id="bDrop" type="button">Abandonner</button></div>
    </div>
    <h2>Choisir un examen</h2>
    <div class="modes" id="modes"></div>
    <div class="card setup" id="setup" hidden>
      <h3>🧭 Une question à la fois</h3>
      <p style="font-size:14px;margin:0;color:var(--muted)">Sans pression : tu réponds, tu peux demander un indice ou ouvrir le résumé du cours, puis tu vois la correction et une astuce d'examen.</p>
      <p class="lab">Domaine</p><div class="chipsel" id="pDom"></div>
      <p class="lab">Chrono</p><div class="chipsel" id="pTime"></div>
      <div class="nav"><button class="btn" id="bPGo" type="button">Commencer</button><button class="btn sec" id="bPCancel" type="button">Annuler</button></div>
    </div>
    <div class="card" style="margin-top:12px">
      <b style="font-size:15px">🎯 Par domaine : 15 questions, 30 min</b>
      <div class="chipsel" id="domsel"></div>
    </div>
    <div class="note" style="margin-top:14px"><b>Le vrai examen :</b> 40 à 60 questions, <b>100 minutes</b>, score mis à l'échelle sur 1000, réussite à <b>700</b>. Il y a aussi des <b>études de cas</b>, des glisser-déposer et des zones à cliquer, que ce site ne reproduit pas. Les questions <b>« Oui / Non »</b> d'une série ne permettent pas de revenir en arrière dans le vrai examen. Ici, une question à plusieurs réponses compte seulement si <b>toutes</b> les bonnes sont cochées.</div>

    <h2>Historique</h2>
    <div id="histBox"></div>
  </section>

  <!-- EXAMEN -->
  <section id="v-exam" hidden>
    <div class="bar">
      <span class="timer" id="timer" role="timer" aria-live="off">--:--</span>
      <span class="prog" id="prog"></span>
      <button class="btn sec" id="bGrid" type="button" style="padding:8px 12px;font-size:14px">Vue d'ensemble</button>
    </div>
    <div class="card qcard" id="qcard"></div>
    <div class="nav">
      <button class="btn sec" id="bPrev" type="button">← Préc.</button>
      <button class="btn sec" id="bFlag" type="button">🚩 Revoir</button>
      <button class="btn" id="bNext" type="button">Suivante →</button>
    </div>
    <div id="gridBox" hidden>
      <div class="grid" id="grid"></div>
      <p class="legend">Bleu = répondue · point orange = à revoir · contour = question actuelle</p>
    </div>
    <div class="card" style="margin-top:14px" id="endBox">
      <p id="endTxt" style="margin:0 0 10px;font-size:14px"></p>
      <button class="btn warn" id="bEnd" type="button" style="width:100%">Terminer l'examen</button>
    </div>
  </section>

  <!-- UNE A LA FOIS -->
  <section id="v-one" hidden>
    <div class="bar">
      <span class="timer" id="pTimer" hidden>--:--</span>
      <span class="prog" id="pProg"></span>
      <button class="btn sec" id="bPStop" type="button" style="padding:8px 12px;font-size:14px">Terminer</button>
    </div>
    <div class="card qcard" id="pCard"></div>
    <div class="tools2" id="pTools">
      <button class="btn sec" id="bHint" type="button">💡 Indice</button>
      <a class="btn sec" id="bPage" target="_blank" rel="noopener">📖 Chercher dans le résumé</a>
      <a class="btn sec" href="lexique.html" target="_blank" rel="noopener">🔤 Lexique</a>
    </div>
    <div id="pHint"></div>
    <div id="pFeed"></div>
    <div class="nav"><button class="btn" id="bCheck" type="button">Valider</button><button class="btn" id="bPNext" type="button" hidden>Question suivante →</button></div>
  </section>

  <!-- BILAN UNE A LA FOIS -->
  <section id="v-onres" hidden>
    <h1>Bilan de l'entraînement</h1>
    <div class="card" style="margin-top:12px"><div class="score"><span class="big" id="oScore"></span></div><div class="stats" id="oStats"></div></div>
    <h2>À retravailler</h2>
    <div id="oRev"></div>
    <div class="nav"><button class="btn" id="bOAgain" type="button">Continuer à s'entraîner</button><button class="btn sec" id="bOHome" type="button">Retour aux examens</button></div>
  </section>

  <!-- RESULTATS -->
  <section id="v-res" hidden>
    <h1>Résultat</h1>
    <div class="card" style="margin-top:12px">
      <div class="score"><span class="big" id="rScore"></span><span class="pass" id="rPass"></span></div>
      <div class="stats" id="rStats"></div>
    </div>
    <h2>Par domaine</h2>
    <div class="card" id="rDom"></div>
    <h2>Correction</h2>
    <div class="chipsel" id="revFilter"></div>
    <div id="rRev"></div>
    <div class="nav"><button class="btn" id="bAgain" type="button">Nouvel examen</button><a class="btn sec" href="../index.html">Sommaire</a></div>
  </section>

  <footer>Questions originales rédigées d'après les modules résumés sur ce site et le plan officiel de l'examen AZ-104. Elles ne viennent pas de l'examen réel.</footer>
  <a class="fab-home" id="fab" href="../index.html" aria-label="Retour au sommaire">☰ Sommaire</a>
</main>
'''
assert len(H)==len(Q)
data=[{'d':d,'t':t,'q':q,'o':o,'a':a,'e':e,'p':p,'h':H[i][0],'x':H[i][1]} for i,(d,t,q,o,a,e,p) in enumerate(Q)]
js='var Q='+json.dumps(data,ensure_ascii=False)+';\n'+r'''
var DOM={id:'Identités et gouvernance',st:'Stockage',co:'Calcul',ne:'Réseaux virtuels',mo:'Supervision et sauvegarde'};
var DOMW={id:'20–25 %',st:'15–20 %',co:'20–25 %',ne:'15–20 %',mo:'10–15 %'};
var MODES={
  full:{n:'Examen complet',q:50,min:100,mix:{id:12,st:9,co:12,ne:10,mo:7},desc:'50 questions · 100 min · comme le vrai'},
  half:{n:'Demi-examen',q:25,min:50,mix:{id:6,st:5,co:6,ne:5,mo:3},desc:'25 questions · 50 min'},
  quick:{n:'Rapide',q:10,min:20,mix:{id:2,st:2,co:2,ne:2,mo:2},desc:'10 questions · 20 min'}
};
var K={run:'exam-run',hist:'exam-hist',seen:'exam-seen',one:'exam-one',pref:'exam-one-pref'};
function load(k,d){try{var v=JSON.parse(localStorage.getItem(k));return v==null?d:v;}catch(e){return d;}}
function save(k,v){try{localStorage.setItem(k,JSON.stringify(v));}catch(e){}}
function del(k){try{localStorage.removeItem(k);}catch(e){}}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
function fmt(s){s=Math.max(0,Math.round(s));var m=Math.floor(s/60),x=s%60;return m+':'+(x<10?'0':'')+x;}
var $=function(id){return document.getElementById(id);};
var run=null,cur=0,tick=null;

function pick(mix){
  var seen=load(K.seen,{}),ids=[];
  Object.keys(mix).forEach(function(d){
    var pool=[];Q.forEach(function(q,i){if(q.d===d)pool.push(i);});
    shuffle(pool);pool.sort(function(a,b){return (seen[a]||0)-(seen[b]||0);});
    ids=ids.concat(pool.slice(0,mix[d]));
  });
  return shuffle(ids);
}
function start(modeKey,dom){
  var m=MODES[modeKey],mix=m?m.mix:{},name,mins;
  if(dom){mix={};mix[dom]=15;name='Domaine : '+DOM[dom];mins=30;}else{name=m.n;mins=m.min;}
  var ids=pick(mix);
  run={name:name,ids:ids,ord:ids.map(function(i){var o=Q[i].o.map(function(_,k){return k;});return Q[i].t==='y'?o:shuffle(o);}),
       ans:ids.map(function(){return [];}),flag:ids.map(function(){return false;}),start:Date.now(),end:Date.now()+mins*60000,mins:mins};
  cur=0;save(K.run,run);show('exam');
}
function show(v){
  ['home','exam','res','one','onres'].forEach(function(x){$('v-'+x).hidden=x!==v;});
  scrollTo(0,0);
  clearInterval(tick);
  if(v==='exam'){renderQ();tick=setInterval(time,1000);time();}
  if(v==='home')home();
}
function time(){
  var left=(run.end-Date.now())/1000;
  $('timer').textContent='⏱ '+fmt(left);
  $('timer').classList.toggle('low',left<300);
  if(left<=0)finish(true);
}
function renderQ(){
  var i=run.ids[cur],q=Q[i],multi=q.t==='m',answered=run.ans.filter(function(a){return a.length;}).length;
  $('prog').textContent='Question '+(cur+1)+' / '+run.ids.length+' · '+answered+' répondue'+(answered>1?'s':'');
  var h='<div class="qmeta"><span class="dom">'+DOM[q.d]+'</span>'+(q.t==='y'?'<span>Série : la solution atteint-elle l\'objectif ?</span>':'')+(run.flag[cur]?'<span>🚩 à revoir</span>':'')+'</div>'+
    '<p class="qtext">'+esc(q.q)+'</p>'+(multi?'<p class="hint">Plusieurs réponses possibles : coche toutes les bonnes.</p>':'')+
    '<div class="opts" role="'+(multi?'group':'radiogroup')+'">';
  run.ord[cur].forEach(function(k,n){
    var on=run.ans[cur].indexOf(k)>=0;
    h+='<button type="button" class="opt'+(multi?' m':'')+'" role="'+(multi?'checkbox':'radio')+'" aria-checked="'+on+'" data-k="'+k+'"><span class="k">'+'ABCDEF'[n]+'</span><span>'+esc(q.o[k])+'</span></button>';
  });
  $('qcard').innerHTML=h+'</div>';
  [].forEach.call($('qcard').querySelectorAll('.opt'),function(b){b.onclick=function(){
    var k=+b.dataset.k,a=run.ans[cur];
    if(multi){var p=a.indexOf(k);if(p>=0)a.splice(p,1);else a.push(k);}else run.ans[cur]=[k];
    save(K.run,run);renderQ();};});
  $('bPrev').disabled=cur===0;
  $('bNext').textContent=cur===run.ids.length-1?'Fin':'Suiv. →';
  $('bNext').disabled=cur===run.ids.length-1;
  $('bFlag').textContent=run.flag[cur]?'🚩 Retirer':'🚩 Revoir';
  var g=$('grid');g.innerHTML='';
  run.ids.forEach(function(_,n){var c=document.createElement('button');c.type='button';
    c.className='cell'+(run.ans[n].length?' done':'')+(run.flag[n]?' flag':'')+(n===cur?' cur':'');
    c.textContent=n+1;c.setAttribute('aria-label','Question '+(n+1));c.onclick=function(){cur=n;renderQ();scrollTo(0,0);};g.appendChild(c);});
  var left=run.ids.length-answered,fl=run.flag.filter(Boolean).length;
  $('endTxt').textContent=(left?left+' question'+(left>1?'s':'')+' sans réponse. ':'Toutes les questions ont une réponse. ')+(fl?fl+' marquée'+(fl>1?'s':'')+' à revoir.':'');
  confirmArm=false;$('bEnd').textContent='Terminer l\'examen';
}
var confirmArm=false;
$('bPrev').onclick=function(){if(cur>0){cur--;renderQ();}};
$('bNext').onclick=function(){if(cur<run.ids.length-1){cur++;renderQ();scrollTo(0,0);}};
$('bFlag').onclick=function(){run.flag[cur]=!run.flag[cur];save(K.run,run);renderQ();};
$('bGrid').onclick=function(){$('gridBox').hidden=!$('gridBox').hidden;};
$('bEnd').onclick=function(){if(!confirmArm){confirmArm=true;$('bEnd').textContent='Confirmer : terminer et corriger';return;}finish(false);};
document.addEventListener('keydown',function(e){
  if($('v-exam').hidden||e.target.tagName==='INPUT')return;
  if(e.key==='ArrowRight')$('bNext').click();else if(e.key==='ArrowLeft')$('bPrev').click();
  else if(/^[a-fA-F]$/.test(e.key)){var b=$('qcard').querySelectorAll('.opt')['abcdef'.indexOf(e.key.toLowerCase())];if(b)b.click();}
});

function isRight(i,a){var g=Q[i].a;return a.length===g.length&&g.every(function(x){return a.indexOf(x)>=0;});}
var last=null;
function finish(timeout){
  clearInterval(tick);
  var dom={},ok=0,seen=load(K.seen,{});
  run.ids.forEach(function(i,n){var d=Q[i].d;dom[d]=dom[d]||[0,0];dom[d][1]++;if(isRight(i,run.ans[n])){dom[d][0]++;ok++;}seen[i]=(seen[i]||0)+1;});
  save(K.seen,seen);
  var sec=Math.min((Date.now()-run.start)/1000,run.mins*60),score=Math.round(ok/run.ids.length*1000);
  var rec={date:Date.now(),name:run.name,score:score,ok:ok,n:run.ids.length,sec:Math.round(sec),dom:dom,timeout:timeout};
  var hist=load(K.hist,[]);hist.push(rec);save(K.hist,hist);
  last={run:run,rec:rec};del(K.run);
  results(timeout);
}
var revMode='all';
function results(timeout){
  show('res');
  var r=last.rec;
  $('rScore').textContent=r.score+' / 1000';
  $('rPass').className='pass '+(r.score>=700?'ok':'ko');$('rPass').textContent=r.score>=700?'✅ Réussi (700 requis)':'❌ Pas encore (700 requis)';
  $('rStats').innerHTML='<span><b>'+r.ok+'</b> / '+r.n+' bonnes réponses</span><span>Temps : <b>'+fmt(r.sec)+'</b></span><span>'+esc(r.name)+'</span>'+(timeout?'<span><b>⏰ Temps écoulé</b></span>':'');
  var h='';Object.keys(DOM).forEach(function(d){if(!r.dom[d])return;var c=r.dom[d],p=Math.round(c[0]/c[1]*100);
    h+='<div class="drow"><span>'+DOM[d]+' <span style="color:var(--muted);font-size:12.5px">('+DOMW[d]+' de l\'examen)</span></span><b style="text-align:right">'+c[0]+'/'+c[1]+'</b><div class="track"><i style="width:'+p+'%;'+(p<70?'background:var(--onprem)':'')+'"></i></div></div>';});
  $('rDom').innerHTML=h+'<p style="font-size:13px;color:var(--muted);margin:10px 0 0">En orange : sous 70 %, à retravailler en priorité.</p>';
  var fs=$('revFilter');fs.innerHTML='';
  [['all','Toutes'],['bad','Erreurs seulement'],['flag','Marquées à revoir']].forEach(function(x){var b=document.createElement('button');b.type='button';b.className='f';b.textContent=x[1];
    b.setAttribute('aria-pressed',revMode===x[0]);b.onclick=function(){revMode=x[0];results(timeout);};fs.appendChild(b);});
  var rv='';
  last.run.ids.forEach(function(i,n){
    var q=Q[i],a=last.run.ans[n],good=isRight(i,a);
    if(revMode==='bad'&&good)return;if(revMode==='flag'&&!last.run.flag[n])return;
    rv+='<div class="card rev '+(good?'good':'bad')+'"><div class="qmeta"><b>'+(good?'✅':'❌')+' Question '+(n+1)+'</b><span class="dom">'+DOM[q.d]+'</span>'+(a.length?'':'<span>sans réponse</span>')+'</div>'+
      '<p style="margin:0;font-size:15px">'+esc(q.q)+'</p><ul>';
    last.run.ord[n].forEach(function(k){var right=q.a.indexOf(k)>=0,picked=a.indexOf(k)>=0;
      rv+='<li class="'+(right?'right':(picked?'wrongpick':''))+'">'+esc(q.o[k])+(right?' ✓':'')+(picked&&right?' (ton choix)':'')+'</li>';});
    rv+='</ul><p class="ex">💡 '+esc(q.e)+' <a href="'+q.p+'.html">Revoir la page</a></p></div>';
  });
  $('rRev').innerHTML=rv||'<p style="color:var(--muted)">Rien à afficher pour ce filtre.</p>';
}
$('bAgain').onclick=function(){show('home');};

function home(){
  var m=$('modes');m.innerHTML='';
  Object.keys(MODES).forEach(function(k){var b=document.createElement('button');b.type='button';b.className='mode';
    b.innerHTML='<b>'+MODES[k].n+'</b><span>'+MODES[k].desc+'</span>';b.onclick=function(){start(k);};m.appendChild(b);});
  var o=document.createElement('button');o.type='button';o.className='mode one';
  o.innerHTML='<b>Une question à la fois</b><span>Chrono au choix · indice · résumé à portée de main · astuce d\'examen</span>';
  o.onclick=function(){$('setup').hidden=false;setupUI();$('setup').scrollIntoView({behavior:'smooth',block:'center'});};m.appendChild(o);
  var op=load(K.one,null);if(op&&op.done<op.ids.length&&op.done>0){o.querySelector('span').textContent='En cours : '+op.ok+' / '+op.done+' bonnes · clique pour continuer';
    o.onclick=function(){one=op;show('one');renderOne();};}
  var ds=$('domsel');ds.innerHTML='';
  Object.keys(DOM).forEach(function(d){var b=document.createElement('button');b.type='button';b.className='f';b.textContent=DOM[d];b.onclick=function(){start(null,d);};ds.appendChild(b);});
  var r=load(K.run,null);
  if(r&&r.end>Date.now()){$('resume').hidden=false;var n=r.ans.filter(function(a){return a.length;}).length;
    $('resumeTxt').textContent=r.name+' · '+n+' / '+r.ids.length+' répondues · '+fmt((r.end-Date.now())/1000)+' restantes';
    $('bResume').onclick=function(){run=r;cur=0;show('exam');};
    $('bDrop').onclick=function(){del(K.run);home();};}
  else{if(r){run=r;finish(true);return;}$('resume').hidden=true;}
  hist();
}
var clearArm=false;
function hist(){
  var H=load(K.hist,[]),box=$('histBox');
  if(!H.length){box.innerHTML='<p style="color:var(--muted);font-size:14px">Aucun examen pour l\'instant. Ton historique s\'affichera ici (gardé dans ce navigateur).</p>';return;}
  var best=Math.max.apply(null,H.map(function(x){return x.score;})),avg=Math.round(H.reduce(function(s,x){return s+x.score;},0)/H.length),
      pass=H.filter(function(x){return x.score>=700;}).length;
  var dom={};H.forEach(function(x){Object.keys(x.dom).forEach(function(d){dom[d]=dom[d]||[0,0];dom[d][0]+=x.dom[d][0];dom[d][1]+=x.dom[d][1];});});
  var weak=Object.keys(dom).sort(function(a,b){return dom[a][0]/dom[a][1]-dom[b][0]/dom[b][1];})[0];
  var last20=H.slice(-20),h='<div class="card"><div class="stats"><span>Examens : <b>'+H.length+'</b></span><span>Moyenne : <b>'+avg+'</b></span><span>Meilleur : <b>'+best+'</b></span><span>Réussis : <b>'+pass+'</b></span>'+
    (weak?'<span>Domaine le plus faible : <b>'+DOM[weak]+'</b> ('+Math.round(dom[weak][0]/dom[weak][1]*100)+' %)</span>':'')+'</div>'+
    '<div class="spark" aria-label="Scores des 20 derniers examens"><span class="line" style="bottom:70%"></span>'+
    last20.map(function(x){return '<i class="'+(x.score<700?'ko':'')+'" style="height:'+Math.max(4,x.score/10)+'%" title="'+x.score+'"></i>';}).join('')+
    '</div><p style="font-size:12.5px;color:var(--muted);margin:4px 0 0">20 derniers examens · ligne verte = 700</p></div>';
  h+='<div class="tablewrap" style="margin-top:10px"><table class="hist"><thead><tr><th>Date</th><th>Examen</th><th>Score</th><th>Bonnes</th><th>Temps</th></tr></thead><tbody>';
  H.slice().reverse().forEach(function(x){var d=new Date(x.date);
    h+='<tr><td class="n">'+d.toLocaleDateString('fr-CA')+' '+d.toLocaleTimeString('fr-CA',{hour:'2-digit',minute:'2-digit'})+'</td><td>'+esc(x.name)+'</td><td class="n"><b style="color:var('+(x.score>=700?'--ok':'--onprem')+')">'+x.score+'</b></td><td class="n">'+x.ok+'/'+x.n+'</td><td class="n">'+fmt(x.sec)+(x.timeout?' ⏰':'')+'</td></tr>';});
  h+='</tbody></table></div><button class="btn sec" id="bClear" type="button" style="margin-top:10px">Effacer l\'historique</button>';
  box.innerHTML=h;
  $('bClear').onclick=function(){if(!clearArm){clearArm=true;this.textContent='Confirmer : tout effacer';return;}del(K.hist);del(K.seen);clearArm=false;hist();};
}
/* ---------- UNE QUESTION A LA FOIS ---------- */
var one=null,pTick=null,pref=load(K.pref,{dom:'all',time:0});
function chips(box,items,val,cb){box.innerHTML='';items.forEach(function(x){var b=document.createElement('button');b.type='button';b.className='f';b.textContent=x[1];
  b.setAttribute('aria-pressed',String(x[0]===val));b.onclick=function(){cb(x[0]);};box.appendChild(b);});}
function setupUI(){
  chips($('pDom'),[['all','Tous les domaines']].concat(Object.keys(DOM).map(function(d){return [d,DOM[d]];})),pref.dom,function(v){pref.dom=v;save(K.pref,pref);setupUI();});
  chips($('pTime'),[[0,'Sans chrono'],[90,'1 min 30 / question'],[120,'2 min / question (rythme du vrai)']],pref.time,function(v){pref.time=v;save(K.pref,pref);setupUI();});
}
$('bPCancel').onclick=function(){$('setup').hidden=true;};
$('bPGo').onclick=function(){
  var seen=load(K.seen,{}),pool=[];Q.forEach(function(q,i){if(pref.dom==='all'||q.d===pref.dom)pool.push(i);});
  shuffle(pool);pool.sort(function(a,b){return (seen[a]||0)-(seen[b]||0);});
  one={ids:pool,done:0,ok:0,miss:[],time:pref.time,dom:pref.dom};newQ();save(K.one,one);$('setup').hidden=true;show('one');renderOne();};
function newQ(){var i=one.ids[one.done],q=Q[i],o=q.o.map(function(_,k){return k;});one.cur={ord:q.t==='y'?o:shuffle(o),ans:[],hint:false,checked:false,end:one.time?Date.now()+one.time*1000:0};}
function renderOne(){
  clearInterval(pTick);
  var c=one.cur,i=one.ids[one.done],q=Q[i],multi=q.t==='m';
  $('pProg').innerHTML='Question <b>'+(one.done+1)+'</b> / '+one.ids.length+(one.done?' · <span class="pscore">'+one.ok+' / '+one.done+' bonnes</span>':'');
  var h='<div class="qmeta"><span class="dom">'+DOM[q.d]+'</span>'+(q.t==='y'?'<span>Série : la solution atteint-elle l\'objectif ?</span>':'')+'</div>'+
    '<p class="qtext">'+esc(q.q)+'</p>'+(multi?'<p class="hint">Plusieurs réponses possibles : coche toutes les bonnes.</p>':'')+'<div class="opts">';
  c.ord.forEach(function(k,n){var on=c.ans.indexOf(k)>=0,cls='';
    if(c.checked){if(q.a.indexOf(k)>=0)cls=' right';else if(on)cls=' wrong';}
    h+='<button type="button" class="opt'+(multi?' m':'')+cls+'" role="'+(multi?'checkbox':'radio')+'" aria-checked="'+on+'" data-k="'+k+'"'+(c.checked?' disabled':'')+'><span class="k">'+'ABCDEF'[n]+'</span><span>'+esc(q.o[k])+'</span></button>';});
  $('pCard').innerHTML=h+'</div>';
  if(!c.checked)[].forEach.call($('pCard').querySelectorAll('.opt'),function(b){b.onclick=function(){var k=+b.dataset.k;
    if(multi){var p=c.ans.indexOf(k);if(p>=0)c.ans.splice(p,1);else c.ans.push(k);}else c.ans=[k];save(K.one,one);renderOne();};});
  $('bPage').href=q.p+'.html';
  $('bHint').hidden=c.checked||c.hint;
  $('pHint').innerHTML=c.hint&&!c.checked?'<div class="coach hintbox"><b class="t">💡 Indice</b>'+esc(q.h)+'</div>':'';
  if(c.checked){var good=isRight(i,c.ans);
    $('pFeed').innerHTML='<div class="coach '+(good?'ok':'ko')+'"><b class="t">'+(good?'✅ Bonne réponse':(c.ans.length?'❌ Pas tout à fait':'⏰ Temps écoulé'))+'</b>'+esc(q.e)+' <a href="'+q.p+'.html" target="_blank" rel="noopener">Revoir la page</a></div>'+
      '<div class="coach tip"><b class="t">🎯 Astuce d\'examen</b>'+esc(q.x)+'</div>';}
  else $('pFeed').innerHTML='';
  $('bCheck').hidden=c.checked;$('bCheck').disabled=!c.ans.length;
  $('bPNext').hidden=!c.checked;$('bPNext').textContent=one.done+1>=one.ids.length?'Voir le bilan':'Question suivante →';
  var t=$('pTimer');t.hidden=!c.end||c.checked;
  if(c.end&&!c.checked){pTime();pTick=setInterval(pTime,1000);}
}
function pTime(){var left=(one.cur.end-Date.now())/1000;$('pTimer').textContent='⏱ '+fmt(left);$('pTimer').classList.toggle('low',left<30);if(left<=0)check();}
function check(){var c=one.cur;if(c.checked)return;clearInterval(pTick);c.checked=true;var i=one.ids[one.done];
  var seen=load(K.seen,{});seen[i]=(seen[i]||0)+1;save(K.seen,seen);
  if(isRight(i,c.ans))one.ok++;else one.miss.push(i);save(K.one,one);renderOne();
  $('pFeed').scrollIntoView({behavior:'smooth',block:'nearest'});}
$('bCheck').onclick=check;
$('bHint').onclick=function(){one.cur.hint=true;save(K.one,one);renderOne();};
$('bPNext').onclick=function(){one.done++;if(one.done>=one.ids.length){oneEnd();return;}newQ();save(K.one,one);renderOne();scrollTo(0,0);};
$('bPStop').onclick=function(){if(one.cur.checked)one.done++;oneEnd();};
function oneEnd(){clearInterval(pTick);var o=one;del(K.one);show('onres');
  var n=o.done,p=n?Math.round(o.ok/n*100):0;
  $('oScore').textContent=n?p+' %':'—';
  $('oStats').innerHTML='<span><b>'+o.ok+'</b> / '+n+' bonnes réponses</span><span>'+(o.dom==='all'?'Tous les domaines':esc(DOM[o.dom]))+'</span>'+(o.time?'<span>Chrono : '+o.time+' s / question</span>':'<span>Sans chrono</span>');
  $('oRev').innerHTML=o.miss.length?o.miss.map(function(i){var q=Q[i];return '<div class="card rev bad"><div class="qmeta"><span class="dom">'+DOM[q.d]+'</span></div><p style="margin:0;font-size:15px">'+esc(q.q)+'</p>'+
    '<p class="ex">✓ <b>'+q.a.map(function(k){return esc(q.o[k]);}).join(' + ')+'</b></p><p class="ex">🎯 '+esc(q.x)+' <a href="'+q.p+'.html">Revoir la page</a></p></div>';}).join(''):'<p style="color:var(--muted)">Aucune erreur. Bravo !</p>';}
$('bOAgain').onclick=function(){show('home');$('setup').hidden=false;setupUI();};
$('bOHome').onclick=function(){show('home');};
document.addEventListener('keydown',function(e){
  if($('v-one').hidden||e.target.tagName==='INPUT'||e.ctrlKey||e.metaKey||e.altKey)return;
  if(e.key==='Enter'){e.preventDefault();if(!$('bCheck').hidden&&!$('bCheck').disabled)check();else if(!$('bPNext').hidden)$('bPNext').click();}
  else if(/^[a-fA-F]$/.test(e.key)&&!one.cur.checked){var b=$('pCard').querySelectorAll('.opt')['abcdef'.indexOf(e.key.toLowerCase())];if(b)b.click();}
  else if(e.key==='h'||e.key==='H'){if(!$('bHint').hidden)$('bHint').click();}
});
show('home');
(function(){var f=document.getElementById('fab');if(!f)return;function u(){f.classList.toggle('show',window.scrollY>600);}addEventListener('scroll',u,{passive:true});u();})();
</script>
</body>
</html>
'''
open(R+'units/examen-blanc.html','w').write(head+css+headerpart+body+theme_js+js)
print('ok')
