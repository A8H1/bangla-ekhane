const LAUNCH = new Date('2026-07-15T11:00:00+05:30').getTime();

const elDays    = document.getElementById('cd-days');
const elHours   = document.getElementById('cd-hours');
const elMins    = document.getElementById('cd-mins');
const elSecs    = document.getElementById('cd-secs');
const heroLaunch = document.getElementById('hero-launch');
const heroOpen   = document.getElementById('hero-open');

function pad(n) { return String(n).padStart(2, '0'); }

function tick() {
  const diff = LAUNCH - Date.now();
  if (diff <= 0) {
    heroLaunch.hidden = true;
    heroOpen.hidden   = false;
    return;
  }
  elDays.textContent  = pad(Math.floor(diff / 86400000));
  elHours.textContent = pad(Math.floor((diff % 86400000) / 3600000));
  elMins.textContent  = pad(Math.floor((diff % 3600000)  / 60000));
  elSecs.textContent  = pad(Math.floor((diff % 60000)    / 1000));
}

tick();
setInterval(tick, 1000);
