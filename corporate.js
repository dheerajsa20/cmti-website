const motionButton = document.querySelector('#client-motion');
const marquee = motionButton.parentElement;
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

function setPaused(paused) {
  marquee.classList.toggle('is-paused', paused);
  motionButton.textContent = paused ? 'Play scrolling' : 'Pause scrolling';
}

setPaused(reducedMotion.matches);
motionButton.addEventListener('click', () => setPaused(!marquee.classList.contains('is-paused')));
reducedMotion.addEventListener('change', event => setPaused(event.matches));
