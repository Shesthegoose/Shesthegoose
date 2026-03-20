/* ============================================================
   SHE'S THE GOOSE — SCRIPT.JS
   ============================================================
   1. Loads all section files via fetch (data-include system)
   2. Runs scroll-reveal animation after sections load
   ============================================================ */


/* ── SECTION LOADER ───────────────────────────────────────── */

async function loadSections() {
  const includes = document.querySelectorAll('[data-include]');

  const promises = Array.from(includes).map(async (el) => {
    const file = el.getAttribute('data-include');
    try {
      const response = await fetch(file);
      if (!response.ok) throw new Error(`Could not load ${file}`);
      const html = await response.text();
      el.innerHTML = html;
    } catch (err) {
      console.warn(err.message);
    }
  });

  await Promise.all(promises);

  // After all sections are loaded, start scroll animations
  initScrollReveal();
}


/* ── SCROLL REVEAL ────────────────────────────────────────── */

function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.reveal').forEach((el) => {
    observer.observe(el);
  });
}


/* ── INIT ─────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', loadSections);
