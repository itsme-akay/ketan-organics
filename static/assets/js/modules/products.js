// Products: category filter + search on the listing, and the "Request a Quote" modal

// ----- Filter + search -----
document.querySelectorAll('[data-products]').forEach((root) => {
  const cards = [...root.querySelectorAll('.product-card')];
  const buttons = [...root.querySelectorAll('.blog__filter')];
  const search = root.querySelector('[data-product-search]');
  const empty = root.querySelector('.products__empty');
  const count = root.querySelector('.products__count');
  let cat = 'all';

  const apply = () => {
    const term = (search?.value || '').trim().toLowerCase();
    let shown = 0;
    cards.forEach((card) => {
      const match = (cat === 'all' || card.dataset.cat === cat)
        && (!term || card.dataset.search.includes(term));
      card.hidden = !match;
      if (match) shown += 1;
    });
    if (empty) empty.hidden = shown > 0;
    if (count) count.textContent = `Showing ${shown} of ${cards.length} products`;
    buttons.forEach((b) => {
      const active = b.dataset.filter === cat;
      b.classList.toggle('is-active', active);
      b.setAttribute('aria-pressed', active);
    });
  };

  buttons.forEach((b) => b.addEventListener('click', () => { cat = b.dataset.filter; apply(); }));
  search?.addEventListener('input', apply);

  // allow links like products.html#cat=grains
  const fromHash = new URLSearchParams(location.hash.slice(1)).get('cat');
  if (buttons.some((b) => b.dataset.filter === fromHash)) cat = fromHash;
  apply();
});

// ----- Request a Quote modal -----
const modal = document.querySelector('[data-quote-modal]');
if (modal) {
  const nameEl = modal.querySelector('[data-quote-product]');
  const hidden = modal.querySelector('input[name="product"]');
  const productRow = modal.querySelector('.quote-modal__product');

  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-quote]');
    if (!trigger) return;
    e.preventDefault();
    const product = trigger.dataset.quote;
    if (nameEl) nameEl.textContent = product || 'General enquiry';
    if (hidden) hidden.value = product || '';
    if (productRow) productRow.hidden = !product;
    // clear any earlier status message
    const status = modal.querySelector('.form__status');
    if (status) { status.textContent = ''; status.className = 'form__status'; }
    modal.showModal();
    modal.querySelector('input:not([type="hidden"])')?.focus();
  });

  modal.querySelector('.quote-modal__close')?.addEventListener('click', () => modal.close());
  // click on the dark backdrop closes the modal
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.close(); });
}
