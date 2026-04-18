const forms = document.querySelectorAll('#contact-form');

forms.forEach(form => {
  const errorEl = form.querySelector('[id$="contact-error"]') || form.parentElement.querySelector('.contact__error');
  const submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Client-side validation
    const name = form.querySelector('[name="name"]');
    const email = form.querySelector('[name="email"]');
    const message = form.querySelector('[name="message"]');

    if (!name.value.trim() || !email.value.trim() || !message.value.trim()) {
      showError('Please fill in all fields.', errorEl);
      return;
    }

    if (!isValidEmail(email.value.trim())) {
      showError('Please enter a valid email address.', errorEl);
      return;
    }

    hideError(errorEl);
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending…';

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          name: name.value.trim(),
          email: email.value.trim(),
          message: message.value.trim(),
        }),
      });

      if (response.ok) {
        showSuccess(form);
      } else {
        const data = await response.json();
        showError(data?.errors?.[0]?.message || 'Something went wrong. Please try again.', errorEl);
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send message';
      }
    } catch {
      showError('Network error. Please check your connection and try again.', errorEl);
      submitBtn.disabled = false;
      submitBtn.textContent = 'Send message';
    }
  });
});

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showError(message, errorEl) {
  if (!errorEl) return;
  errorEl.textContent = message;
  errorEl.classList.add('visible');
}

function hideError(errorEl) {
  if (!errorEl) return;
  errorEl.textContent = '';
  errorEl.classList.remove('visible');
}

function showSuccess(form) {
  const successHTML = `
    <div class="contact__success">
      <p class="contact__success-title">Message sent.</p>
      <p class="contact__success-text">Thanks for reaching out — I'll get back to you shortly.</p>
    </div>
  `;
  form.innerHTML = successHTML;
}
