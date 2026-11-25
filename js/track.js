// Sends a Google Analytics event when someone taps an order, call, WhatsApp,
// directions, review or menu-download link, so orders and enquiries from the
// site show up in Analytics (Reports > Engagement > Events).
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a || typeof gtag !== 'function') return;
  var h = a.getAttribute('href'), name = null, p = {};
  if (h.indexOf('wa.me') > -1) {
    name = 'whatsapp_click';
    p.purpose = /catering/i.test(decodeURIComponent(h)) ? 'catering' : 'takeaway';
  } else if (h.indexOf('tel:') === 0) {
    name = 'call_click';
  } else if (/swiggy|zomato|ownly/i.test(h)) {
    name = 'order_click';
    p.platform = (h.match(/swiggy|zomato|ownly/i) || [''])[0].toLowerCase();
  } else if (/district\.in/i.test(h)) {
    name = 'book_table_click';
  } else if (/maps\.app\.goo\.gl|google\.com\/maps/i.test(h)) {
    name = 'directions_click';
  } else if (/writereview/i.test(h)) {
    name = 'review_click';
  } else if (/\.pdf($|\?)/i.test(h)) {
    name = 'menu_download';
  } else if (/instagram\.com|youtube\.com/i.test(h)) {
    name = 'social_click';
    p.platform = /youtube/i.test(h) ? 'youtube' : 'instagram';
  }
  if (!name) return;
  p.link_location = (a.closest('section, footer, nav, [id$="-float"]') || {}).id || 'page';
  gtag('event', name, p);
}, true);
