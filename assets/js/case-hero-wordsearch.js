// Case hero word search: hover (or drag) over the grid to light up the case's key words.
// Each found word opens a balloon with its caption. Words and captions live in the HTML legend,
// so the content is complete without JS, for assistive tech, and with reduced motion.

const REVEAL_RADIUS = 1.5; // in cells
const BALLOON_MIN_MS = 1500; // a fresh balloon stays at least this long while the pointer moves on
const MOBILE_QUERY = '(max-width: 768px)';
const NOISE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

const root = document.querySelector('.wsh');
if (!root) throw new Error('.wsh not found');

const grid = root.querySelector('.wsh__grid');
const count = root.querySelector('.wsh__count');
const revealBtn = root.querySelector('.wsh__reveal');
const items = [...root.querySelectorAll('.wsh__item')];
const mobile = matchMedia(MOBILE_QUERY);
const prefersReducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Seeded RNG so the puzzle is identical on every visit
function mulberry32(seed) {
  return () => {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Places words horizontally/vertically, alternating orientation; overlaps only on equal letters
function place(cols, rows, seed) {
  const rand = mulberry32(seed);
  const board = Array.from({ length: rows }, () => Array(cols).fill(null));
  const words = items
    .map(li => ({ li, word: li.dataset.word }))
    .sort((a, b) => b.word.length - a.word.length);

  for (const [index, w] of words.entries()) {
    let placed = false;
    for (let attempt = 0; attempt < 600 && !placed; attempt++) {
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
        Object.assign(w, { dir, r0, c0, cells, found: false });
        placed = true;
      }
    }
    if (!placed) return null;
  }
  return { board, words, rand };
}

let state = null;
let balloon = null;
let shownWord = null;
let shownAt = 0;

function build() {
  const found = new Set(state?.words.filter(w => w.found).map(w => w.word));
  const cols = Number(mobile.matches ? root.dataset.colsMobile : root.dataset.cols);
  const rows = Number(mobile.matches ? root.dataset.rowsMobile : root.dataset.rows);
  let layout = null;
  for (let seed = Number(root.dataset.seed ?? 7); !layout; seed++) layout = place(cols, rows, seed);

  grid.innerHTML = '';
  grid.style.setProperty('--cols', cols);
  grid.style.setProperty('--rows', rows);
  balloon = null;
  shownWord = null;

  const { board, words, rand } = layout;
  const cells = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const el = document.createElement('span');
      el.className = 'wsh__cell';
      const ch = board[r][c];
      el.textContent = ch ?? NOISE[Math.floor(rand() * NOISE.length)];
      el.style.opacity = (rand() * 0.4 + 0.3).toFixed(2);
      if (ch) el.classList.add('is-word');
      grid.appendChild(el);
      cells.push({ el, r, c, isWord: Boolean(ch), lit: false });
    }
  }
  state = { cols, rows, words, cells, rand };

  // Words found before a breakpoint change stay found, without reopening their balloons
  words.filter(w => found.has(w.word)).forEach(w => markFound(w, { quiet: true }));
  updateCount();
}

const cellAt = (r, c) => state.cells[r * state.cols + c];

function lightCell(cell) {
  if (cell.lit) return;
  cell.lit = true;
  if (cell.isWord) {
    cell.el.classList.add('is-lit');
  } else {
    cell.el.textContent = NOISE[Math.floor(state.rand() * NOISE.length)];
    cell.el.style.opacity = (state.rand() * 0.12 + 0.08).toFixed(2);
  }
}

