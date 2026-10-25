// The case header's Back button acts like the browser's Back, returning to the page
// (and scroll position) the visitor came from: the home or another case.
// Without a previous page on this site in this tab (arrived from outside, or opened
// in a new tab), it keeps its href and goes to the home's work section instead.
const back = document.querySelector('.cs-header__back');
const cameFromSite = () => {
  try {
    return history.length > 1 && new URL(document.referrer).origin === location.origin;
  } catch {
    return false;
  }
};

back?.addEventListener('click', (event) => {
  if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  if (!cameFromSite()) return;
  event.preventDefault();
  history.back();
});
