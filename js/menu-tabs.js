const tabs   = document.querySelectorAll('.tab-btn');
const panels = document.querySelectorAll('.tab-panel');

tabs.forEach(btn => {
  btn.addEventListener('click', () => {
    tabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
    panels.forEach(p => { p.hidden = true; });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    document.getElementById('tab-' + btn.dataset.tab).hidden = false;
  });
});

const fishChips = document.querySelectorAll('.fish-chip');
const fishItems = document.querySelectorAll('#tab-fish .menu-card, #tab-fish .menu-group-label');

fishChips.forEach(chip => {
  chip.addEventListener('click', () => {
    fishChips.forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    const filter = chip.dataset.fishFilter;
    fishItems.forEach(item => {
      const show = filter === 'all' || item.classList.contains('fish-' + filter);
      item.classList.toggle('fish-hide', !show);
    });
  });
});
