const stars      = document.querySelectorAll('.star');
const ratingInput = document.getElementById('fb-rating');
const form        = document.getElementById('feedback-form');
const toast       = document.getElementById('feedback-toast');
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
  const data = new FormData(form);
  try {
    await fetch('/', {
      method: 'POST',
      body: new URLSearchParams(data).toString(),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  } catch (_) { /* offline / local dev — show toast anyway */ }

  showToast();
  form.reset();
  selected = 0;
  ratingInput.value = '';
  highlight(0);
});
