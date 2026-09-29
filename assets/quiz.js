/* CCAR-F · componentes reutilizables: Quiz y Recall
   Uso Quiz:   <div class="quiz" data-src="quiz-id"></div>
               <script type="application/json" id="quiz-id">[{q, options:[...], answer:idx, why}]</script>
   Uso Recall: <div class="recall" data-terms="a,b,c" data-prompt="..."></div>
   Las opciones se barajan; las respuestas deben tener el mismo largo (sin pistas de formato). */
(function(){
  const css = `
  .quiz,.recall{font-family:var(--sans);font-size:.88rem;margin:20px 0}
  .q{border:1px solid var(--rule);border-radius:8px;padding:14px 16px;margin:14px 0}
  .q p.stem{font-family:var(--serif);font-size:1rem;margin:0 0 10px}
  .q label{display:block;padding:7px 10px;margin:4px 0;border-radius:6px;border:1px solid transparent;cursor:pointer}
  .q label:hover{border-color:var(--rule)}
  .q input{margin-right:8px}
  .q label.right{background:var(--ok-soft);border-color:var(--ok)}
  .q label.wrong{background:var(--bad-soft);border-color:var(--bad)}
  .q .why{display:none;margin-top:10px;color:var(--muted);font-size:.84rem}
  .q.done .why{display:block}
  .score{font-weight:600;margin-top:10px}
  .recall .res{margin-top:10px}
  .recall .hit{color:var(--ok)} .recall .miss{color:var(--bad)}`;
  const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);
  const shuffle=a=>{for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};

  document.querySelectorAll('.quiz').forEach((root,qi)=>{
    const data=JSON.parse(document.getElementById(root.dataset.src).textContent);
    let answered=0,correct=0;
    const score=document.createElement('div');score.className='score';
    data.forEach((item,i)=>{
      const box=document.createElement('div');box.className='q';
      box.innerHTML=`<p class="stem"><strong>${i+1}.</strong> ${item.q}</p>`;
      shuffle(item.options.map((t,k)=>({t,k}))).forEach(o=>{
        const l=document.createElement('label');
        l.innerHTML=`<input type="radio" name="q${qi}_${i}">${o.t}`;
        l.onclick=()=>{
          if(box.classList.contains('done'))return;
          box.classList.add('done');answered++;
          if(o.k===item.answer){l.classList.add('right');correct++}
          else{l.classList.add('wrong');
            box.querySelectorAll('label').forEach(x=>{if(x.dataset.k==item.answer)x.classList.add('right')})}
          if(answered===data.length)score.textContent=`Resultado: ${correct}/${data.length}. Anotá los errores en errores.md.`;
        };
        l.dataset.k=o.k;box.appendChild(l);
      });
      const why=document.createElement('div');why.className='why';why.innerHTML=item.why;box.appendChild(why);
      root.appendChild(box);
    });
    root.appendChild(score);
  });

  document.querySelectorAll('.recall').forEach(root=>{
    const terms=root.dataset.terms.split(',').map(s=>s.trim());
    root.innerHTML=`<p>${root.dataset.prompt}</p><textarea placeholder="Escribí de memoria, sin mirar arriba..."></textarea>
      <p><button class="primary">Comprobar</button></p><div class="res"></div>`;
    root.querySelector('button').onclick=()=>{
      const txt=root.querySelector('textarea').value.toLowerCase();
      const hits=terms.filter(t=>txt.includes(t.toLowerCase()));
      root.querySelector('.res').innerHTML=`<strong>${hits.length}/${terms.length}</strong> · `+
        terms.map(t=>`<span class="${hits.includes(t)?'hit':'miss'}">${t}</span>`).join(' · ');
    };
  });
})();
