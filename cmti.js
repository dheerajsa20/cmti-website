// CMTI page script for the redesigned pages (redesign-2026).
// The kit's system.js, motion.js and layout.js run the nav, the hover layer, the hero's entrance and the moments.
// This file adds only what is CMTI's own: Lenis smooth scrolling, the click-to-load YouTube films and the
// enquiry form that opens a WhatsApp draft.
(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ----- Lenis: gentle smoothing on the wheel only; native touch; off under reduced motion -----
  let lenis = null;
  const headerOffset = () => -((document.querySelector('.nav')?.offsetHeight || 72) + 16);
  if (!reduced && typeof window.Lenis === 'function') {
    lenis = new window.Lenis({ lerp: 0.12, smoothWheel: true, syncTouch: false, anchors: false });
    const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
    // stop the page while the phone menu sheet is open
    const toggle = document.querySelector('.nav__toggle');
    if (toggle) new MutationObserver(() => (toggle.getAttribute('aria-expanded') === 'true' ? lenis.stop() : lenis.start()))
      .observe(toggle, { attributes: true, attributeFilter: ['aria-expanded'] });
  }

  // In-page links scroll under the fixed bar; the target then takes focus so keyboard users land there.
  document.addEventListener('click', (event) => {
    const a = event.target.closest('a[href*="#"]');
    if (!a || event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
    const url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname || !url.hash || url.hash === '#') return;
    const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if (!target) return;
    event.preventDefault();
    const land = () => {
      if (!target.hasAttribute('tabindex')) target.setAttribute('tabindex', '-1');
      target.focus({ preventScroll: true });
    };
    history.pushState(null, '', url.hash);
    if (a.classList.contains('skip-link') || !lenis) {
      target.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
      land();
    } else {
      lenis.scrollTo(target, { offset: target.id === 'top' ? 0 : headerOffset(), onComplete: land });
    }
  });

  // ----- YouTube films: the poster stays until a click, then the player loads in place -----
  const player = (id, title) => {
    const f = document.createElement('iframe');
    f.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    f.title = title;
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    return f;
  };
  // the hero's play control is a link to the film on YouTube; with scripts on, the film plays in the frame
  for (const link of document.querySelectorAll('[data-yt-film]')) {
    link.addEventListener('click', (event) => {
      const host = link.closest('[data-film-host]');
      if (!host) return;
      event.preventDefault();
      const f = player(link.dataset.ytFilm, link.dataset.title);
      host.append(f);
      const over = host.querySelector('.hero__over');
      if (over) over.hidden = true;
      f.focus();
    });
  }
  for (const button of document.querySelectorAll('[data-yt]')) {
    button.addEventListener('click', () => {
      const f = player(button.dataset.yt, button.dataset.title);
      button.replaceWith(f);
      f.focus();
    });
  }

  // ----- Enquiry: the kit checks the fields; a valid form opens WhatsApp with the enquiry written out -----
  const form = document.getElementById('enquiry-form');
  if (form) {
    const programme = new URLSearchParams(location.search).get('programme');
    const select = form.querySelector('#programme');
    if (programme && select) {
      const match = [...select.options].find((o) => o.text === programme);
      if (match) match.selected = true;
    }
    form.addEventListener('submit', (event) => {
      const fields = [...form.elements].filter((el) => el.matches('input, select, textarea'));
      if (!fields.every((el) => el.checkValidity())) return; // system.js shows the errors
      event.preventDefault();
      const v = (name) => (form.elements[name]?.value || '').trim();
      const lines = [
        'Training enquiry from the CMTI website',
        `Name: ${v('name')}`,
        `Phone: ${v('phone')}`,
        `Email: ${v('email')}`,
        v('organisation') && `Organisation: ${v('organisation')}`,
        `Programme: ${v('programme')}`,
        v('message') && `Training needs: ${v('message')}`,
      ].filter(Boolean);
      const url = `https://wa.me/${form.action.split('wa.me/')[1].replace(/\D/g, '')}?text=${encodeURIComponent(lines.join('\n'))}`;
      const status = form.querySelector('[data-form-status]');
      const win = window.open(url, '_blank');
      if (win) win.opener = null; else location.href = url;
      if (status) status.textContent = 'WhatsApp is open with your enquiry. Press send there to reach CMTI.';
    });
  }
})();
