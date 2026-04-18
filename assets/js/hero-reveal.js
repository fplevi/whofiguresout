const COLS = 22;
const ROWS = 6;
const HEADLINE_ROW_1 = 2;
const HEADLINE_ROW_2 = 3;
const AUTO_REVEAL_DELAY = 4000;
const STAGGER = 60;

const LINE_1 = "I'm a product designer";
const LINE_2 = "who figures it out.";
const NOISE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*";

const grid = document.getElementById('hero-grid');
if (!grid) throw new Error('hero-grid not found');

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Dimensions calculated from container width so the grid always fits
function getDimensions() {
  const availableWidth = grid.clientWidth;
  const charW = availableWidth / COLS;
  const lineH = charW * (115 / 57);
  const fontSize = charW * (88 / 57);
  const revealRadius = charW * (120 / 57);
  return { charW, lineH, fontSize, revealRadius };
}

function buildHeadlineMap() {
  const map = {};
  for (let r = 0; r < ROWS; r++) map[r] = {};
  for (let i = 0; i < LINE_1.length && i < COLS; i++) map[HEADLINE_ROW_1][i] = LINE_1[i];
  for (let i = 0; i < LINE_2.length && i < COLS; i++) map[HEADLINE_ROW_2][i] = LINE_2[i];
  return map;
}

const headlineMap = buildHeadlineMap();

function randomChar() {
  return NOISE[Math.floor(Math.random() * NOISE.length)];
}

function randomOpacity(min = 0.18, max = 0.65) {
  return (Math.random() * (max - min) + min).toFixed(2);
}

let cells = [];
let autoRevealTimer = null;
let autoRevealed = false;
let dims = getDimensions();

function buildGrid() {
  grid.innerHTML = '';
  cells = [];
  dims = getDimensions();
  const { charW, lineH, fontSize } = dims;

  grid.style.height = `${ROWS * lineH}px`;

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const el = document.createElement('span');
      el.className = 'hero__char';
      el.style.left = `${c * charW}px`;
      el.style.top = `${r * lineH}px`;
      el.style.fontSize = `${fontSize}px`;
      el.style.lineHeight = `${lineH}px`;
      el.style.width = `${charW}px`;

      const isHeadline = headlineMap[r][c] !== undefined;
      const correctChar = isHeadline ? headlineMap[r][c] : null;
      const opacity = parseFloat(randomOpacity());

      el.textContent = randomChar();
      el.style.color = 'var(--accent-primary)';
      el.style.opacity = opacity;

      grid.appendChild(el);
      cells.push({ el, row: r, col: c, isHeadline, correctChar, revealed: false, opacity });
    }
  }
}

function revealCell(cell, toCorrect) {
  cell.revealed = true;
  if (cell.isHeadline && toCorrect) {
    cell.el.textContent = cell.correctChar;
    cell.el.style.color = 'var(--text-primary)';
    cell.el.style.opacity = '1';
  } else {
    const postOpacity = randomOpacity(0.10, 0.28);
    cell.el.textContent = randomChar();
    cell.el.style.color = 'var(--accent-primary)';
    cell.el.style.opacity = postOpacity;
  }
}

function finishReveal() {
  grid.removeAttribute('aria-hidden');
  grid.setAttribute('aria-label', "I'm a product designer who figures it out.");
}

function onMouseMove(e) {
  if (autoRevealed) return;

  const rect = grid.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;
  const { charW, lineH, revealRadius } = dims;

  cells.forEach(cell => {
    if (cell.revealed) return;
    const cellX = cell.col * charW + charW / 2;
    const cellY = cell.row * lineH + lineH / 2;
    const dist = Math.sqrt((mouseX - cellX) ** 2 + (mouseY - cellY) ** 2);
    if (dist < revealRadius) revealCell(cell, true);
  });

  const allHeadlineRevealed = cells.filter(c => c.isHeadline).every(c => c.revealed);
  if (allHeadlineRevealed) finishReveal();
}

function autoReveal() {
  autoRevealed = true;
  grid.removeEventListener('mousemove', onMouseMove);

  for (let c = 0; c < COLS; c++) {
    const colCells = cells.filter(cell => cell.col === c && !cell.revealed);
    setTimeout(() => {
      colCells.forEach(cell => revealCell(cell, true));
    }, c * STAGGER);
  }

  setTimeout(finishReveal, COLS * STAGGER + 120);
}

function initReducedMotion() {
  cells.forEach(cell => {
    if (cell.isHeadline) {
      cell.el.textContent = cell.correctChar;
      cell.el.style.color = 'var(--text-primary)';
      cell.el.style.opacity = '1';
    } else {
      cell.el.style.opacity = '0.12';
    }
    cell.revealed = true;
  });
  finishReveal();
}

// Debounced resize: rebuild grid with new dimensions
let resizeTimer = null;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    const wasRevealed = autoRevealed;
    clearTimeout(autoRevealTimer);
    autoRevealed = false;
    grid.removeEventListener('mousemove', onMouseMove);

    buildGrid();

    if (prefersReducedMotion || wasRevealed) {
      initReducedMotion();
    } else {
      grid.addEventListener('mousemove', onMouseMove);
      autoRevealTimer = setTimeout(autoReveal, AUTO_REVEAL_DELAY);
    }
  }, 150);
});

// Init
buildGrid();

if (prefersReducedMotion) {
  initReducedMotion();
} else {
  grid.addEventListener('mousemove', onMouseMove);
  autoRevealTimer = setTimeout(autoReveal, AUTO_REVEAL_DELAY);
}
