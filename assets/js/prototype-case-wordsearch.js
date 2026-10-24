// PROTOTYPE — throwaway. Word-search case hero; ?variant=A|B|C|D switches layout.
// Question it answers: which layout makes the hover word search read as an optional mini game
// that still tells the case (problem, decisions, trade-off, result)?

const VARIANTS = {
  A: { name: 'Side panel', cols: 14, rows: 8 },
  B: { name: 'Band', cols: 24, rows: 6 },
  C: { name: 'Callouts', cols: 12, rows: 12 },
  D: { name: 'Band + callouts', cols: 24, rows: 7, mobile: { cols: 12, rows: 12 } },
};
const CALLOUT_VARIANTS = ['C', 'D'];
const KEYS = Object.keys(VARIANTS);
const REVEAL_RADIUS = 1.5; // in cells
const NOISE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

const params = new URLSearchParams(location.search);
const variant = KEYS.includes(params.get('variant')) ? params.get('variant') : 'D';
const isMobile = matchMedia('(max-width: 768px)').matches;
const { cols, rows } = (isMobile && VARIANTS[variant].mobile) || VARIANTS[variant];

const header = document.querySelector('.wsh');
const grid = header.querySelector('.wsh__grid');
const count = header.querySelector('.wsh__count');
const revealBtn = header.querySelector('.wsh__reveal');
const items = [...header.querySelectorAll('.wsh__item')];
const prefersReducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

header.classList.add(`wsh--${variant}`);
grid.style.setProperty('--cols', cols);
grid.style.setProperty('--rows', rows);

// ---------- Seeded placement so the puzzle is stable between reloads ----------
function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function place(seed) {
  const rand = mulberry32(seed);
  const board = Array.from({ length: rows }, () => Array(cols).fill(null));
  const words = items
    .map(li => ({ li, word: li.dataset.word }))
    .sort((a, b) => b.word.length - a.word.length);

  for (const [index, w] of words.entries()) {
    let placed = false;
    for (let attempt = 0; attempt < 600 && !placed; attempt++) {
      // Alternate orientations so the words don't all stack as horizontal lines
      const fitsH = w.word.length <= cols;
      const fitsV = w.word.length <= rows;
      const wantV = index % 2 === 1 && attempt < 400;
      const dir = fitsV && (wantV || !fitsH) ? 'V' : 'H';
      const maxR = dir === 'V' ? rows - w.word.length : rows - 1;
      const maxC = dir === 'H' ? cols - w.word.length : cols - 1;
      const r0 = Math.floor(rand() * (maxR + 1));
      const c0 = Math.floor(rand() * (maxC + 1));
      const cells = [...w.word].map((ch, i) => ({
        r: dir === 'V' ? r0 + i : r0,
        c: dir === 'H' ? c0 + i : c0,
        ch,
      }));
      if (cells.every(({ r, c, ch }) => board[r][c] === null || board[r][c] === ch)) {
        cells.forEach(({ r, c, ch }) => { board[r][c] = ch; });
        Object.assign(w, { dir, r0, c0, cells });
        placed = true;
      }
    }
    if (!placed) return null;
  }
  return { board, words, rand };
}

let layout = null;
for (let seed = 7; !layout; seed++) layout = place(seed);
const { board, words, rand } = layout;

// ---------- Build cells ----------
const randomNoise = () => NOISE[Math.floor(rand() * NOISE.length)];
const randomOpacity = (min, max) => (rand() * (max - min) + min).toFixed(2);

const cells = [];
for (let r = 0; r < rows; r++) {
  for (let c = 0; c < cols; c++) {
    const el = document.createElement('span');
    el.className = 'wsh__cell';
    const ch = board[r][c];
    el.textContent = ch ?? randomNoise();
    el.style.opacity = randomOpacity(0.3, 0.7);
    if (ch) el.classList.add('is-word');
    grid.appendChild(el);
    cells.push({ el, r, c, isWord: Boolean(ch), lit: false });
  }
}
const cellAt = (r, c) => cells[r * cols + c];

// ---------- Reveal ----------
function lightCell(cell) {
  if (cell.lit) return;
  cell.lit = true;
  if (cell.isWord) {
    cell.el.classList.add('is-lit');
  } else {
    cell.el.textContent = randomNoise();
    cell.el.style.opacity = randomOpacity(0.08, 0.2);
  }
}

let callout = null;
let calloutTimer = null;
let shownWord = null;
let shownAt = 0;

