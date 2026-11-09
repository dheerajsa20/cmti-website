// CMTI site behaviour: navigation, hero finder, motion, video dialog and WhatsApp enquiries.
const WHATSAPP_NUMBER = '918884422179';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
document.documentElement.classList.add('js');

// ----- Header shadow once the page scrolls -----
const masthead = document.querySelector('.masthead');
const onScroll = () => masthead?.classList.toggle('is-scrolled', window.scrollY > 8);
onScroll();
window.addEventListener('scroll', onScroll, { passive: true });

// ----- Navigation: dropdowns and mobile menu -----
const nav = document.querySelector('#site-nav');
const menuToggle = document.querySelector('.menu-toggle');
const subButtons = [...document.querySelectorAll('.has-sub > button')];

function closeSubs(except) {
  for (const button of subButtons) if (button !== except) button.setAttribute('aria-expanded', 'false');
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
  menuToggle.querySelector('.menu-label').textContent = open ? 'Close' : 'Menu';
  document.body.classList.toggle('nav-open', open);
}
menuToggle?.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
document.addEventListener('click', (event) => { if (!event.target.closest('.has-sub')) closeSubs(); });
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  const openSub = subButtons.find((b) => b.getAttribute('aria-expanded') === 'true');
  if (openSub) { closeSubs(); openSub.focus(); return; }
  if (nav?.classList.contains('is-open')) { setMenu(false); menuToggle.focus(); }
});
nav?.addEventListener('click', (event) => { if (event.target.closest('a')) { setMenu(false); closeSubs(); } });

const here = location.pathname.split('/').pop() || 'index.html';
for (const link of document.querySelectorAll('.site-nav a[href]')) {
  if (link.getAttribute('href') === here) link.setAttribute('aria-current', 'page');
}

// ----- Tabs helper (hero finder and course journey) -----
function setupTabs(tabs, onSelect) {
  function select(tab, focus) {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
    }
    if (focus) tab.focus();
    onSelect(tab);
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab, false));
    tab.addEventListener('keydown', (event) => {
      const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      if (event.key in keys) {
        event.preventDefault();
        select(tabs[(i + keys[event.key] + tabs.length) % tabs.length], true);
      } else if (event.key === 'Home') { event.preventDefault(); select(tabs[0], true); }
      else if (event.key === 'End') { event.preventDefault(); select(tabs[tabs.length - 1], true); }
    });
  });
  return select;
}

// Hero "I am..." finder
const finderTabs = [...document.querySelectorAll('.finder [role="tab"]')];
setupTabs(finderTabs, (tab) => {
  for (const t of finderTabs) document.getElementById(t.getAttribute('aria-controls')).hidden = t !== tab;
});

// Course journey: tabs that also advance on their own until the visitor takes over
const journey = document.querySelector('[data-journey]');
if (journey) {
  const tabs = [...journey.querySelectorAll('[role="tab"]')];
  const media = journey.querySelector('.journey-media');
  const img = media.querySelector('img');
  const playButton = media.querySelector('.journey-play');
  const STEP_MS = 6000;
  let timer = null;
  let playing = !reducedMotion;
  media.style.setProperty('--journey-ms', STEP_MS + 'ms');

  const showImage = (tab) => {
    media.setAttribute('aria-labelledby', tab.id);
    if (img.getAttribute('src') === tab.dataset.img) return;
    img.classList.add('is-swapping');
    setTimeout(() => {
      img.src = tab.dataset.img;
      img.alt = tab.dataset.alt;
      img.onload = () => img.classList.remove('is-swapping');
    }, reducedMotion ? 0 : 250);
  };

  const restartProgress = () => {
    media.classList.remove('is-playing');
    void media.offsetWidth; // restart the CSS progress animation
    if (playing) media.classList.add('is-playing');
  };

  const schedule = () => {
    clearTimeout(timer);
    restartProgress();
    if (!playing) return;
    timer = setTimeout(() => {
      const current = tabs.findIndex((t) => t.getAttribute('aria-selected') === 'true');
      select(tabs[(current + 1) % tabs.length], false, true);
    }, STEP_MS);
  };

  const setPlaying = (value) => {
    playing = value;
    playButton.setAttribute('aria-pressed', String(value));
    playButton.textContent = value ? 'Pause tour' : 'Play tour';
    schedule();
  };

  const baseSelect = setupTabs(tabs, (tab) => showImage(tab));
  function select(tab, focus, auto) {
    baseSelect(tab, focus);
    if (!auto) setPlaying(false); else schedule();
  }
  tabs.forEach((tab) => tab.addEventListener('click', () => setPlaying(false)));
  playButton.addEventListener('click', () => setPlaying(!playing));

  // Only run the tour while the section is on screen
  if (!reducedMotion && 'IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && playing) schedule();
      else clearTimeout(timer);
    }, { threshold: 0.4 }).observe(media);
  }
}

