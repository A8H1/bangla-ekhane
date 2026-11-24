const navbar    = document.getElementById('navbar');
const hamburger = document.getElementById('nav-hamburger');
const navLinks  = document.getElementById('nav-links');
const announcementBar = document.querySelector('.announcement-bar');

function setAnnouncementHeight() {
  if (!announcementBar) return;
  document.documentElement.style.setProperty('--announcement-h', announcementBar.offsetHeight + 'px');
}
setAnnouncementHeight();
window.addEventListener('resize', setAnnouncementHeight);

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 10);
});

hamburger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

document.getElementById('whatsapp-float')?.addEventListener('click', () => {
  gtag?.('event', 'whatsapp_click', { event_category: 'engagement', event_label: 'float_button' });
});

document.getElementById('menu-pdf-link')?.addEventListener('click', () => {
  gtag?.('event', 'menu_pdf_download', { event_category: 'engagement' });
});

// Pop-up journey: move past stalls from "Coming up" into the row, count stalls/communities, wire arrows.
(() => {
  const up = document.querySelector('.pop-upcoming'), row = document.querySelector('.pop-row');
  if (!up || !row) return;
  const now = Date.now();
  [...up.querySelectorAll('.pop-ticket[data-date]')].forEach(t => {
    if (now > new Date(t.dataset.date + 'T23:59:59+05:30')) {
      const later = [...row.children].find(r => r.dataset.date < t.dataset.date);
      row.insertBefore(t, later || null);
    }
  });
  if (!up.children.length) up.closest('.pop-up-wrap').hidden = true;
  const stalls = row.querySelectorAll('.pop-ticket');
  const names = new Set();
  stalls.forEach(t => t.querySelector('h3').textContent.split(/,|&/).forEach(n => n.trim() && names.add(n.trim())));
  document.querySelector('.pop-n-stalls').textContent = stalls.length;
  document.querySelector('.pop-n-comm').textContent = names.size;
  const prev = document.querySelector('.pop-arrow.prev'), next = document.querySelector('.pop-arrow.next');
  const step = () => (row.querySelector('.pop-ticket')?.offsetWidth || 236) + 14;
  const sync = () => {
    prev.disabled = row.scrollLeft < 10;
    next.disabled = row.scrollLeft + row.clientWidth > row.scrollWidth - 10;
  };
  prev.addEventListener('click', () => row.scrollBy({ left: -step() * 2 }));
  next.addEventListener('click', () => row.scrollBy({ left: step() * 2 }));
  row.addEventListener('scroll', sync, { passive: true });
  window.addEventListener('resize', sync);
  sync();
})();
