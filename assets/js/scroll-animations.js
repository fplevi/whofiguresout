const nav = document.getElementById('nav');
const hero = document.getElementById('hero');

// Nav background fill on scroll past hero
function initNavScroll() {
  if (!nav || !hero) return;

  const observer = new IntersectionObserver(
    ([entry]) => {
      nav.classList.toggle('scrolled', !entry.isIntersecting);
    },
    { threshold: 0, rootMargin: `-64px 0px 0px 0px` }
  );

  observer.observe(hero);
}

// Cards entrance animation
function initCardAnimations() {
  const cards = document.querySelectorAll('.case-card');
  if (!cards.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          const delay = Array.from(cards).indexOf(entry.target) * 120;
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, delay);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transition = `opacity 600ms ease-out, transform 600ms ease-out`;
    observer.observe(card);
  });
}

// Section entrance animations
function initSectionAnimations() {
  const sections = document.querySelectorAll('.contact, .about, .photo-name, .footer, .cs-section');
  if (!sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 }
  );

  sections.forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(16px)';
    section.style.transition = 'opacity 500ms ease-out, transform 500ms ease-out';
    observer.observe(section);
  });
}

// Skip animations if user prefers reduced motion
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  initNavScroll();
  initCardAnimations();
  initSectionAnimations();
} else {
  // Still init nav scroll (no animation, just class toggle)
  initNavScroll();
  // Make everything visible immediately
  document.querySelectorAll('.case-card, .contact, .about, .photo-name, .footer, .cs-section').forEach(el => {
    el.style.opacity = '1';
    el.style.transform = 'none';
  });
}
