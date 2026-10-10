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
