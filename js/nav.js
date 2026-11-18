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

// Drop the "Upcoming" badge once a pop-up's date has passed.
document.querySelectorAll('.timeline-item.is-upcoming[data-event-date]').forEach(el => {
  const end = new Date(el.dataset.eventDate + 'T23:59:59+05:30');
  if (Date.now() > end) {
    el.classList.remove('is-upcoming');
    el.querySelector('.timeline-badge')?.remove();
  }
});