function showCallout(w) {
  if (!CALLOUT_VARIANTS.includes(variant)) return;
  shownWord = w;
  shownAt = performance.now();
  if (!callout) {
    callout = document.createElement('div');
    callout.className = 'wsh__callout';
    callout.setAttribute('aria-hidden', 'true');
    callout.innerHTML = '<p class="wsh__callout-cat"></p><p class="wsh__callout-text"></p>';
    grid.appendChild(callout);
  }
  callout.querySelector('.wsh__callout-cat').textContent = w.li.querySelector('.wsh__cat').textContent;
  callout.querySelector('.wsh__callout-text').textContent = w.li.querySelector('.wsh__caption').textContent;

  // Below the word if there's room, else above it, else pinned inside the grid's bottom edge
  const endR = w.dir === 'V' ? w.r0 + w.word.length : w.r0 + 1;
  // Anchor near the word's start, clamped so the balloon stays inside the grid
  const widthPct = (callout.offsetWidth / grid.clientWidth) * 100 || 30;
  const leftPct = Math.max(0, Math.min((w.c0 / cols) * 100, 100 - widthPct));
  callout.style.left = `${leftPct}%`;
  callout.style.top = '';
  callout.style.bottom = '';
  if (rows - endR >= 3) callout.style.top = `calc(${(endR / rows) * 100}% + 8px)`;
  else if (w.r0 >= 3) callout.style.bottom = `calc(${(1 - w.r0 / rows) * 100}% + 8px)`;
  else callout.style.bottom = '8px';
  callout.classList.add('is-visible');
  clearTimeout(calloutTimer);
  // C hides on a timer; D keeps the balloon until the pointer moves on to other letters
  if (variant === 'C') calloutTimer = setTimeout(hideCallout, 3200);
}

function hideCallout() {
  callout?.classList.remove('is-visible');
  shownWord = null;
}

function wordAt(r, c) {
  return words.find(w => w.found && w.cells.some(cell => cell.r === r && cell.c === c));
}

function markFound(w) {
  w.found = true;
  w.cells.forEach(({ r, c }) => lightCell(cellAt(r, c)));

  const capsule = document.createElement('span');
  capsule.className = 'wsh__capsule';
  const inset = 0.08;
  const width = w.dir === 'H' ? w.word.length : 1;
  const height = w.dir === 'V' ? w.word.length : 1;
  capsule.style.left = `${((w.c0 + inset) / cols) * 100}%`;
  capsule.style.top = `${((w.r0 + inset) / rows) * 100}%`;
  capsule.style.width = `${((width - inset * 2) / cols) * 100}%`;
  capsule.style.height = `${((height - inset * 2) / rows) * 100}%`;
  grid.appendChild(capsule);

  w.li.classList.add('is-found');
  updateCount();
  showCallout(w);
}

function updateCount() {
  const found = words.filter(w => w.found).length;
  count.textContent = found === words.length ? 'All found' : `${found}/${words.length} found`;
  if (found === words.length) revealBtn.hidden = true;
}

function checkWords() {
  words.forEach(w => {
    if (!w.found && w.cells.every(({ r, c }) => cellAt(r, c).lit)) markFound(w);
  });
}

function onPointerMove(e) {
  const rect = grid.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * cols;
  const y = ((e.clientY - rect.top) / rect.height) * rows;
  cells.forEach(cell => {
    if (cell.lit) return;
    if (Math.hypot(x - (cell.c + 0.5), y - (cell.r + 0.5)) < REVEAL_RADIUS) lightCell(cell);
  });
  checkWords();

  if (variant === 'D') {
    const hovered = wordAt(Math.floor(y), Math.floor(x));
    if (hovered && hovered !== shownWord) showCallout(hovered);
    else if (!hovered && shownWord && performance.now() - shownAt > 1500) hideCallout();
  }
}

function revealAll(stagger) {
  words.filter(w => !w.found).forEach((w, i) => {
    setTimeout(() => markFound(w), i * stagger);
  });
  setTimeout(() => cells.forEach(lightCell), words.length * stagger);
}

grid.addEventListener('pointermove', onPointerMove);
grid.addEventListener('pointerdown', onPointerMove);
grid.addEventListener('pointerleave', () => { if (variant === 'D') hideCallout(); });
// Found chips re-open their balloon
items.forEach(li => li.addEventListener('click', () => {
  const w = words.find(word => word.li === li);
  if (w?.found) showCallout(w);
}));
revealBtn.addEventListener('click', () => revealAll(prefersReducedMotion ? 0 : 450));
updateCount();
if (prefersReducedMotion) revealAll(0);

// ---------- Prototype switcher (not part of the design) ----------
const bar = document.createElement('div');
bar.className = 'proto-switcher';
bar.innerHTML = `<button type="button" aria-label="Previous variant">←</button><span>${variant} (${VARIANTS[variant].name})</span><button type="button" aria-label="Next variant">→</button>`;
document.body.appendChild(bar);

function go(step) {
  const next = KEYS[(KEYS.indexOf(variant) + step + KEYS.length) % KEYS.length];
  const p = new URLSearchParams(location.search);
  p.set('variant', next);
  location.search = p.toString();
}
const [prev, next] = bar.querySelectorAll('button');
prev.addEventListener('click', () => go(-1));
next.addEventListener('click', () => go(1));
addEventListener('keydown', e => {
  if (e.target.closest('input, textarea, [contenteditable]')) return;
  if (e.key === 'ArrowLeft') go(-1);
  if (e.key === 'ArrowRight') go(1);
});
