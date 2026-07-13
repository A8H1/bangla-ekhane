const stars        = document.querySelectorAll('.star');
const ratingInput  = document.getElementById('fb-rating');
const priorityInput = document.getElementById('fb-priority');
const form         = document.getElementById('feedback-form');
const toast        = document.getElementById('feedback-toast');
const thanksPanel  = document.getElementById('feedback-thanks');
const againLink    = document.getElementById('feedback-again');
let selected = 0;

function highlight(val) {
  stars.forEach(s => s.classList.toggle('active', Number(s.dataset.value) <= Number(val)));
}

stars.forEach(star => {
  star.addEventListener('mouseover', () => highlight(star.dataset.value));
  star.addEventListener('mouseout',  () => highlight(selected));
  star.addEventListener('click', () => {
    selected = star.dataset.value;
    ratingInput.value = selected;
    highlight(selected);
  });
});

function showToast() {
  toast.classList.remove('hide');
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
    toast.classList.add('hide');
  }, 3000);
}

form.addEventListener('submit', async e => {
  e.preventDefault();

  // Flag low ratings so they stand out in the email notification —
  // every rating still gets the same Google review nudge below,
  // this only changes what lands in our inbox.
  priorityInput.value = Number(ratingInput.value) <= 3
    ? '⚠️ LOW RATING — follow up directly, do not rely on a public review'
    : '';

  const data = new FormData(form);
  try {
    await fetch('/', {
      method: 'POST',
      body: new URLSearchParams(data).toString(),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  } catch (_) { /* offline / local dev — show confirmation anyway */ }

  showToast();
  form.hidden = true;
  thanksPanel.hidden = false;
  form.reset();
  selected = 0;
  ratingInput.value = '';
  priorityInput.value = '';
  highlight(0);
});

againLink.addEventListener('click', e => {
  e.preventDefault();
  thanksPanel.hidden = true;
  form.hidden = false;
});
