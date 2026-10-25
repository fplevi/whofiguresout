// Replays place() from assets/js/case-hero-wordsearch.js and scores seeds: parallel words must not sit in
// neighbouring lines (or the same line) with overlapping spans. Usage: node seed-search.mjs WORD,WORD,...
const words0 = process.argv[2].split(',');
function mulberry32(seed) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function place(cols, rows, seed) {
  const rand = mulberry32(seed);
  const board = Array.from({ length: rows }, () => Array(cols).fill(null));
  const words = words0.map(word => ({ word })).sort((a, b) => b.word.length - a.word.length);
  for (const [index, w] of words.entries()) {
    let placed = false;
    for (let attempt = 0; attempt < 600 && !placed; attempt++) {
      const fitsH = w.word.length <= cols, fitsV = w.word.length <= rows;
      const wantV = index % 2 === 1 && attempt < 400;
      const dir = fitsV && (wantV || !fitsH) ? 'V' : 'H';
      const maxR = dir === 'V' ? rows - w.word.length : rows - 1;
      const maxC = dir === 'H' ? cols - w.word.length : cols - 1;
      const r0 = Math.floor(rand() * (maxR + 1)), c0 = Math.floor(rand() * (maxC + 1));
      const cells = [...w.word].map((ch, i) => ({ r: dir === 'V' ? r0 + i : r0, c: dir === 'H' ? c0 + i : c0, ch }));
      if (cells.every(({ r, c, ch }) => board[r][c] === null || board[r][c] === ch)) {
        cells.forEach(({ r, c, ch }) => { board[r][c] = ch; }); Object.assign(w, { dir, r0, c0 }); placed = true;
      }
    }
    if (!placed) return null;
  }
  return words;
}
// The page bumps the seed until a layout fits; mirror that.
const layoutFor = (cols, rows, seed) => { for (let s = seed; ; s++) { const l = place(cols, rows, s); if (l) return l; } };
function clashes(words) {
  // Any two words with letters in neighbouring cells (diagonals included) read as one find.
  const cells = (w) => [...w.word].map((_, i) => [w.dir === 'V' ? w.r0 + i : w.r0, w.dir === 'H' ? w.c0 + i : w.c0]);
  let n = 0;
  for (let i = 0; i < words.length; i++) for (let j = i + 1; j < words.length; j++) {
    const a = cells(words[i]), b = cells(words[j]);
    if (a.some(([r, c]) => b.some(([r2, c2]) => Math.max(Math.abs(r - r2), Math.abs(c - c2)) <= 1))) n++;
  }
  return n;
}
const draw = (cols, rows, words) => { const g = Array.from({ length: rows }, () => Array(cols).fill('·')); for (const w of words) [...w.word].forEach((ch, i) => { g[w.dir === 'V' ? w.r0 + i : w.r0][w.dir === 'H' ? w.c0 + i : w.c0] = ch; }); return g.map(r => r.join(' ')).join('\n'); };
const good = [];
for (let seed = 1; seed <= 2000; seed++) {
  const d = layoutFor(24, 7, seed), m = layoutFor(12, 12, seed);
  const score = clashes(d) + clashes(m);
  const vertical = d.filter(w => w.dir === 'V').length;
  if ((score === 0 && good.length < 4)) {
    if (score === 0) good.push(seed);
    console.log(`seed ${seed}: clashes ${score}, desktop vertical ${vertical}\n${draw(24, 7, d)}\n\n${draw(12, 12, m)}\n`);
  }
}
console.log('candidates', good);
