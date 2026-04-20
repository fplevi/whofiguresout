# Felipe Levi — Portfolio

Personal portfolio built entirely with AI assistance. Every layer of the project — from concept to code — was made in collaboration with AI tools.

---

## How this was made

This project started as an experiment: could I build a production-quality portfolio end-to-end using only AI tools, without writing a single line of code by hand?

The answer was yes.

**Ideation and structure** were defined with Claude. The information architecture, section order, content hierarchy, and copywriting all came out of conversations — not a brief handed to a developer.

**Sketches and high-fidelity frames** were produced with Claude. Layout decisions, component design, spacing systems, and visual language were iterated directly in the design tool through AI prompts.

**Hero images and case study visuals** were generated with Google Flow — the GIFs and PNGs showing product walkthroughs and UI screens were created without traditional screen recording or manual asset production.

**Animations** were built with Jitter, then integrated into the static site.

**The code** — every HTML file, every CSS rule, every JavaScript interaction — was written by Claude Code (Anthropic's CLI). No template was used. The codebase was built from scratch across 17 staged commits, each one a deliberate step: design tokens, layout system, hero animations, scroll effects, responsive behavior, case study pages, before/after sliders, parallax, and image integration.

---

## Key decisions

**No framework, no build step.** The site is plain HTML, CSS, and vanilla JS. Fast to load, easy to maintain, zero dependencies.

**Design tokens as the foundation.** All spacing, typography, color, and radius values live in `tokens.css`. Every component references them — consistency is structural, not manual.

**CSS custom properties for theming.** The visual system is controlled by a single token file, making global changes a one-line edit.

**Scroll animations without a library.** Entrance animations, nav fill-on-scroll, and the photo parallax effect are all driven by `IntersectionObserver` and `requestAnimationFrame` — no GSAP, no ScrollTrigger.

**Before/after comparison slider built natively.** The enrollment case study uses a `clip-path` approach driven by a range input — no third-party slider library.

**Proportional images everywhere.** Case study images use `aspect-ratio` or natural sizing (`width: 100%; height: auto`) so they never crop or distort at any viewport width.

**Semantic, accessible HTML.** ARIA labels, landmark roles, skip links, and reduced-motion support are built in from the start — not retrofitted.

---

## Structure

```
felipelevi/
├── index.html                  — Homepage (hero, work, contact, about)
├── case-studies/
│   ├── billing.html            — Billing & Debt Recovery
│   ├── enrollment.html         — Enrollment Journey
│   └── harmony.html            — Harmony Design System
├── assets/
│   ├── css/
│   │   ├── tokens.css          — Design tokens (spacing, type, color)
│   │   ├── global.css          — Base styles and utilities
│   │   ├── nav.css             — Navigation and scroll state
│   │   ├── hero.css            — Hero grid and reveal animation
│   │   ├── cards.css           — Work cards
│   │   ├── case-study.css      — Shared case study layout
│   │   ├── contact.css         — Contact section and form
│   │   └── footer.css          — About, photo, footer
│   ├── js/
│   │   ├── hero-reveal.js      — Hero text reveal on load
│   │   ├── scroll-animations.js — Nav scroll, card entrances, parallax, compare slider
│   │   └── contact-form.js     — Form submission via Formspree
│   └── images/                 — Case study assets (GIFs, PNGs)
```

---

## Tools used

| Layer | Tool |
|---|---|
| Ideation, copy, code | Claude (Anthropic) |
| High-fidelity design | Claude |
| Hero images & GIFs | Google Flow |
| Animations | Jitter |
| Form handling | Formspree |