function showBalloon(w) {
  if (!balloon) {
    balloon = document.createElement('div');
    balloon.className = 'wsh__balloon';
    balloon.setAttribute('aria-hidden', 'true'); // the legend already carries the text
    balloon.innerHTML = '<p class="wsh__balloon-cat"></p><p class="wsh__balloon-text"></p>';
    grid.appendChild(balloon);
  }
  balloon.querySelector('.wsh__balloon-cat').textContent = w.li.querySelector('.wsh__cat').textContent;
  balloon.querySelector('.wsh__balloon-text').textContent = w.li.querySelector('.wsh__caption').textContent;

  // Below the word if there's room, else above it, else pinned inside the grid's bottom edge
  const { cols, rows } = state;
  const endR = w.dir === 'V' ? w.r0 + w.word.length : w.r0 + 1;
  const widthPct = (balloon.offsetWidth / grid.clientWidth) * 100;
  balloon.style.left = `${Math.max(0, Math.min((w.c0 / cols) * 100, 100 - widthPct))}%`;
  balloon.style.top = '';
  balloon.style.bottom = '';
  if (rows - endR >= 3) balloon.style.top = `calc(${(endR / rows) * 100}% + 8px)`;
  else if (w.r0 >= 3) balloon.style.bottom = `calc(${(1 - w.r0 / rows) * 100}% + 8px)`;
  else balloon.style.bottom = '8px';

  balloon.classList.add('is-visible');
  shownWord = w;
  shownAt = performance.now();
}

function hideBalloon() {
  balloon?.classList.remove('is-visible');
  shownWord = null;
}

function markFound(w, { quiet = false } = {}) {
  w.found = true;
  w.cells.forEach(({ r, c }) => lightCell(cellAt(r, c)));

  const { cols, rows } = state;
  const inset = 0.08;
  const capsule = document.createElement('span');
  capsule.className = 'wsh__capsule';
  capsule.style.left = `${((w.c0 + inset) / cols) * 100}%`;
  capsule.style.top = `${((w.r0 + inset) / rows) * 100}%`;
  capsule.style.width = `${(((w.dir === 'H' ? w.word.length : 1) - inset * 2) / cols) * 100}%`;
  capsule.style.height = `${(((w.dir === 'V' ? w.word.length : 1) - inset * 2) / rows) * 100}%`;
  grid.appendChild(capsule);

  w.li.classList.add('is-found');
  w.li.querySelector('.wsh__chip').disabled = false;
  if (!quiet) {
    updateCount();
    showBalloon(w);
  }
}

function updateCount() {
  const { words } = state;
  const found = words.filter(w => w.found).length;
  count.textContent = found === words.length ? 'All found' : `${found}/${words.length} found`;
  revealBtn.hidden = found === words.length;
}

function onPointerMove(e) {
  const { cols, rows, cells, words } = state;
  const rect = grid.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * cols;
  const y = ((e.clientY - rect.top) / rect.height) * rows;

  cells.forEach(cell => {
    if (!cell.lit && Math.hypot(x - (cell.c + 0.5), y - (cell.r + 0.5)) < REVEAL_RADIUS) lightCell(cell);
  });
  words.forEach(w => {
    if (!w.found && w.cells.every(({ r, c }) => cellAt(r, c).lit)) markFound(w);
  });

  const r = Math.floor(y);
  const c = Math.floor(x);
  const hovered = words.find(w => w.found && w.cells.some(cell => cell.r === r && cell.c === c));
  if (hovered && hovered !== shownWord) showBalloon(hovered);
  else if (!hovered && shownWord && performance.now() - shownAt > BALLOON_MIN_MS) hideBalloon();
}

function revealAll(stagger, onDone) {
  const pending = state.words.filter(w => !w.found);
  pending.forEach((w, i) => setTimeout(() => markFound(w, { quiet: stagger === 0 }), i * stagger));
  setTimeout(() => {
    state.cells.forEach(lightCell);
    updateCount();
    onDone?.();
  }, pending.length * stagger);
}

build();
root.classList.add('wsh--ready');

grid.addEventListener('pointermove', onPointerMove);
grid.addEventListener('pointerdown', onPointerMove);
grid.addEventListener('pointerleave', hideBalloon);
// The button hides itself once everything is found, so hand focus to the first chip
revealBtn.addEventListener('click', () => {
  revealAll(prefersReducedMotion ? 0 : 450, () => items[0].querySelector('.wsh__chip').focus());
});

// Found chips reopen their balloon (click, tap, or keyboard focus)
items.forEach(li => {
  const chip = li.querySelector('.wsh__chip');
  const open = () => {
    const w = state.words.find(word => word.li === li);
    if (w?.found) showBalloon(w);
  };
  chip.addEventListener('click', open);
  chip.addEventListener('focus', open);
  chip.addEventListener('blur', hideBalloon);
});

mobile.addEventListener('change', build);

if (prefersReducedMotion) revealAll(0);
