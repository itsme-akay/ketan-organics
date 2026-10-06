// Hero carousel: autoplay, dots, arrows, swipe, keyboard
function initHeroSlider(root) {
  const track = root.querySelector('.hero-slider__track');
  const slides = [...root.querySelectorAll('.hero-slide')];
  const dotsWrap = root.querySelector('.hero-slider__dots');
  const delay = Number(root.dataset.autoplay) || 5000;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (slides.length < 2) return;

  let index = 0;
  let timer = null;

  const dots = slides.map((_, i) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'hero-slider__dot';
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', () => { goTo(i); restart(); });
    dotsWrap.appendChild(dot);
    return dot;
  });

  function goTo(i) {
    index = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
    slides.forEach((s, n) => {
      const active = n === index;
      s.setAttribute('aria-hidden', !active);
      s.querySelectorAll('a').forEach((a) => (a.tabIndex = active ? 0 : -1));
    });
    dots.forEach((d, n) => {
      d.classList.toggle('is-active', n === index);
      d.setAttribute('aria-current', n === index ? 'true' : 'false');
    });
  }

  const next = () => goTo(index + 1);
  const prev = () => goTo(index - 1);
  const stop = () => clearInterval(timer);
  const start = () => { if (!reduceMotion) { stop(); timer = setInterval(next, delay); } };
  const restart = () => { stop(); start(); };

  root.querySelector('.hero-slider__arrow--next')?.addEventListener('click', () => { next(); restart(); });
  root.querySelector('.hero-slider__arrow--prev')?.addEventListener('click', () => { prev(); restart(); });

  // Pause on hover / focus
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);
  root.addEventListener('focusin', stop);
  root.addEventListener('focusout', start);
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));

  // Keyboard
  root.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { next(); restart(); }
    if (e.key === 'ArrowLeft') { prev(); restart(); }
  });

  // Swipe
  let startX = 0;
  root.addEventListener('touchstart', (e) => { startX = e.touches[0].clientX; stop(); }, { passive: true });
  root.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 40) (dx < 0 ? next : prev)();
    start();
  });

  goTo(0);
  start();
}

document.querySelectorAll('[data-hero-slider]').forEach(initHeroSlider);
