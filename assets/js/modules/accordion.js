// Accordion: one item open at a time; click an open item to close it
function initAccordion(root) {
  const items = [...root.querySelectorAll('.acc__item')];

  const setOpen = (item, open) => {
    item.classList.toggle('is-open', open);
    item.querySelector('.acc__trigger')?.setAttribute('aria-expanded', open);
  };

  items.forEach((item) => {
    item.querySelector('.acc__trigger')?.addEventListener('click', () => {
      const willOpen = !item.classList.contains('is-open');
      items.forEach((other) => setOpen(other, false));
      setOpen(item, willOpen);
    });
  });
}

document.querySelectorAll('[data-accordion]').forEach(initAccordion);
