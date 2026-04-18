# Felipe Levi Portfolio — V1 Development Plan
## Claude Code Agent Guide

---

## Project Overview

**Goal:** Build and launch Felipe Levi's portfolio v1 on GitHub Pages.
**Stack:** HTML + CSS + Vanilla JS — no frameworks, no build step, no dependencies.
**Deploy:** GitHub Pages (static hosting, zero cost).
**Scope:** Homepage + 3 case study pages. No CMS for v1.

---

## Design Tokens (from Figma Variables)

```css
:root {
  /* Background */
  --background-primary:   #0D0F1A;
  --background-secondary: #121528;
  --background-divider:   rgba(255, 255, 255, 0.08);

  /* Text */
  --text-primary:    rgba(242, 242, 245, 1.00);
  --text-secondary:  rgba(242, 242, 245, 0.45);
  --text-muted:      rgba(242, 242, 245, 0.45);
  --text-ghost:      rgba(242, 242, 245, 0.20);
  --text-index:      rgba(242, 242, 245, 0.025);

  /* Accent */
  --accent-primary:  #F4A87C;
  --accent-muted:    rgba(244, 168, 124, 0.35);
  --accent-subtle:   rgba(244, 168, 124, 0.12);

  /* Border Radius */
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-full: 100px;

  /* Spacing */
  --space-4:  4px;
  --space-8:  8px;
  --space-12: 12px;
  --space-16: 16px;
  --space-20: 20px;
  --space-24: 24px;
  --space-32: 32px;
  --space-40: 40px;
  --space-48: 48px;
  --space-64: 64px;
  --space-80: 80px;

  /* Typography */
  --font-display:  'Fraunces', serif;
  --font-body:     'Inter', sans-serif;

  --size-display:  88px;
  --size-h1:       80px;
  --size-h2:       72px;
  --size-h3:       48px;
  --size-h4:       40px;
  --size-body-lg:  18px;
  --size-body-md:  16px;
  --size-body-sm:  15px;
  --size-label:    11px;
  --size-stat:     64px;

  /* Layout */
  --max-width:    1440px;
  --content-width: 1280px;
  --margin:        80px;
}
```

---

## File Structure

```
portfolio/
├── index.html                  # Homepage
├── case-studies/
│   ├── harmony.html            # Harmony — Design System
│   ├── billing.html            # Billing & Debt Recovery
│   └── enrollment.html         # Enrollment Journey
├── assets/
│   ├── css/
│   │   ├── reset.css           # CSS reset
│   │   ├── tokens.css          # Design tokens (variables above)
│   │   ├── global.css          # Typography, layout, utilities
│   │   ├── nav.css
│   │   ├── hero.css            # Character reveal grid
│   │   ├── cards.css           # Case study cards
│   │   ├── contact.css
│   │   ├── footer.css
│   │   └── case-study.css      # Shared case study layout
│   ├── js/
│   │   ├── hero-reveal.js      # Character grid reveal interaction
│   │   ├── scroll-animations.js # Scroll-triggered card animations
│   │   └── contact-form.js     # Form submission (Formspree)
│   ├── fonts/                  # Self-hosted Fraunces + Inter
│   │   ├── fraunces/
│   │   └── inter/
│   └── images/
│       ├── harmony/
│       ├── billing/
│       └── enrollment/
└── README.md
```

---

## Pages

### 1. Homepage (`index.html`)

**Sections in order:**

1. **Nav** — Logo left, Work / About / Contact right. Work in accent color (active state). Sticky on scroll, background fills in as user scrolls past hero.

2. **Hero** — Character reveal grid. 22 cols × 6 rows, Fraunces Bold 88px, cell width 57px, line height 115px. Grid starts at y=92px below nav. All chars in `--accent-primary` at varying opacity (18–65%) on load. On hover: chars near cursor flip to correct letter + `--text-primary` within ~120px radius. Auto-reveal after 4s if no hover: left-to-right sweep, 60ms stagger per char. Subtitle ("Design is a series of decisions...") always visible below the grid. Scroll hint "↓ scroll" at bottom.

