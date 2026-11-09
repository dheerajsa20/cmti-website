const form = document.querySelector('#enquiry');
const programme = document.querySelector('#programme');

for (const link of document.querySelectorAll('[data-programme]')) {
  link.addEventListener('click', () => {
    programme.value = link.dataset.programme;
  });
}

form?.addEventListener('submit', (event) => {
  event.preventDefault();
  const values = new FormData(form);
  const body = [
    ['Name', values.get('name')],
    ['Email', values.get('email')],
    ['Phone', values.get('phone')],
    ['Organisation', values.get('organisation')],
    ['Programme', values.get('programme')],
    ['Preferred format', values.get('format')],
    ['Training requirements', values.get('message')],
  ].filter(([, value]) => value.trim()).map(([label, value]) => label + ': ' + value.trim()).join('\r\n');
  const subject = encodeURIComponent('CMTI training enquiry – ' + values.get('programme'));
  document.querySelector('#form-status').textContent = 'Send the draft from your email app. If it does not open, email cmtioffice@cmti.co.in directly.';
  window.location.href = 'mailto:cmtioffice@cmti.co.in?subject=' + subject + '&body=' + encodeURIComponent(body);
});

const collegeStrip = document.querySelector('#college-strip');
for (const button of document.querySelectorAll('[data-college-scroll]')) {
  button.addEventListener('click', () => {
    collegeStrip.scrollBy({left: Number(button.dataset.collegeScroll) * collegeStrip.clientWidth});
  });
}

const requestedProgramme = new URLSearchParams(window.location.search).get('programme');
if (programme && [...programme.options].some(option => option.value === requestedProgramme)) {
  programme.value = requestedProgramme;
}

const collegeToggle = document.querySelector('[data-college-toggle]');
if (collegeStrip && collegeToggle) {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let playing = !reducedMotion.matches;
  let previousTime = 0;
  let fraction = 0;
  const firstCopy = collegeStrip.firstElementChild.cloneNode(true);

  for (const item of [...collegeStrip.children]) {
    const copy = item === collegeStrip.firstElementChild ? firstCopy : item.cloneNode(true);
    copy.setAttribute('aria-hidden', 'true');
    collegeStrip.append(copy);
  }

  function updateToggle() {
    collegeToggle.textContent = playing ? 'Pause scrolling' : 'Play scrolling';
  }

  collegeStrip.classList.add('is-looping');
  collegeToggle.hidden = false;
  updateToggle();

  collegeToggle.addEventListener('click', () => {
    playing = !playing;
    updateToggle();
  });

  reducedMotion.addEventListener('change', () => {
    playing = !reducedMotion.matches;
    updateToggle();
  });

  function scrollColleges(time) {
    const elapsed = Math.min(time - previousTime, 50);
    previousTime = time;
    if (playing && !collegeStrip.matches(':hover, :focus-within')) {
      const width = firstCopy.offsetLeft - collegeStrip.firstElementChild.offsetLeft;
      if (width > 0) {
        fraction += elapsed * 0.032;
        const step = Math.floor(fraction);
        fraction -= step;
        if (step) collegeStrip.scrollLeft = (collegeStrip.scrollLeft + step) % width;
      }
    }
    requestAnimationFrame(scrollColleges);
  }

  requestAnimationFrame(scrollColleges);
}
