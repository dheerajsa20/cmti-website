// CMTI building drawing: a G+4 frame structure with a tower crane, drawn as an SVG.
// The drawing has five stages, set with data-stage="1".."5":
//   1 setting out   2 footings and starter bars   3 frame and crane
//   4 BIM model overlay   5 finished building with lights on
// [data-autobuild] runs the stages once on page load (the hero);
// [data-stage-btn] buttons drive the interactive section.

(() => {
  const GROUND = 250;
  const LEFT = 104;
  const BAY = 50;
  const BAYS = 4;
  const FLOORS = 5;
  const STOREY = 32;
  const RIGHT = LEFT + BAY * BAYS;
  const TOP = GROUND - STOREY * FLOORS;
  const columns = Array.from({ length: BAYS + 1 }, (_, i) => LEFT + i * BAY);

  function draw() {
    const p = [];
    p.push('<svg viewBox="0 0 420 312" class="building" role="presentation" focusable="false">');

    // Ground line and soil hatching
    p.push(`<g class="b-ground"><path class="draw" pathLength="1" d="M14 ${GROUND}H406"/>`);
    let hatch = '';
    for (let x = 22; x < 406; x += 14) hatch += `M${x} ${GROUND + 4}l-10 10`;
    p.push(`<path class="hatch" d="${hatch}"/></g>`);

    // Stage 1: setting-out grid lines, grid bubbles and level marker
    p.push('<g class="b-setout">');
    columns.forEach((x, i) => {
      p.push(`<path class="dash" style="--i:${i}" d="M${x} ${GROUND + 30}V${TOP - 30}"/>`);
      p.push(`<circle class="bubble" style="--i:${i}" cx="${x}" cy="${GROUND + 40}" r="9"/><text class="bubble-t" style="--i:${i}" x="${x}" y="${GROUND + 43.5}">${String.fromCharCode(65 + i)}</text>`);
    });
    p.push(`<path class="draw" pathLength="1" d="M${LEFT - 34} ${GROUND}V${TOP}M${LEFT - 40} ${GROUND}h12M${LEFT - 40} ${TOP}h12"/>`);
    p.push(`<text class="dim" x="${LEFT - 44}" y="${(GROUND + TOP) / 2}" transform="rotate(-90 ${LEFT - 44} ${(GROUND + TOP) / 2})">G+4</text>`);
    p.push(`<text class="lvl" x="${RIGHT + 18}" y="${GROUND - 4}">±0.00</text>`);
    p.push('</g>');

    // Stage 2: footings and column starter bars
    p.push('<g class="b-footing">');
    columns.forEach((x, i) => {
      p.push(`<rect style="--i:${i}" x="${x - 13}" y="${GROUND + 6}" width="26" height="12"/>`);
      p.push(`<path style="--i:${i}" d="M${x - 4} ${GROUND + 6}v-14M${x + 4} ${GROUND + 6}v-14"/>`);
    });
    p.push('</g>');

    // Stage 3: the frame, floor by floor
    for (let f = 0; f < FLOORS; f++) {
      const y = GROUND - STOREY * (f + 1);
      p.push(`<g class="b-floor" style="--i:${f}">`);
      columns.forEach((x) => p.push(`<rect class="col" x="${x - 3}" y="${y}" width="6" height="${STOREY}"/>`));
      p.push(`<rect class="slab" x="${LEFT - 8}" y="${y - 2}" width="${RIGHT - LEFT + 16}" height="6"/>`);
      for (let b = 0; b < BAYS; b++) {
        p.push(`<rect class="win" style="--w:${f * BAYS + b}" x="${LEFT + b * BAY + 12}" y="${y + 10}" width="${BAY - 24}" height="${STOREY - 18}"/>`);
      }
      p.push('</g>');
    }

    // Tower crane
    const mastX = 352;
    const jibY = TOP - 52;
    let lattice = '';
    for (let y = GROUND; y > jibY + 8; y -= 14) lattice += `M${mastX - 7} ${y}L${mastX + 7} ${y - 14}`;
    p.push('<g class="b-crane">');
    p.push(`<path class="mast" d="M${mastX - 7} ${GROUND}V${jibY}M${mastX + 7} ${GROUND}V${jibY}${lattice}"/>`);
    p.push(`<path class="jib" d="M${LEFT + 20} ${jibY}H${mastX + 44}M${LEFT + 20} ${jibY + 7}H${mastX + 44}M${mastX} ${jibY}L${mastX} ${jibY - 24}L${LEFT + 20} ${jibY}M${mastX} ${jibY - 24}L${mastX + 44} ${jibY}"/>`);
    p.push(`<rect class="weight" x="${mastX + 26}" y="${jibY + 7}" width="16" height="14"/>`);
    p.push(`<rect class="cab" x="${mastX - 22}" y="${jibY + 7}" width="15" height="12"/>`);
    p.push(`<g class="trolley"><rect x="-8" y="${jibY + 7}" width="16" height="5"/><path class="cable" d="M0 ${jibY + 12}V${TOP - 22}"/><path class="hook" d="M-3 ${TOP - 22}h6v4a3 3 0 0 1 -6 0"/><rect class="beam" x="-22" y="${TOP - 15}" width="44" height="5"/></g>`);
    p.push('</g>');

    // Stage 4: BIM model overlay
    p.push('<g class="b-bim">');
    p.push(`<path d="M${LEFT} ${TOP}l18 -14H${RIGHT + 18}V${GROUND - 14}L${RIGHT} ${GROUND}M${RIGHT} ${TOP}l18 -14"/>`);
    p.push(`<rect class="clash" x="${LEFT + BAY * 2 - 9}" y="${GROUND - STOREY * 3 - 9}" width="18" height="18"/>`);
    p.push('</g>');

    // Stage 5: landscaping
    p.push(`<g class="b-finish"><circle cx="${LEFT - 22}" cy="${GROUND - 20}" r="13"/><path d="M${LEFT - 22} ${GROUND}v-10"/><circle cx="${RIGHT + 26}" cy="${GROUND - 16}" r="10"/><path d="M${RIGHT + 26} ${GROUND}v-8"/></g>`);

    p.push('</svg>');
    return p.join('');
  }

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const drawings = [...document.querySelectorAll('[data-building]')];
  for (const el of drawings) el.innerHTML = draw();

  // Hero: run through the stages once, then let the crane idle
  const hero = document.querySelector('[data-autobuild]');
  if (hero) {
    if (reduced) {
      hero.dataset.stage = '5';
    } else {
      const timings = [[1, 150], [2, 900], [3, 1500], [5, 3100]];
      for (const [stage, delay] of timings) setTimeout(() => { hero.dataset.stage = String(stage); }, delay);
      setTimeout(() => hero.classList.add('is-idle'), 4200);
    }
  }

  // Interactive stages
  const panel = document.querySelector('.stages [data-building]');
  const caption = document.querySelector('.stages-caption');
  const buttons = [...document.querySelectorAll('[data-stage-btn]')];
  function setStage(n) {
    if (!panel) return;
    panel.dataset.stage = String(n);
    for (const button of buttons) {
      const on = button.dataset.stageBtn === String(n);
      button.setAttribute('aria-expanded', String(on));
      document.getElementById(button.getAttribute('aria-controls')).hidden = !on;
    }
    const label = buttons[n - 1].textContent.replace(/^\d/, '').trim();
    if (caption) caption.textContent = `Stage ${n} of 5: ${label}`;
  }
  for (const button of buttons) button.addEventListener('click', () => setStage(Number(button.dataset.stageBtn)));

  // Facts in the title block count up once the hero has built
  const counters = document.querySelectorAll('[data-count]');
  if (!reduced) {
    for (const el of counters) {
      const target = Number(el.dataset.count);
      const final = el.textContent;
      el.textContent = '0+';
      const start = performance.now() + 600;
      const tick = (now) => {
        const t = Math.min(Math.max((now - start) / 1400, 0), 1);
        const eased = 1 - Math.pow(1 - t, 3);
        el.textContent = t < 1 ? Math.round(target * eased).toLocaleString('en-IN') + '+' : final;
        if (t < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }
})();
