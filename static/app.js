const $ = (s) => document.querySelector(s);
const textInput = $('#textInput'), patternInput = $('#patternInput');
const samples = [
  {text:'the quick brown fox jumps over the lazy dog. the fox is quick.', pattern:'fox'},
  {text:'ABABABCABABABCABABABC', pattern:'ABABABC'},
  {text:'mississippi river flows through mississippi. mississippi!', pattern:'issi'},
  {text:'A needle in a haystack is still a needle. Look closely.', pattern:'needle'}
];
const esc = (s) => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function updateCounts(){ $('#textCount').textContent = `${textInput.value.length.toLocaleString()} characters`; $('#patternCount').textContent = `${patternInput.value.length.toLocaleString()} characters`; }
textInput.addEventListener('input', updateCounts); patternInput.addEventListener('input', updateCounts);
$('#sampleBtn').addEventListener('click', () => { const sample=samples[Math.floor(Math.random()*samples.length)]; textInput.value=sample.text; patternInput.value=sample.pattern; updateCounts(); });
function paintText(text, pattern, positions){
  if(!pattern || !positions.length){ $('#visualText').textContent=text || 'Your text will appear here.'; return; }
  const starts = new Set(positions), out=[]; let i=0;
  while(i<text.length){ if(starts.has(i)){ out.push(`<mark>${esc(text.slice(i,i+pattern.length))}</mark>`); i+=pattern.length; } else { out.push(esc(text[i])); i++; } }
  $('#visualText').innerHTML=out.join('');
}
function renderCards(results){
  const colors={naive:'mint',kmp:'blue',rabin_karp:'amber'};
  $('#resultsGrid').innerHTML=results.map((r,i)=>`<article class="result-card ${colors[r.id]}" style="--card-delay:${i*80}ms"><div class="result-card-top"><span class="result-name"><span class="result-dot"></span>${esc(r.name)}</span><span class="result-complexity">${esc(r.complexity)}</span></div><div class="match-count"><strong>${r.count}</strong><span>${r.count===1?'match':'matches'} found</span></div><div class="metric-row"><div class="metric"><span>CHARACTER CHECKS</span><strong>${r.comparisons.toLocaleString()}</strong></div><div class="metric"><span>RUNTIME</span><strong>${r.time_ms.toFixed(4)} <small>ms</small></strong></div></div><div class="result-bottom"><span>SPACE <b>${esc(r.space)}</b></span><span>POSITIONS <b>${r.positions.length?r.positions.join(', '):'—'}</b></span></div></article>`).join('');
}
$('#runBtn').addEventListener('click', async () => {
  const error=$('#errorBox'); error.hidden=true;
  const algorithms=[...document.querySelectorAll('input[name="algorithm"]:checked')].map(x=>x.value);
  if(!algorithms.length){error.textContent='Select at least one algorithm to compare.';error.hidden=false;return;}
  const btn=$('#runBtn'); btn.disabled=true; btn.innerHTML='<span class="spinner"></span> Comparing…';
  try{
    const response=await fetch('/api/compare',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:textInput.value,pattern:patternInput.value,algorithms})});
    const data=await response.json(); if(!response.ok) throw new Error(data.error||'Something went wrong.');
    renderCards(data.results); const all=data.results.flatMap(r=>r.positions); const unique=[...new Set(all)].sort((a,b)=>a-b);
    paintText(textInput.value,patternInput.value,unique);
    $('#matchSummary').textContent=`${unique.length} ${unique.length===1?'match':'matches'} · ${data.text_length.toLocaleString()} characters`;
    $('#visualCaption').textContent=`Searching for “${patternInput.value}” · match positions are zero-based`;
    $('#resultsNote').textContent=`${data.results.length} algorithms · ${unique.length} matches found`;
  }catch(e){error.textContent=e.message;error.hidden=false;}finally{btn.disabled=false;btn.innerHTML='<span class="run-icon">▶</span> Run comparison <span class="button-arrow">↗</span>';}
});
updateCounts();
