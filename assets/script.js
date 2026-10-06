// Optional micro-celebration effect (may be sandboxed by Streamlit)
window.addEventListener('celebrate', () => {
  const burst = document.createElement('div');
  burst.style.position = 'fixed';
  burst.style.left = '50%';
  burst.style.top = '10%';
  burst.style.transform = 'translateX(-50%)';
  burst.style.pointerEvents = 'none';
  burst.style.zIndex = 9999;
  for (let i=0; i<40; i++) {
    const s = document.createElement('span');
    s.textContent = '✦';
    s.style.position = 'absolute';
    s.style.fontSize = (Math.random()*18+8)+'px';
    s.style.left = (Math.random()*600-300)+'px';
    s.style.animation = 'fall 1.1s ease-out forwards';
    burst.appendChild(s);
  }
  document.body.appendChild(burst);
  setTimeout(()=> burst.remove(), 1200);
});
