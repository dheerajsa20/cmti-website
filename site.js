// CMTI site behaviour: navigation, programme prefill and WhatsApp enquiries.
const WHATSAPP_NUMBER = '918884422179';

// ----- Navigation: dropdowns and mobile menu -----
const nav = document.querySelector('#site-nav');
const menuToggle = document.querySelector('.menu-toggle');
const subButtons = [...document.querySelectorAll('.has-sub > button')];

function closeSubs(except) {
  for (const button of subButtons) {
    if (button !== except) button.setAttribute('aria-expanded', 'false');
  }
}

for (const button of subButtons) {
  button.addEventListener('click', () => {
    const open = button.getAttribute('aria-expanded') === 'true';
    closeSubs(button);
    button.setAttribute('aria-expanded', String(!open));
  });
}

function setMenu(open) {
  if (!nav || !menuToggle) return;
  nav.classList.toggle('is-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.textContent = open ? 'Close' : 'Menu';
  document.body.classList.toggle('nav-open', open);
}

menuToggle?.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));

document.addEventListener('click', (event) => {
  if (!event.target.closest('.has-sub')) closeSubs();
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  const openSub = subButtons.find((b) => b.getAttribute('aria-expanded') === 'true');
  if (openSub) { closeSubs(); openSub.focus(); return; }
  if (nav?.classList.contains('is-open')) { setMenu(false); menuToggle.focus(); }
});

// Close the mobile menu after following an in-page link
nav?.addEventListener('click', (event) => {
  if (event.target.closest('a')) { setMenu(false); closeSubs(); }
});

// Mark the current page in the navigation
const here = location.pathname.split('/').pop() || 'index.html';
for (const link of document.querySelectorAll('.site-nav a[href]')) {
  const target = link.getAttribute('href');
  if (target === here) link.setAttribute('aria-current', 'page');
}

// ----- Enquiry form: prefill the programme -----
const form = document.querySelector('#enquiry');
const programme = document.querySelector('#programme');

function choose(value) {
  if (!programme || !value) return;
  const option = [...programme.options].find((o) => o.value === value || o.text === value);
  if (option) programme.value = option.value;
}

for (const link of document.querySelectorAll('[data-programme]')) {
  link.addEventListener('click', () => choose(link.dataset.programme));
}
choose(new URLSearchParams(location.search).get('programme'));

// ----- Enquiry form: validate, then open WhatsApp with the message -----
const messages = {
  name: 'Enter your name so we know who to reply to.',
  programme: 'Choose the programme you are asking about.',
  message: 'Tell us briefly what training you need.',
};

function showError(field, text) {
  const error = document.querySelector('#e-' + (field.id === 'programme' ? 'programme' : field.name));
  field.setAttribute('aria-invalid', text ? 'true' : 'false');
  if (error) error.textContent = text;
}

form?.addEventListener('blur', (event) => {
  const field = event.target;
  if (messages[field.name] && field.value.trim()) showError(field, '');
}, true);

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  const status = document.querySelector('#form-status');
  let firstInvalid = null;

  for (const name of Object.keys(messages)) {
    const field = form.elements[name];
    const empty = !field.value.trim();
    showError(field, empty ? messages[name] : '');
    if (empty && !firstInvalid) firstInvalid = field;
  }
  if (firstInvalid) {
    status.textContent = '';
    firstInvalid.focus();
    return;
  }

  const data = new FormData(form);
  const organisation = data.get('organisation').trim();
  const lines = [
    'Hello CMTI, I have a training enquiry.',
    '',
    'Name: ' + data.get('name').trim(),
    ...(organisation ? ['Organisation: ' + organisation] : []),
    'Programme: ' + data.get('programme'),
    'Preferred format: ' + data.get('format'),
    '',
    data.get('message').trim(),
  ];

  const url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
  // Open WhatsApp in a new tab; fall back to the same tab if pop-ups are blocked.
  // ('noopener' in the features string would make window.open return null.)
  const opened = window.open(url, '_blank');
  if (opened) opened.opener = null;
  else location.href = url;

  status.innerHTML = '';
  status.append(
    'WhatsApp opened with your enquiry. Press Send there to deliver it. No WhatsApp? Email ',
    Object.assign(document.createElement('a'), {
      href: 'mailto:cmtioffice@cmti.co.in?subject=' + encodeURIComponent('Training enquiry: ' + data.get('programme')) + '&body=' + encodeURIComponent(lines.join('\n')),
      textContent: 'cmtioffice@cmti.co.in',
    }),
    '.'
  );
});
