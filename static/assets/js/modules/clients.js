// Happy Clients: media carousel (left) + auto-scrolling review wall (right)
function initClients(root) {
  /* ---------- Media carousel ---------- */
  const slides = [...root.querySelectorAll('.clients__slide')];
  const play = root.querySelector('.clients__play');
  let current = 0;

  const stopVideo = (slide) => {
    const video = slide.querySelector('video');
    if (video) video.remove();
  };

  const show = (i) => {
    stopVideo(slides[current]);
    current = (i + slides.length) % slides.length;
    slides.forEach((s, n) => s.classList.toggle('is-active', n === current));
    // play button only for slides that have a video
    if (play) play.hidden = !slides[current].dataset.video;
  };

  root.querySelector('.clients__arrow--prev')?.addEventListener('click', () => show(current - 1));
  root.querySelector('.clients__arrow--next')?.addEventListener('click', () => show(current + 1));

  play?.addEventListener('click', () => {
    const slide = slides[current];
    const video = document.createElement('video');
    video.src = slide.dataset.video;
    video.controls = true;
    video.autoplay = true;
    video.playsInline = true;
    slide.appendChild(video);
    play.hidden = true;
  });

  if (slides.length) show(0);

  /* ---------- Review wall ---------- */
  const track = root.querySelector('.clients__track');
  const dotsWrap = root.querySelector('.clients__dots');
  const rows = [...root.querySelectorAll('.clients__row')];
  if (!track || !rows.length) return;

  const isVertical = () => getComputedStyle(track).flexDirection === 'column';
  const visibleRows = 3;
  const steps = Math.max(rows.length - visibleRows + 1, 1); // scroll positions
  let step = 0;
  let timer = null;

  const dots = Array.from({ length: steps }, (_, i) => {
    const dot = document.createElement('button');
    dot.type = 'button';
    dot.className = 'clients__dot';
    dot.tabIndex = -1;
    dot.addEventListener('click', () => { goTo(i); restart(); });
    dotsWrap?.appendChild(dot);
    return dot;
  });

  const setActive = (i) => {
    step = i;
    dots.forEach((d, n) => d.classList.toggle('is-active', n === i));
  };

  // Move the rows with a transform (no scroll container, so page scrolling is never trapped)
  function goTo(i) {
    const target = (i + steps) % steps;
    const rowStep = rows[1] ? rows[1].offsetTop - rows[0].offsetTop : 0;
    const last = rows[rows.length - 1];
    const contentHeight = last.offsetTop + last.offsetHeight - rows[0].offsetTop;
    const maxOffset = Math.max(contentHeight - track.clientHeight, 0);
    track.style.setProperty('--offset', `${Math.min(rowStep * target, maxOffset)}px`);
    setActive(target);
  }

  // Keyboard: up / down arrows when the review wall is focused
  track.addEventListener('keydown', (e) => {
    if (!isVertical()) return;
    if (e.key === 'ArrowDown') { e.preventDefault(); goTo(Math.min(step + 1, steps - 1)); restart(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); goTo(Math.max(step - 1, 0)); restart(); }
  });

  // Keep the position correct when the layout changes size
  window.addEventListener('resize', () => { if (isVertical()) goTo(step); });

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const stop = () => clearInterval(timer);
  const start = () => {
    stop();
    if (reduceMotion || steps < 2) return;
    timer = setInterval(() => { if (isVertical()) goTo(step + 1); }, 4000);
  };
  const restart = () => { stop(); start(); };

  track.addEventListener('mouseenter', stop);
  track.addEventListener('mouseleave', start);
  track.addEventListener('focusin', stop);
  track.addEventListener('focusout', start);
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));

  setActive(0);
  start();
}

document.querySelectorAll('[data-clients]').forEach(initClients);
