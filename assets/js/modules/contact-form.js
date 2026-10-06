// Contact form: client-side validation with clear messages.
// Not connected to a backend yet (static build) — it says so honestly instead of pretending to send.
document.querySelectorAll('[data-contact-form]').forEach((form) => {
  const status = form.querySelector('.form__status');
  const fields = [...form.querySelectorAll('[required]')];

  const messageFor = (field) => {
    if (field.validity.valueMissing) return 'This field is required.';
    if (field.type === 'email' && field.validity.typeMismatch) return 'Please enter a valid email address.';
    if (field.type === 'tel' && field.validity.patternMismatch) return 'Please enter a valid phone number.';
    return '';
  };

  const validate = (field) => {
    const message = field.checkValidity() ? '' : messageFor(field);
    const error = form.querySelector(`#${field.id}-error`);
    field.setAttribute('aria-invalid', message ? 'true' : 'false');
    if (error) {
      error.textContent = message;
      if (message) field.setAttribute('aria-describedby', error.id);
      else field.removeAttribute('aria-describedby');
    }
    return !message;
  };

  fields.forEach((field) => {
    field.addEventListener('blur', () => validate(field));
    field.addEventListener('input', () => { if (field.getAttribute('aria-invalid') === 'true') validate(field); });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const invalid = fields.filter((field) => !validate(field));
    if (invalid.length) {
      status.className = 'form__status is-error';
      status.textContent = 'Please correct the highlighted fields and try again.';
      invalid[0].focus();
      return;
    }
    // TODO: send the form data to the server / form plugin here, then show a real success message.
    status.className = 'form__status is-info';
    status.textContent = 'This form is not connected yet, so your message was not sent. Please email bulk@ketanorganics.com (bulk orders) or info@ketanorganics.com instead.';
  });
});
