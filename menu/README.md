# Menu source

`menu.json` holds every dish (English name, Bengali name, portion, price, veg/non-veg)
for the Bangla Ekhane dine-in menu. Run

    python3 menu/build_menu.py

to regenerate both the downloadable PDF (`assets/menu/Bangla_Ekhane_Menu.pdf`) and the
menu tabs on the website (`index.html`). See `MENU_SYNC_CHECKLIST.md` for the full routine.

- `build_menu.py` – the template and build script (A4 pages, two columns, the original design)
- `assets/background.jpg` – paper texture and Baul illustration
- `assets/logo.png` – round logo
- `assets/thali-guide-page.pdf` – page 4 (illustrated "Our Thalis" guide), inserted as-is
- `fonts/` – Lora, Marcellus, Galada, Tiro Bangla and a ₹ glyph from Noto Serif Bengali,
  all under the SIL Open Font License (`OFL.txt`, `OFL-NotoSerifBengali.txt`)
