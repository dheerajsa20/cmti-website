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
// On desktop, hovering one menu closes any other menu opened by click or keyboard
const canHover = window.matchMedia('(hover: hover) and (min-width: 1101px)');
for (const item of document.querySelectorAll('.has-sub')) {
  item.addEventListener('mouseenter', () => { if (canHover.matches) closeSubs(item.querySelector('button')); });
  item.addEventListener('mouseleave', () => { if (canHover.matches) item.querySelector('button').setAttribute('aria-expanded', 'false'); });
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
  nav.style.setProperty('--nav-top', masthead.getBoundingClientRect().bottom + 'px');
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

// Generic tab boards ([data-tabs]): each tab shows the panel it controls
for (const board of document.querySelectorAll('[data-tabs]')) {
  const tabs = [...board.querySelectorAll('[role="tab"]')];
  setupTabs(tabs, (tab) => {
    for (const t of tabs) document.getElementById(t.getAttribute('aria-controls')).hidden = t !== tab;
  });
}

// Training topics: open the clicked topic in a panel placed right after that tile's row
for (const grid of document.querySelectorAll('[data-topic-grid]')) {
  const tiles = [...grid.querySelectorAll('.topic-tile')];
  const panel = grid.querySelector('.topic-panel');
  let current = null;

  const columns = () => getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length;

  function place() {
    if (!current) return;
    const cols = columns();
    const index = tiles.indexOf(current);
    const rowEnd = Math.min(Math.floor(index / cols) * cols + cols - 1, tiles.length - 1);
    tiles[rowEnd].after(panel);
    // Point the panel's arrow at the centre of the chosen tile
    const g = grid.getBoundingClientRect();
    const t = current.getBoundingClientRect();
    panel.style.setProperty('--arrow-x', (t.left - g.left + t.width / 2) + 'px');
  }

  function close() {
    if (!current) return;
    current.setAttribute('aria-expanded', 'false');
    current.classList.remove('is-active');
    panel.hidden = true;
    const was = current;
    current = null;
    return was;
  }

  function open(tile) {
    if (current) { current.setAttribute('aria-expanded', 'false'); current.classList.remove('is-active'); }
    current = tile;
    tile.setAttribute('aria-expanded', 'true');
    tile.classList.add('is-active');
    panel.querySelector('.tp-icon').innerHTML = tile.querySelector('.icon').outerHTML;
    panel.querySelector('.tp-title').textContent = tile.dataset.title;
    panel.querySelector('.tp-desc').textContent = tile.dataset.desc;
    panel.querySelector('.tp-count').textContent = 'Topic ' + (tiles.indexOf(tile) + 1) + ' of ' + tiles.length;
    panel.hidden = false;
    place();
    panel.classList.remove('is-entering');
    void panel.offsetWidth;
    panel.classList.add('is-entering');
    const r = panel.getBoundingClientRect();
    if (r.bottom > innerHeight || r.top < 80) panel.scrollIntoView({ block: 'nearest', behavior: reducedMotion ? 'auto' : 'smooth' });
  }

  for (const tile of tiles) {
    tile.addEventListener('click', () => (tile === current ? close() : open(tile)));
  }
  panel.querySelector('.tp-close').addEventListener('click', () => { const was = close(); was?.focus(); });
  panel.addEventListener('keydown', (event) => { if (event.key === 'Escape') { const was = close(); was?.focus(); } });
  window.addEventListener('resize', place);
}

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

// ----- Logo marquees: continuous scroll, one pause button per group -----
for (const group of document.querySelectorAll('[data-marquee-group]')) {
  const rows = [...group.querySelectorAll('.marquee')];
  const toggle = group.querySelector('.marquee-toggle');
  if (reducedMotion) { toggle?.remove(); continue; }
  for (const row of rows) {
    const track = row.querySelector('.marquee-track');
    for (const item of [...track.children]) {
      const copy = item.cloneNode(true);
      copy.setAttribute('aria-hidden', 'true');
      track.append(copy);
    }
    row.style.setProperty('--marquee-duration', track.children.length * 2.4 + 's');
    row.classList.add('is-running');
  }
  toggle?.addEventListener('click', () => {
    const paused = toggle.getAttribute('aria-pressed') !== 'true';
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.textContent = paused ? 'Play scrolling' : 'Pause scrolling';
    for (const row of rows) row.classList.toggle('is-paused', paused);
  });
}

// ----- Embedded videos: load the YouTube player in place on click -----
for (const button of document.querySelectorAll('[data-embed]')) {
  button.addEventListener('click', () => {
    const iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + button.dataset.embed + '?autoplay=1&rel=0';
    iframe.title = button.dataset.title || 'Video';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    const frame = document.createElement('div');
    frame.className = 'video-embed';
    frame.append(iframe);
    button.replaceWith(frame);
    iframe.focus();
  });
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
  email: 'Enter an email address, for example name@example.com.',
  programme: 'Select the programme you are asking about.',
  message: 'Tell us briefly about your training requirements.',
};
const isValid = (field) => field.name === 'email'
  ? /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value.trim())
  : Boolean(field.value.trim());
function showError(field, text) {
  const error = document.querySelector('#e-' + field.name);
  field.setAttribute('aria-invalid', text ? 'true' : 'false');
  if (error) error.textContent = text;
}
form?.addEventListener('blur', (event) => {
  const field = event.target;
  if (messages[field.name] && isValid(field)) showError(field, '');
}, true);

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  const status = document.querySelector('#form-status');
  let firstInvalid = null;
  for (const name of Object.keys(messages)) {
    const field = form.elements[name];
    const bad = !isValid(field);
    showError(field, bad ? messages[name] : '');
    if (bad && !firstInvalid) firstInvalid = field;
  }
  if (firstInvalid) { status.textContent = ''; firstInvalid.focus(); return; }

  const data = new FormData(form);
  const lines = ['CMTI training enquiry – ' + data.get('programme'), ''];
  for (const [label, key] of [['Name', 'name'], ['Email', 'email'], ['Phone', 'phone'], ['Organisation', 'organisation'], ['Programme', 'programme'], ['Preferred format', 'format']]) {
    const value = (data.get(key) || '').trim();
    if (value) lines.push(label + ': ' + value);
  }
  lines.push('', 'Training requirements: ' + data.get('message').trim());
  const url = 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(lines.join('\n'));
  // Open WhatsApp in a new tab; fall back to the same tab if pop-ups are blocked.
  const opened = window.open(url, '_blank');
  if (opened) opened.opener = null;
  else location.href = url;

  status.textContent = 'WhatsApp opened with your enquiry. Press Send there to deliver it. No WhatsApp? Email ';
  status.append(
    Object.assign(document.createElement('a'), {
      href: 'mailto:cmtioffice@cmti.co.in?subject=' + encodeURIComponent('CMTI training enquiry – ' + data.get('programme')) + '&body=' + encodeURIComponent(lines.join('\n')),
      textContent: 'cmtioffice@cmti.co.in',
    }),
    '.'
  );
});
