# Menu Sync Checklist

Run this whenever Arpan updates the Google Sheet ("Bangal Ekhane Menu List") and asks
for the changes to go live. Sync is on-request, not automatic — see the workflow
decision this follows.

## 1. Read the sheet
- Open the sheet and check `modifiedTime` against the last sync to confirm there's
  actually something new.
- Read the **main restaurant menu table** only. Ignore the smaller second table on
  the same sheet — that's the separate stall menu (different portions/pricing),
  mapped to `stall-menu.pdf`, not the website.

## 2. Diff against the live site
For every section (Starter, Fish, Chicken, Mutton, Combo, Veg, Dal, Rice, Roti,
Sweets, Chatni, Chef's Special), compare the sheet row-by-row against the
`menu-card` divs in `index.html`:
- Item name (English + Bengali)
- Qty/portion note
- Price
- Veg/non-veg badge (not stated in the sheet — infer from the dish, e.g. Bengali
  sweets and Samosa are veg)

Known intentional divergence: some items sit in a different tab on the site than
in the sheet (e.g. Egg Roll, Egg Chicken Roll, Luchi and Aloo Dam are filed under
Chef's Special on the site but under Starter/Combo in the sheet). That's a prior
reorganization, not a data error — don't "fix" it back. Only flag it if the price
no longer matches.

## 3. Edit `index.html`
Add/update the affected `menu-card` divs directly. This is the source of truth the
PDF and carousels are generated from.

## 4. Regenerate the downloadable PDF
```
cp index.html <tmp>/index.html          # extract_menu.py reads a relative path
python3 extract_menu.py > menu_data.json
python3 build_menu_pdf.py               # writes menu_preview.html
<Chrome> --headless --disable-gpu --print-to-pdf=Bangla_Ekhane_Menu.pdf \
  --no-pdf-header-footer --run-all-compositor-stages-before-draw \
  --virtual-time-budget=10000 file://.../menu_preview.html
```
Verify before copying into the repo:
- `pdfinfo` → still 4 pages, A4
- `pdftotext` → new/changed item names show up
- `pdftoppm` the affected page → visually confirm no overflow/clipping, correct
  veg/non-veg badge colors
- Copy to `assets/menu/Bangla_Ekhane_Menu.pdf`

## 5. Regenerate carousel collateral (if it exists downstream)
The `full-menu-story` (and `full-menu-square`) Instagram/WhatsApp carousels in
`~/Downloads/bangla-ekhane-collaterals/carousel-slides/` are generated from the
same `menu_data.json`, via `build_carousel_v2.py`. Only the middle data-driven
slides need regenerating — slide 1 (title) and the last slide (CTA) are static.
Regenerate, convert PNG→JPG, visually spot-check the affected slide, then replace
in the Downloads folder. These are offline/print collateral, not part of the repo.

## 6. Ship
- `git fetch origin arpan-feedback` and confirm this branch is a clean fast-forward
  (no divergence) before pushing.
- Commit `index.html` + the regenerated PDF together.
- Push directly to `arpan-feedback` (no PR — see deploy workflow).
- Spot-check the live site (`curl` or browser) once GitHub Pages picks it up.

## Related
- Menu sync is sync-on-request, not a live feed from the Sheet (see
  `menu_sync_workflow` decision).
- Deploys go straight to `arpan-feedback`, no PR (see deploy workflow).
