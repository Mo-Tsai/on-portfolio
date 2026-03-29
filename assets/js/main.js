/* ON Design Lab — Shared JS */
document.addEventListener('DOMContentLoaded', () => {
  // Nav active state
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      a.classList.add('active');
    }
  });
});
