// Blog: category filter on the listing page + share buttons on single posts

// ----- Category filter -----
document.querySelectorAll('[data-blog]').forEach((root) => {
  const buttons = [...root.querySelectorAll('.blog__filter')];
  const cards = [...root.querySelectorAll('.post-card')];
  const empty = root.querySelector('.blog__empty');

  const apply = (cat) => {
    let shown = 0;
    cards.forEach((card) => {
      const match = cat === 'all' || card.dataset.cat === cat;
      card.hidden = !match;
      if (match) shown += 1;
    });
    if (empty) empty.hidden = shown > 0;
    buttons.forEach((b) => {
      const active = b.dataset.filter === cat;
      b.classList.toggle('is-active', active);
      b.setAttribute('aria-pressed', active);
    });
  };

  buttons.forEach((b) => b.addEventListener('click', () => apply(b.dataset.filter)));

  // allow links like blogs.html#cat=hydrosol
  const fromHash = new URLSearchParams(location.hash.slice(1)).get('cat');
  apply(buttons.some((b) => b.dataset.filter === fromHash) ? fromHash : 'all');
});

// ----- Share buttons -----
document.querySelectorAll('[data-share]').forEach((el) => {
  const url = encodeURIComponent(location.href);
  const title = encodeURIComponent(document.title);
  const targets = {
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${url}`,
    x: `https://twitter.com/intent/tweet?url=${url}&text=${title}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${url}`,
    whatsapp: `https://wa.me/?text=${title}%20${url}`,
  };
  const type = el.dataset.share;

  if (type === 'copy') {
    el.addEventListener('click', async () => {
      const status = el.parentElement.querySelector('.post-share__status');
      try {
        await navigator.clipboard.writeText(location.href);
        if (status) status.textContent = 'Link copied';
      } catch {
        if (status) status.textContent = 'Could not copy the link';
      }
    });
  } else if (targets[type]) {
    el.href = targets[type];
    el.target = '_blank';
    el.rel = 'noopener';
  }
});
