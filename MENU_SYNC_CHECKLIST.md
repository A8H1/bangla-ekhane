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

## 2. Diff against `menu/menu.json`
`menu/menu.json` is now the single source of truth for the menu. Both the
downloadable PDF and the website's menu tabs are generated from it, so they can
no longer drift apart. For every section, compare the sheet row-by-row against
`menu.json`:
- Item name (English + Bengali `bn`)
- Qty/portion note (`qty`, written as it should print, e.g. `1 pc`, `3+3 pcs`, `Plate`)
- Price (dine-in price only; Swiggy/Zomato prices are not shown)
- Veg/non-veg (`veg: true/false`; eggs count as non-veg)

Fish dishes also carry a `group` (katla, rohu, hilsa, pabda, bhetki, prawn) that
drives the website's fish filter chips.

## 3. Edit `menu/menu.json`
Add/update/remove items in the right section, in the order they should appear.
Sections appear in the PDF and on the site in the order listed. `pdf_pages`
says which sections go on which PDF page (page 4, the illustrated thali guide,
is inserted unchanged from `menu/assets/thali-guide-page.pdf`).

## 4. Rebuild
```
python3 menu/build_menu.py
```
This rewrites `assets/menu/Bangla_Ekhane_Menu.pdf` and the menu tabs in
`index.html` (between the `MENU-TABS` / `MENU-PANELS` markers — don't hand-edit
inside them). Needs Python 3 with `playwright` (Chrome/Chromium) and `pikepdf`.
If a page overflows, the build stops and names the page: move a section to
another page in `pdf_pages`.

Verify before shipping:
- `pdftotext -layout assets/menu/Bangla_Ekhane_Menu.pdf -` → new/changed items show up
- `pdftoppm` the affected page → visually confirm layout
- open `index.html` → click the affected tab

## 5. Regenerate carousel collateral (if it exists downstream)
The `full-menu-story` (and `full-menu-square`) Instagram/WhatsApp carousels in
`~/Downloads/bangla-ekhane-collaterals/carousel-slides/` are generated from the
same menu data (now `menu/menu.json`), via `build_carousel_v2.py`. Only the middle data-driven
slides need regenerating — slide 1 (title) and the last slide (CTA) are static.
Regenerate, convert PNG→JPG, visually spot-check the affected slide, then replace
in the Downloads folder. These are offline/print collateral, not part of the repo.

## 6. Ship
- `git fetch origin arpan-feedback` and confirm this branch is a clean fast-forward
  (no divergence) before pushing.
- Commit `menu/menu.json`, `index.html` and the regenerated PDF together.
- Push directly to `arpan-feedback` (no PR — see deploy workflow).
- Spot-check the live site (`curl` or browser) once GitHub Pages picks it up.

## Related
- Menu sync is sync-on-request, not a live feed from the Sheet (see
  `menu_sync_workflow` decision).
- Deploys go straight to `arpan-feedback`, no PR (see deploy workflow).
