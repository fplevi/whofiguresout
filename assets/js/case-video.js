// Evidence videos autoplay muted in the markup, so they play even without this script.
// Here they skip their recorded page load (data-start, in seconds) and pause off screen.
// With reduced motion they stop on the poster and offer controls instead.
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const observer = new IntersectionObserver((entries) => {
  for (const { target: video, isIntersecting } of entries) {
    if (isIntersecting) video.play().catch(() => { video.controls = true; });
    else video.pause();
  }
}, { threshold: 0.25 });

for (const video of document.querySelectorAll('video[data-start]')) {
  const start = Number(video.dataset.start);
  // Jump back before the end, so the native loop never shows the page load at 0.
  // Servers without Range requests can't seek: then the video plays from 0 instead of freezing.
  const canSeek = () => video.seekable.length > 0 && video.seekable.end(0) > start;
  const keepInRange = () => {
    if (!canSeek()) return;
    if (video.currentTime < start || video.currentTime > video.duration - 0.3) video.currentTime = start;
  };
  video.addEventListener('timeupdate', keepInRange);
  if (video.readyState >= 1) keepInRange();
  else video.addEventListener('loadedmetadata', keepInRange, { once: true });

  if (reduced) {
    video.removeAttribute('autoplay');
    video.pause();
    video.controls = true;
  } else {
    observer.observe(video);
  }
}
