const COLS = 22;
const ROWS = 6;
const CHAR_W = 57;
const LINE_H = 115;
const HEADLINE_ROW_1 = 2; // 0-indexed
const HEADLINE_ROW_2 = 3;
const REVEAL_RADIUS = 120;
const AUTO_REVEAL_DELAY = 4000;
const STAGGER = 60;
const DURATION = 120;

const LINE_1 = "I'm a product designer";
const LINE_2 = "who figures it out.";
const NOISE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*";

const grid = document.getElementById('hero-grid');
if (!grid) throw new Error('hero-grid not found');

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Build headline map: [row][col] = correct char or null
function buildHeadlineMap() {
  const map = {};
  for (let r = 0; r < ROWS; r++) map[r] = {};

  // Line 1 starts at col 0, row HEADLINE_ROW_1
  for (let i = 0; i < LINE_1.length && i < COLS; i++) {
    map[HEADLINE_ROW_1][i] = LINE_1[i];
  }
  // Line 2 starts at col 0, row HEADLINE_ROW_2
  for (let i = 0; i < LINE_2.length && i < COLS; i++) {
    map[HEADLINE_ROW_2][i] = LINE_2[i];
  }
  return map;
}

const headlineMap = buildHeadlineMap();

function randomChar() {
  return NOISE[Math.floor(Math.random() * NOISE.length)];
}

function randomOpacity() {
  return (Math.random() * (0.65 - 0.18) + 0.18).toFixed(2);
}

// State per cell
const cells = [];

function buildGrid() {
  grid.style.position = 'relative';
  grid.style.height = `${ROWS * LINE_H}px`;

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const el = document.createElement('span');
      el.className = 'hero__char';
      el.style.left = `${c * CHAR_W}px`;
      el.style.top = `${r * LINE_H}px`;

      const isHeadline = headlineMap[r][c] !== undefined;
      const correctChar = isHeadline ? headlineMap[r][c] : null;
      const noiseChar = randomChar();
      const opacity = parseFloat(randomOpacity());

      el.textContent = noiseChar;
      el.style.color = 'var(--accent-primary)';
      el.style.opacity = opacity;

      grid.appendChild(el);
      cells.push({ el, row: r, col: c, isHeadline, correctChar, revealed: false, opacity });
    }
  }
}

// Reveal a single cell to its correct/noise state
function revealCell(cell, toCorrect) {
  cell.revealed = true;
  if (cell.isHeadline && toCorrect) {
    cell.el.textContent = cell.correctChar;
    cell.el.style.color = 'var(--text-primary)';
    cell.el.style.opacity = '1';
  } else {
    // Keep noise char, dim to post-reveal opacity
    const postOpacity = (Math.random() * (0.28 - 0.10) + 0.10).toFixed(2);
    cell.el.textContent = randomChar();
    cell.el.style.color = 'var(--accent-primary)';
    cell.el.style.opacity = postOpacity;
  }
}

// Hover reveal: find cells within radius of cursor
function onMouseMove(e) {
  if (autoRevealed) return;
  hovering = true;
  clearTimeout(autoRevealTimer);

  const rect = grid.getBoundingClientRect();
  const mouseX = e.clientX - rect.left;
  const mouseY = e.clientY - rect.top;

  cells.forEach(cell => {
    if (cell.revealed) return;
    const cellX = cell.col * CHAR_W + CHAR_W / 2;
    const cellY = cell.row * LINE_H + LINE_H / 2;
    const dist = Math.sqrt((mouseX - cellX) ** 2 + (mouseY - cellY) ** 2);

    if (dist < REVEAL_RADIUS) {
      revealCell(cell, true);
    }
  });

  // Check if all headline chars revealed
  const allHeadlineRevealed = cells
    .filter(c => c.isHeadline)
    .every(c => c.revealed);

  if (allHeadlineRevealed) {
    finishReveal();
  }
}

let autoRevealTimer = null;
let autoRevealed = false;
let hovering = false;

function autoReveal() {
  autoRevealed = true;
  grid.removeEventListener('mousemove', onMouseMove);

  // Sweep left to right per column
  for (let c = 0; c < COLS; c++) {
    const colCells = cells.filter(cell => cell.col === c && !cell.revealed);
    setTimeout(() => {
      colCells.forEach(cell => revealCell(cell, true));
    }, c * STAGGER);
  }

  // After sweep complete, finalize
  setTimeout(finishReveal, COLS * STAGGER + DURATION);
}

function finishReveal() {
  // Update aria attributes once revealed
  grid.removeAttribute('aria-hidden');
  grid.setAttribute('aria-label', "I'm a product designer who figures it out.");
}

function initReducedMotion() {
  // Show headline immediately, no animation
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

buildGrid();

if (prefersReducedMotion) {
  initReducedMotion();
} else {
  grid.addEventListener('mousemove', onMouseMove);
  autoRevealTimer = setTimeout(autoReveal, AUTO_REVEAL_DELAY);
}