// ----- Client logo marquee -----
const marquee = document.querySelector('.marquee');
if (marquee && !reducedMotion) {
  const track = marquee.querySelector('.marquee-track');
  for (const item of [...track.children]) {
    const copy = item.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    track.append(copy);
  }
  marquee.style.setProperty('--marquee-duration', track.children.length * 2.2 + 's');
  marquee.classList.add('is-running');
  const toggle = document.querySelector('.marquee-toggle');
  toggle?.addEventListener('click', () => {
    const paused = marquee.classList.toggle('is-paused');
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.textContent = paused ? 'Play logos' : 'Pause logos';
  });
} else {
  document.querySelector('.marquee-toggle')?.remove();
}

// ----- Reveal on scroll and number count-up -----
function countUp(el) {
  const target = Number(el.dataset.count);
  const final = el.textContent;
  if (reducedMotion || !target) return;
  const start = performance.now();
  const tick = (now) => {
    const t = Math.min((now - start) / 1600, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = t < 1 ? Math.round(target * eased).toLocaleString('en-IN') + '+' : final;
    if (t < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

if ('IntersectionObserver' in window) {
  const revealer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const el = entry.target;
      el.classList.add('is-visible');
      // Hand control back to the element's own hover transitions once revealed
      el.addEventListener('transitionend', () => el.classList.remove('reveal', 'is-visible'), { once: true });
      revealer.unobserve(el);
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  // Stagger items that sit in the same grid
  const groups = new Map();
  for (const el of document.querySelectorAll('.reveal')) {
    const index = groups.get(el.parentElement) || 0;
    groups.set(el.parentElement, index + 1);
    el.style.setProperty('--delay', Math.min(index, 5) * 90 + 'ms');
    revealer.observe(el);
  }

  const counter = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) { countUp(entry.target); counter.unobserve(entry.target); }
    }
  }, { threshold: 0.6 });
  for (const el of document.querySelectorAll('[data-count]')) counter.observe(el);
} else {
  for (const el of document.querySelectorAll('.reveal')) el.classList.remove('reveal');
}

// ----- Student video dialog -----
const dialog = document.querySelector('.video-dialog');
if (dialog) {
  const frame = dialog.querySelector('.video-frame');
  let opener = null;
  for (const card of document.querySelectorAll('[data-video]')) {
    card.addEventListener('click', () => {
      opener = card;
      frame.innerHTML = '';
      const iframe = document.createElement('iframe');
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + card.dataset.video + '?autoplay=1&rel=0';
      iframe.title = card.dataset.title;
      iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      frame.append(iframe);
      dialog.showModal();
    });
  }
  const close = () => dialog.close();
  dialog.querySelector('.video-close').addEventListener('click', close);
  dialog.addEventListener('click', (event) => { if (event.target === dialog) close(); });
  dialog.addEventListener('close', () => { frame.innerHTML = ''; opener?.focus(); });
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
  const error = document.querySelector('#e-' + field.name);
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
  if (firstInvalid) { status.textContent = ''; firstInvalid.focus(); return; }

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
  const opened = window.open(url, '_blank');
  if (opened) opened.opener = null;
  else location.href = url;

  status.textContent = 'WhatsApp opened with your enquiry. Press Send there to deliver it. No WhatsApp? Email ';
  status.append(
    Object.assign(document.createElement('a'), {
      href: 'mailto:cmtioffice@cmti.co.in?subject=' + encodeURIComponent('Training enquiry: ' + data.get('programme')) + '&body=' + encodeURIComponent(lines.join('\n')),
      textContent: 'cmtioffice@cmti.co.in',
    }),
    '.'
  );
});
