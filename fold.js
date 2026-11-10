/* Replie les sections du bas (à partir de « Pièges d'examen ») — fermées par défaut */
(function(){
  var main=document.querySelector('main');if(!main)return;
  var h2s=[].slice.call(main.querySelectorAll(':scope > h2'));
  var start=-1;h2s.forEach(function(h,i){if(start<0&&/^Pi[eè]ges/i.test(h.textContent.trim()))start=i;});
  if(start<0)return;
  var blocks=[];
  h2s.slice(start).forEach(function(h){
    var body=document.createElement('div');body.className='fold-body';body.hidden=true;
    var n=h.nextSibling;
    while(n&&!(n.nodeType===1&&(n.tagName==='H2'||n.matches('nav.pager')))){var nx=n.nextSibling;body.appendChild(n);n=nx;}
    h.parentNode.insertBefore(body,n);
    var btn=document.createElement('button');btn.type='button';btn.className='fold-h';btn.setAttribute('aria-expanded','false');
    var lbl=document.createElement('span');lbl.className='fold-lbl';
    while(h.firstChild)lbl.appendChild(h.firstChild);
    var ch=document.createElement('span');ch.className='chev';ch.setAttribute('aria-hidden','true');ch.textContent='▾';
    btn.appendChild(lbl);btn.appendChild(ch);h.appendChild(btn);h.classList.add('fold');
    function set(o){body.hidden=!o;btn.setAttribute('aria-expanded',o?'true':'false');}
    btn.addEventListener('click',function(){set(body.hidden);});
    blocks.push({h:h,body:body,set:set});
  });
  // Bouton « Tout ouvrir / Tout fermer »
  var all=document.createElement('button');all.type='button';all.className='fold-all';
  function label(){var anyClosed=blocks.some(function(b){return b.body.hidden;});all.textContent=anyClosed?'▾ Tout ouvrir (pièges, quiz, Terraform, lexique…)':'▴ Tout fermer';}
  all.addEventListener('click',function(){var open=blocks.some(function(b){return b.body.hidden;});blocks.forEach(function(b){b.set(open);});label();});
  blocks.forEach(function(b){b.h.querySelector('.fold-h').addEventListener('click',label);});
  blocks[0].h.parentNode.insertBefore(all,blocks[0].h);label();
  // Ouvre la section visée par un lien #ancre (ex. #unite-2, #licences)
  function openHash(){
    if(!location.hash)return;var t;try{t=document.querySelector(location.hash);}catch(e){return;}
    if(!t)return;blocks.forEach(function(b){if(b.h===t||b.h.contains(t)||b.body.contains(t)){b.set(true);label();setTimeout(function(){t.scrollIntoView();},0);}});
  }
  openHash();window.addEventListener('hashchange',openHash);
})();
