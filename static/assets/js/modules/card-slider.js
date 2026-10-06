// Card slider: native scroll-snap track with prev/next buttons and mouse drag
function initCardSlider(track) {
  const scope = track.closest('[data-slider-scope]') || track.parentElement;
  const prev = scope.querySelector('[data-slider-prev]');
  const next = scope.querySelector('[data-slider-next]');

  const step = () => {
    const card = track.firstElementChild;
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return card ? card.getBoundingClientRect().width + gap : track.clientWidth;
  };
  const maxScroll = () => track.scrollWidth - track.clientWidth;

  const nav = prev?.closest('.slider-nav');

  const update = () => {
    // hide the arrows when every card already fits
    const scrollable = maxScroll() > 2;
    if (nav) nav.hidden = !scrollable;
    track.classList.toggle('is-static', !scrollable);
    if (prev) prev.disabled = track.scrollLeft <= 2;
    if (next) next.disabled = track.scrollLeft >= maxScroll() - 2;
  };

  prev?.addEventListener('click', () => track.scrollBy({ left: -step(), behavior: 'smooth' }));
  next?.addEventListener('click', () => track.scrollBy({ left: step(), behavior: 'smooth' }));
  track.addEventListener('scroll', update, { passive: true });
  window.addEventListener('resize', update);

  // Keyboard
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); track.scrollBy({ left: step(), behavior: 'smooth' }); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); track.scrollBy({ left: -step(), behavior: 'smooth' }); }
  });

  // Mouse drag (touch devices swipe natively)
  let down = false, moved = false, startX = 0, startLeft = 0;
  track.addEventListener('mousedown', (e) => {
    down = true; moved = false;
    startX = e.pageX; startLeft = track.scrollLeft;
  });
  window.addEventListener('mousemove', (e) => {
    if (!down) return;
    const dx = e.pageX - startX;
    if (Math.abs(dx) > 5) { moved = true; track.classList.add('is-dragging'); }
    if (moved) track.scrollLeft = startLeft - dx;
  });
  window.addEventListener('mouseup', () => {
    if (!down) return;
    down = false;
    if (moved) {
      // snap to the nearest card
      const target = Math.round(track.scrollLeft / step()) * step();
      track.classList.remove('is-dragging');
      track.scrollTo({ left: Math.min(target, maxScroll()), behavior: 'smooth' });
    }
  });
  // a drag must not count as a click on the card link
  track.addEventListener('click', (e) => { if (moved) { e.preventDefault(); moved = false; } }, true);
  track.addEventListener('dragstart', (e) => e.preventDefault());

  update();
}

document.querySelectorAll('[data-card-slider]').forEach(initCardSlider);