3. **Selected Work** — Section tag "SELECTED WORK" in accent. Three full-width cards (big version). Each card: dark background (`--background-secondary`), coral left stripe (3px), faded index number (01/02/03) in background, category tag, title in Fraunces Bold 72px, hook text, stat number in accent, stat label, "Read case study" CTA inside card. Default state: opacity 0.6, muted fills. Active/hover state: full opacity, coral stripe, stat visible, CTA solid. Bottom row: "Want more?" muted + "Show all projects →" accent, both right-aligned.

4. **Contact** — "CONTACT" tag. "Have a project in mind?" at 22px muted. "Let's work together." Fraunces Bold 80px. Email + LinkedIn links in accent. Full-width form: name, email, message fields + "Send message" CTA right-aligned. Form submits via Formspree (no backend needed).

5. **About** — "ABOUT" tag. Bio paragraph in `--text-secondary`.

6. **Photo + Big Name** — Full-width photo (Felipe's AI-generated photo, dark background blends into page). "Felipe Levi" at Fraunces Bold 200px below it, edge to edge.

7. **Footer** — "Found what you were looking for?" left, "Download CV ↓" solid coral button right.

---

### 2. Case Study Pages (shared template)

**Sections in order:**

1. **Nav** — Same as homepage, sticky.
2. **Case Header** — Back link "← Back to work" in accent. Category tag. Title Fraunces Bold 88px. Hook line 22px. Meta row: 3 pills (Role / Timeline / Outcome).
3. **Hero Image** — Full bleed, no border, no padding. Edge to edge.
4. **The Problem** — Tag, title Fraunces 48px, body text, stakes callout box right side.
5. **My Role** — Tag, title, body.
6. **The Decisions** — Tag, intro title, 3 decision cards. Each card: number, title Fraunces 24px, body, tradeoff pill right.
7. **What Shipped** — Tag, title, image grid (Option B: full-width primary + two columns below).
8. **The Outcome** — Tag, title, 4 stat boxes.
9. **Next Project** — "Next project" muted label, next case title in Fraunces 48px with arrow, category tag.
10. **Contact** — Same as homepage contact section.

**Three instances:**
- `harmony.html` — Next: Billing & Debt Recovery
- `billing.html` — Next: Enrollment Journey
- `enrollment.html` — Next: Harmony

---

## Key Interactions

### Hero Character Reveal (`hero-reveal.js`)

```
CONSTANTS:
  COLS = 22
  ROWS = 6
  CHAR_W = 57px
  LINE_H = 115px
  HEADLINE_ROW_1 = 2 (0-indexed)
  HEADLINE_ROW_2 = 3
  REVEAL_RADIUS = 120px
  AUTO_REVEAL_DELAY = 4000ms
  STAGGER = 60ms per char
  DURATION = 120ms per char

LINE_1 = "I'm a product designer"
LINE_2 = "who figures it out."
NOISE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%&*"

STATE A (on load):
  - All positions show random chars
  - Color: var(--accent-primary)
  - Opacity: random 0.18–0.65 per char

TRIGGER (hover):
  - Track mouse position relative to grid
  - For each char within REVEAL_RADIUS of cursor:
    - Swap to correct headline char (or keep noise if not headline pos)
    - Transition color to var(--text-primary)
    - Duration: 120ms ease-out

TRIGGER (auto after 4s no hover):
  - Left to right sweep across all cols
  - Each char: random → correct, accent → white
  - 60ms stagger per column

STATE C (fully revealed):
  - Headline chars: var(--text-primary)
  - Noise chars: var(--accent-primary) opacity 10–28%
  - Subtitle: always visible throughout
```

### Scroll Animations (`scroll-animations.js`)

```
CASE CARDS:
  - IntersectionObserver threshold: 0.15
  - On enter: opacity 0 → 1, translateY(24px) → 0
  - Duration: 600ms ease-out
  - Stagger between cards: 120ms

SECTIONS:
  - Same observer, lighter animation
  - opacity 0 → 1, translateY(16px) → 0
  - Duration: 500ms ease-out

NAV BACKGROUND:
  - On scroll past hero height: nav background fills in
  - transition: background-color 300ms ease
```

### Contact Form (`contact-form.js`)

```
Provider: Formspree (https://formspree.io)
  - Free tier: 50 submissions/month
  - No backend needed
  - AJAX submit → show success state inline
  - No page reload

Fields: name (required), email (required), message (required)
Success state: replace form with confirmation message
Error state: show inline error below submit button
```

---

## Performance Rules (Agent Must Follow)

- **No JavaScript frameworks.** Vanilla JS only.
- **No CSS preprocessors.** Plain CSS with custom properties.
- **Fonts:** Self-host Fraunces and Inter (download from Google Fonts, serve locally). Preload critical weights.
- **Images:** WebP format, `loading="lazy"` on all below-fold images. Hero image eager-loaded.
- **No external dependencies** except Formspree endpoint.
- **Target:** Lighthouse score 95+ on performance.
- **Google Fonts import:** Only if self-hosting fails — use `display=swap`.

---

## Accessibility Rules (Agent Must Follow)

- All interactive elements keyboard navigable.
- Focus styles visible (outline using `--accent-primary`).
- Hero grid: after auto-reveal completes, `aria-label` on the grid container with the full headline text. Before reveal: `aria-hidden="true"` on grid, headline in visually hidden `<h1>`.
- Form fields: `<label>` elements properly associated.
- Color contrast: all text meets WCAG AA minimum. `--text-secondary` at 45% on `--background-primary` must pass.
- Images: meaningful `alt` attributes.
- `prefers-reduced-motion`: disable char animation, show headline immediately.

---

## GitHub Pages Setup

```
Repository: github.com/fplevi/portfolio (or similar)
Branch: main → GitHub Pages serves from /root
Custom domain: optional, can add later
HTTPS: automatic via GitHub Pages

Deploy flow:
  1. Push to main
  2. GitHub Pages serves automatically
  3. No build step, no CI needed
```

---

## Development Stages (for Claude Code)

### Stage 1 — Foundation
- [ ] Create repo and folder structure
- [ ] `reset.css` + `tokens.css` with all design variables
- [ ] `global.css` — typography scale, layout utilities
- [ ] Google Fonts / self-hosted fonts setup
- [ ] Nav component (HTML + CSS)

### Stage 2 — Homepage
- [ ] Hero section HTML structure
- [ ] Hero CSS (grid container, char positioning)
- [ ] `hero-reveal.js` — full character reveal interaction
- [ ] `prefers-reduced-motion` fallback for hero
- [ ] Case cards section (HTML + CSS)
- [ ] Cards hover states
- [ ] Contact section (HTML + CSS)
- [ ] About section
- [ ] Photo + Big Name section
- [ ] Footer

### Stage 3 — Scroll Animations
- [ ] `scroll-animations.js` — IntersectionObserver setup
- [ ] Card entrance animations
- [ ] Section entrance animations
- [ ] Nav background fill on scroll

### Stage 4 — Case Study Pages
- [ ] Shared case study template (HTML + CSS)
- [ ] `harmony.html` — content + images
- [ ] `billing.html` — content + images
- [ ] `enrollment.html` — content + images
- [ ] "What Shipped" image grid (Option B layout)
- [ ] Next project link wired between pages

### Stage 5 — Contact Form
- [ ] Formspree account + endpoint
- [ ] `contact-form.js` — AJAX submit
- [ ] Success + error states
- [ ] Form validation (client-side)

### Stage 6 — Performance + Polish
- [ ] Image optimization (convert to WebP)
- [ ] Lazy loading implementation
- [ ] Font preloading
- [ ] Lighthouse audit + fixes
- [ ] Accessibility audit + fixes
- [ ] Cross-browser test (Chrome, Firefox, Safari)
- [ ] Mobile responsive pass (breakpoints: 375px, 768px, 1440px)

### Stage 7 — Launch
- [ ] GitHub repo setup
- [ ] GitHub Pages enable
- [ ] Custom domain (optional)
- [ ] Final review

---

## Claude Code Agent Rules

```markdown
# AGENT RULES — Felipe Levi Portfolio

## Stack
- HTML5 + CSS3 (custom properties) + Vanilla JS (ES6+)
- No frameworks. No build tools. No npm.
- Files served directly from disk / GitHub Pages.

## Code Style
- HTML: semantic elements, BEM-ish class naming
- CSS: custom properties for all tokens, mobile-first
- JS: ES6 modules where supported, otherwise IIFE
- No inline styles except dynamic values set by JS
- Comments on every non-obvious block

## Design Fidelity
- All colors from --variable-name tokens only. Never hardcode hex.
- All spacing from --space-N tokens only.
- All border radii from --radius-N tokens only.
- Typography: Fraunces Bold for display/headings, Inter Regular/Medium for body.

## Hero Interaction
- Character grid must match exact spec: 57px cell, 115px line height, 22 cols, 6 rows
- Headline on rows 2 and 3 (0-indexed), left-aligned at x=80px
- Grid centered vertically between nav bottom and subtitle top
- prefers-reduced-motion: skip animation, show headline immediately

## Accessibility
- Every image needs alt text
- Every form field needs a label
- Focus states must be visible
- Run axe-core check before marking any stage done

## Performance
- Images: WebP, lazy loaded (except hero)
- Fonts: preloaded, font-display: swap
- No render-blocking resources
- Target: LH 95+ performance

## File naming
- Lowercase, hyphenated: `hero-reveal.js`, `case-study.css`
- No spaces, no camelCase for files

## Git
- Commit after each stage is complete
- Commit message format: "Stage N: description"
- Never commit broken states
```

---

## Content Reference

### Homepage

**Opening line:** "I'm a product designer who figures it out."
**Subtitle:** "Design is a series of decisions made under real constraints. I make them, ship them, and improve them."

**About:** "I'm a product designer based in Brasília, Brazil, with ten years of experience across brand, editorial, and digital product. I'm competitive by nature — I train every day, I set hard goals, and I don't do either halfway. That same instinct is what I bring to design: I show up, I figure it out, and I don't stop until it ships."

**Footer:** "Found what you were looking for?" + "Download CV ↓"

### Case Cards

| # | Tag | Title | Hook | Stat | Stat Label |
|---|-----|-------|------|------|-----------|
| 01 | DESIGN SYSTEM | Harmony | Five platforms, four years of diverging decisions. We built the system that made good design durable. | 50% | faster delivery |
| 02 | PRODUCT DESIGN | Billing & Debt Recovery | Debt negotiation was a phone call. We made it a five-minute self-service flow — recovering BRL 4.5M in the first year alone. | BRL 4.5M | recovered in year one |
| 03 | UX RESEARCH & DESIGN | Enrollment Journey | Most users were abandoning mid-flow and calling a human to finish. We fixed that. Enrollments grew 171% in a year. | 171% | more enrollments |

### Contact

**Question:** "Have a project in mind?"
**Headline:** "Let's work together."
**Email:** fplevi@gmail.com
**LinkedIn:** linkedin.com/in/fplevi

---

## Assets Needed (Felipe to Provide)

- [ ] Photo (Felipe's AI-generated photo, dark background)
- [ ] CV/Resume PDF for download
- [ ] Product screenshots for each case study:
  - Harmony: Figma library overview + component in context + live product screen
  - Billing: Participant flow screens + back-office dashboard
  - Enrollment: Enrollment flow screens + status/notification screens
- [ ] Favicon (can be generated from "F" in accent color)

---

## Questions Before Starting

None — plan is complete. Start with Stage 1.
