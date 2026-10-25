// Case hero word search: hover (or drag) over the grid to light up the case's key words.
// Each found word opens a balloon with its caption. Words and captions live in the HTML legend,
// so the content is complete without JS, for assistive tech, and with reduced motion.
// An optional fixed phrase (.wsh__phrase, used by the home hero) sits centered in the grid: it
// reveals like a word, opens its own balloon, reveals itself after a delay, and stays out of the count.

const REVEAL_RADIUS = 1.5; // in cells
const BALLOON_MIN_MS = 1500; // a fresh balloon stays at least this long while the pointer moves on
const MOBILE_QUERY = '(max-width: 768px)';
const NOISE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
const PHRASE_AUTO_REVEAL_MS = 10000;
const PHRASE_STAGGER_MS = 60; // per column

const root = document.querySelector('.wsh');
if (!root) throw new Error('.wsh not found');

const grid = root.querySelector('.wsh__grid');
const count = root.querySelector('.wsh__count');
const revealBtn = root.querySelector('.wsh__reveal');
const items = [...root.querySelectorAll('.wsh__item')];
const phraseEl = root.querySelector('.wsh__phrase');
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

// The phrase's lines (one set per breakpoint), each centered, the block centered vertically.
// Its rows are reserved whole, so words never cross it and the space beside it stays noise.
function layPhrase(cols, rows) {
  if (!phraseEl) return null;
  const lines = (mobile.matches ? phraseEl.dataset.linesMobile : phraseEl.dataset.lines).split('|');
  const top = Math.floor((rows - lines.length) / 2);
  const cells = lines.flatMap((line, i) => {
    const left = Math.floor((cols - line.length) / 2);
    return [...line].map((ch, j) => ({ r: top + i, c: left + j, ch }));
  });
  return {
    li: phraseEl,
    cells,
    rowsTaken: lines.map((_, i) => top + i),
    r0: top,
    c0: Math.min(...cells.map(cell => cell.c)),
    endR: top + lines.length,
    found: false,
  };
}

// Places words horizontally/vertically, alternating orientation; overlaps only on equal letters
function place(cols, rows, seed, phrase) {
  const rand = mulberry32(seed);
  const board = Array.from({ length: rows }, () => Array(cols).fill(null));
  phrase?.rowsTaken.forEach(r => board[r].fill(RESERVED));
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
        const endR = dir === 'V' ? r0 + w.word.length : r0 + 1;
        Object.assign(w, { dir, r0, c0, endR, cells, found: false });
        placed = true;
      }
    }
    if (!placed) return null;
  }
  return { board, words, rand };
}

const RESERVED = Symbol('reserved');

let state = null;
let balloon = null;
let shownWord = null;
let shownAt = 0;

function build() {
  const found = new Set(state?.words.filter(w => w.found).map(w => w.word));
  const phraseFound = state?.phrase?.found;
  // Size comes from CSS (--wsh-cols/rows on .wsh), already resolved for the current breakpoint,
  // so the space reserved before this script ran matches the grid built here.
  const gridStyle = getComputedStyle(grid);
  const cols = parseInt(gridStyle.getPropertyValue('--cols'), 10);
  const rows = parseInt(gridStyle.getPropertyValue('--rows'), 10);
  const phrase = layPhrase(cols, rows);
  let layout = null;
  for (let seed = Number(root.dataset.seed ?? 7); !layout; seed++) layout = place(cols, rows, seed, phrase);

  grid.innerHTML = '';
  balloon = null;
  shownWord = null;

  const { board, words, rand } = layout;
  const phraseAt = new Map(phrase?.cells.map(cell => [cell.r * cols + cell.c, cell.ch]));
  const cells = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const el = document.createElement('span');
      el.className = 'wsh__cell';
      // Word letters show from the start (it's a word search); phrase letters stay noise until lit
      const inPhrase = phraseAt.has(r * cols + c);
      const ch = inPhrase ? phraseAt.get(r * cols + c) : board[r][c] === RESERVED ? null : board[r][c];
      el.textContent = ch && !inPhrase ? ch : NOISE[Math.floor(rand() * NOISE.length)];
      el.style.opacity = (rand() * 0.4 + 0.3).toFixed(2);
      if (ch) el.classList.add('is-word');
      grid.appendChild(el);
      cells.push({ el, r, c, ch, isWord: Boolean(ch), lit: false });
    }
  }
  state = { cols, rows, words, phrase, cells, rand };

  // Words found before a breakpoint change stay found, without reopening their balloons
  words.filter(w => found.has(w.word)).forEach(w => markFound(w, { quiet: true }));
  if (phraseFound) markPhraseFound({ quiet: true });
  updateCount();
}

const cellAt = (r, c) => state.cells[r * state.cols + c];

function lightCell(cell) {
  if (cell.lit) return;
  cell.lit = true;
  if (cell.isWord) {
    cell.el.textContent = cell.ch;
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
  const cat = balloon.querySelector('.wsh__balloon-cat');
  cat.textContent = w.li.querySelector('.wsh__cat')?.textContent ?? '';
  cat.hidden = !cat.textContent;
  balloon.querySelector('.wsh__balloon-text').textContent = w.li.querySelector('.wsh__caption').textContent;

  // Below the word if there's room, else above it, else pinned inside the grid's bottom edge
  const { cols, rows } = state;
  const { endR } = w;
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

function markPhraseFound({ quiet = false } = {}) {
  const { phrase } = state;
  if (!phrase || phrase.found) return;
  phrase.found = true;
  // The noise beside it fades too, so the headline reads clean
  phrase.rowsTaken.forEach(r => state.cells.filter(cell => cell.r === r).forEach(lightCell));
  if (!quiet) showBalloon(phrase);
}

// Column by column, left to right, so the phrase reads in even for visitors who don't play
function autoRevealPhrase() {
  const { phrase, cols } = state;
  if (!phrase || phrase.found) return;
  for (let c = 0; c < cols; c++) {
    setTimeout(() => {
      state.phrase.rowsTaken.forEach(r => lightCell(cellAt(r, c)));
    }, c * PHRASE_STAGGER_MS);
  }
  setTimeout(() => markPhraseFound({ quiet: true }), cols * PHRASE_STAGGER_MS);
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
  const { phrase } = state;
  if (phrase && !phrase.found && phrase.cells.every(({ r, c }) => cellAt(r, c).lit)) markPhraseFound();

  const r = Math.floor(y);
  const c = Math.floor(x);
  const hovered = [...words, ...(phrase ? [phrase] : [])]
    .find(w => w.found && w.cells.some(cell => cell.r === r && cell.c === c));
  if (hovered && hovered !== shownWord) showBalloon(hovered);
  else if (!hovered && shownWord && performance.now() - shownAt > BALLOON_MIN_MS) hideBalloon();
}

function revealAll(stagger, onDone) {
  const pending = state.words.filter(w => !w.found);
  pending.forEach((w, i) => setTimeout(() => markFound(w, { quiet: stagger === 0 }), i * stagger));
  setTimeout(() => {
    state.cells.forEach(lightCell);
    markPhraseFound({ quiet: true });
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
else if (phraseEl) setTimeout(() => autoRevealPhrase(), PHRASE_AUTO_REVEAL_MS);
