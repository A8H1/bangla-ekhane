const vid        = document.getElementById('promo-vid');
const btn        = document.getElementById('vid-unmute');
const iconMuted  = document.getElementById('icon-muted');
const iconSound  = document.getElementById('icon-unmuted');

btn.addEventListener('click', () => {
  vid.muted = !vid.muted;
  iconMuted.style.display = vid.muted ? 'block' : 'none';
  iconSound.style.display = vid.muted ? 'none'  : 'block';
});
