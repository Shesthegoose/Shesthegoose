// She's the Goose — shared behavior
function bdThanks(form){
  var page = form.closest('.sunday, .foot');
  if(page){ var t = page.querySelector('.thanks') || document.getElementById('bdThanksMsg');
    if(t){ t.classList.add('show'); t.style.display='block'; } }
  setTimeout(function(){ var e=form.querySelector('input[type=email]'); if(e) e.value=''; },400);
}
// condensed masthead bar
(function(){
  var bar=document.getElementById('condensed');
  var nav=document.querySelector('.nav');
  if(!bar||!nav) return;
  var threshold=0, ticking=false;
  function measure(){ threshold = nav.getBoundingClientRect().bottom + window.scrollY; }
  measure(); window.addEventListener('resize', measure);
  function onScroll(){
    if(ticking) return; ticking=true;
    requestAnimationFrame(function(){
      bar.classList.toggle('show', window.scrollY > threshold);
      ticking=false;
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
})();
document.addEventListener('keydown', function(e){
  if(e.key==='Escape'){ var m=document.getElementById('menu'); if(m) m.classList.remove('open'); }
});
// search page
(function(){
  var q=document.getElementById('q'), out=document.getElementById('results');
  if(!q||!out||!window.SEARCH_DATA) return;
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function render(term){
    out.innerHTML='';
    term=term.trim().toLowerCase();
    if(term.length<2) return;
    var hits=window.SEARCH_DATA.filter(function(d){
      return (d.t+' '+d.x+' '+d.k+' '+(d.b||'')).toLowerCase().indexOf(term)>-1;
    }).slice(0,30);
    if(!hits.length){ out.innerHTML='<p class="none">Nothing found for &ldquo;'+esc(term)+'&rdquo;. Try a season, a dish, or a room.</p>'; return; }
    hits.forEach(function(d){
      var row=document.createElement('div'); row.className='r-row';
      row.innerHTML='<a href="'+d.u+'"><span class="k">'+esc(d.k)+'</span><span class="t">'+esc(d.t)+'</span>'+(d.x?'<span class="x">'+esc(d.x)+'</span>':'')+'</a>';
      out.appendChild(row);
    });
  }
  q.addEventListener('input',function(){render(q.value);});
})();
