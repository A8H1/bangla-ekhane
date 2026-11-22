#!/usr/bin/env python3
"""Build the Bangla Ekhane dine-in menu PDF (and the website menu tabs) from menu.json.

    python3 menu/build_menu.py            # rebuild PDF + website menu
    python3 menu/build_menu.py --pdf-only
    python3 menu/build_menu.py --web-only

menu.json is the single source of truth: edit a dish, price or section there,
run this script, and both assets/menu/Bangla_Ekhane_Menu.pdf and the menu tabs
in index.html are regenerated to match.

Needs: Python 3, playwright (with a Chromium/Chrome browser) and pikepdf for
the PDF step. The website step needs nothing extra.
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MENU = ROOT / "menu"
DATA = json.loads((MENU / "menu.json").read_text(encoding="utf-8"))
OUT_PDF = ROOT / "assets/menu/Bangla_Ekhane_Menu.pdf"
INDEX = ROOT / "index.html"

e = lambda s: html.escape(str(s), quote=False)
SECTIONS = {s["id"]: s for s in DATA["sections"]}


def qty_pdf(q):
    return q


# ───────────────────────── PDF ─────────────────────────
CSS = """
@font-face { font-family: LoraName; src: url('fonts/Lora-Name.ttf'); }
@font-face { font-family: LoraPrice; src: url('fonts/Lora-Price.ttf'); }
@font-face { font-family: LoraItalic; src: url('fonts/Lora-Italic.ttf'); }
@font-face { font-family: RupeeSerif; src: url('fonts/RupeeSerif.ttf'); }
@font-face { font-family: Galada; src: url('fonts/Galada-Regular.ttf'); }
@font-face { font-family: Marcellus; src: url('fonts/Marcellus-Regular.ttf'); }
@font-face { font-family: Tiro; src: url('fonts/TiroBangla-Regular.ttf'); }
@page { size: 595.5pt 842.25pt; margin: 0; }
:root {
  --paper:#fbf4e4; --maroon:#5b1213; --title:#5a1616; --ink:#392819; --bn:#3b2a1b;
  --qty:#8c7040; --label:#7f6336; --rule:#d4b57c; --dot:#cdb98f; --divider:#e2d1a6;
  --green:#27733b; --red:#8c1d1d; --frame-out:#4f1c19; --frame-in:#b6965b;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--paper); }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { position: relative; width: 595.5pt; height: 842.25pt; overflow: hidden; page-break-after: always;
  background: var(--paper) url('assets/background.jpg') center / 100% 100% no-repeat; color: var(--ink); }
.page:last-child { page-break-after: auto; }
.frame { position: absolute; inset: 10.5pt; border: 0.75pt solid var(--frame-out); }
.frame::after { content: ''; position: absolute; inset: 3pt; border: 0.75pt solid var(--frame-in); }

/* running header (inner pages) */
.hdr { position: absolute; left: 33pt; right: 33pt; top: 27pt; height: 30pt; display: flex; align-items: center;
  border-bottom: 0.75pt solid var(--rule); padding-bottom: 3pt; }
.hdr img { width: 25pt; height: 25pt; margin-right: 8pt; }
.hdr .en { font: 14pt Marcellus; color: var(--title); letter-spacing: .02em; }
.hdr .bnl { font: 15pt Galada; color: var(--maroon); margin-left: 8pt; position: relative; top: 1pt; }
.hdr .tag { margin-left: auto; font: 8.6pt Marcellus; color: var(--label); letter-spacing: .32em; margin-right: -.32em; }

/* footer */
.ftr { position: absolute; left: 33pt; right: 33pt; top: 798pt; border-top: 0.75pt solid var(--rule);
  padding-top: 6pt; display: flex; justify-content: space-between; align-items: flex-start;
  font: 9pt Marcellus; color: var(--ink); }
.ftr .url { color: var(--label); letter-spacing: .08em; }
.ftr .tagline { font: 8.5pt Tiro; color: var(--maroon); }
.ftr .r { text-align: right; }

/* content columns */
.cols { position: absolute; left: 33pt; right: 33pt; column-count: 2; column-gap: 25.5pt;
  column-fill: auto; column-rule: 0.75pt solid var(--divider); }
.sec { break-inside: auto; }
.sec + .sec { margin-top: 10pt; }
.sec-h { display: flex; align-items: baseline; justify-content: space-between; border-bottom: 0.75pt solid var(--rule);
  padding-bottom: 2.5pt; break-after: avoid; }
.sec-h .t { font: 22.5pt/1.2 Galada; color: var(--maroon); }
.sec-h .l { font: 8pt Marcellus; color: var(--label); letter-spacing: .3em; margin-right: -.3em; }
.grp { display: flex; align-items: center; gap: 5pt; margin: 7pt 0 .5pt; break-after: avoid;
  font: 8.4pt Marcellus; letter-spacing: .22em; }
.grp .b { font: 9pt Tiro; letter-spacing: 0; }
.grp.v { color: var(--green); } .grp.n { color: var(--red); }
.badge { flex: none; width: 8.6pt; height: 8.6pt; border: 0.9pt solid; display: inline-flex; align-items: center; justify-content: center; }
.badge.v { border-color: var(--green); } .badge.v::after { content:''; width: 3.6pt; height: 3.6pt; border-radius: 50%; background: var(--green); }
.badge.n { border-color: #7a2a24; } .badge.n::after { content:''; width:0; height:0; border-left: 2.3pt solid transparent;
  border-right: 2.3pt solid transparent; border-bottom: 3.9pt solid var(--red); margin-top: -.6pt; }
.it { display: grid; grid-template-columns: 15.8pt 1fr auto; align-items: start; padding: 4pt 0 3.4pt;
  border-bottom: 0.75pt dotted var(--dot); break-inside: avoid; }
.it .badge { margin-top: 2.2pt; }
.nm { font: 12.3pt/14.2pt LoraName; color: var(--ink); }
.nm .q { font: 9.3pt LoraItalic; color: var(--qty); }
.nm .nw { white-space: nowrap; }
.bn { font: 10.4pt/12.4pt Tiro; color: var(--bn); margin-top: 0; }
.pr { font: 13.2pt/14.2pt RupeeSerif, LoraPrice; color: var(--maroon); letter-spacing: .07em; padding-left: 8pt; white-space: nowrap; }

/* cover */
.cover-logo { position: absolute; left: 50%; top: 34pt; width: 88pt; height: 88pt; transform: translateX(-50%); }
.cover-en { position: absolute; left: 0; right: 0; top: 128pt; text-align: center; font: 37pt Marcellus; color: var(--title); letter-spacing: .02em; }
.cover-bn { position: absolute; left: 0; right: 0; top: 168pt; text-align: center; font: 31pt Galada; color: var(--maroon); }
.cover-tag { position: absolute; left: 0; right: 0; top: 215.5pt; text-align: center; font: 9.4pt Marcellus; color: var(--label); letter-spacing: .42em; }
.orn { position: absolute; left: 33pt; right: 33pt; top: 241pt; height: 24pt; display: flex; align-items: center; gap: 10pt; }
.orn::before, .orn::after { content: ''; flex: 1; border-top: 0.75pt solid var(--rule); }
.orn svg { width: 24pt; height: 24pt; }
.legend { position: absolute; left: 0; right: 0; top: 762pt; display: flex; justify-content: center; gap: 22pt;
  font: 8.4pt Marcellus; color: var(--ink); }
.legend span { display: inline-flex; align-items: center; gap: 6pt; }
"""

ORNAMENT = """<svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="22" fill="none" stroke="#c9a45c" stroke-width="1.1" stroke-dasharray="1.4 2.2"/>
<g fill="none" stroke="#7a1a1a" stroke-width="1.3">""" + "".join(
    f'<path transform="rotate({a} 24 24)" d="M24 24 C20.5 18 21 11 24 6 C27 11 27.5 18 24 24Z"/>' for a in range(0, 360, 45)) + """</g>
<g fill="#e3ad3a">""" + "".join(
    f'<path transform="rotate({a} 24 24)" d="M24 24 C22.6 20 22.8 16.5 24 14 C25.2 16.5 25.4 20 24 24Z"/>' for a in range(22, 382, 45)) + """</g>
<circle cx="24" cy="24" r="2.6" fill="#7a1a1a"/></svg>"""


def item_html(it):
    q = f'<span class="q">&nbsp;· <span class="nw">{e(it["qty"])}</span></span>' if it.get("qty") else ""
    return (f'<div class="it"><span class="badge {"v" if it["veg"] else "n"}"></span>'
            f'<div><div class="nm">{e(it["name"])}{q}</div><div class="bn">{e(it["bn"])}</div></div>'
            f'<div class="pr">₹{it["price"]}</div></div>')


def section_html(s):
    out = [f'<div class="sec"><div class="sec-h"><span class="t">{e(s["bn"])}</span><span class="l">{e(s["label"])}</span></div>']
    for veg, en, bn in ((True, "VEG", "নিরামিষ"), (False, "NON-VEG", "আমিষ")):
        items = [i for i in s["items"] if i["veg"] == veg]
        if not items:
            continue
        cls = "v" if veg else "n"
        out.append(f'<div class="grp {cls}"><span class="badge {cls}"></span>{en}<span class="b">· {bn}</span></div>')
        out += [item_html(i) for i in items]
    out.append("</div>")
    return "".join(out)


FOOT_ADDR = "CSK Mall, Gunjur, Bengaluru"
FOOT_CALL = "Call / WhatsApp 82403 80848"


def page_html(n, sections, cover=False):
    body = ['<div class="frame"></div>']
    if cover:
        body += ['<img class="cover-logo" src="assets/logo.png">',
                 '<div class="cover-en">Bangla Ekhane</div>', '<div class="cover-bn">বাংলা এখানে</div>',
                 '<div class="cover-tag">TASTE OF BENGAL · DINE-IN MENU</div>', f'<div class="orn">{ORNAMENT}</div>']
        top, bottom = 272, 748
        body.append('<div class="legend"><span><span class="badge v"></span>Vegetarian</span>'
                    '<span><span class="badge n"></span>Non-vegetarian (incl. egg)</span></div>')
        body.append(f'<div class="ftr" style="top:781pt"><div>{FOOT_ADDR}<br>{FOOT_CALL}</div>'
                    f'<div class="r"><span class="tagline">সেরা স্বাদ · সেরা মান · সেরা অভিজ্ঞতা</span><br>'
                    f'<span class="url">banglaekhane.in · {n}</span></div></div>')
    else:
        body.append('<div class="hdr"><img src="assets/logo.png"><span class="en">Bangla Ekhane</span>'
                    '<span class="bnl">বাংলা এখানে</span><span class="tag">DINE-IN MENU</span></div>')
        top, bottom = 64, 791
        body.append(f'<div class="ftr"><div>{FOOT_ADDR} · {FOOT_CALL}</div><div class="url">banglaekhane.in · {n}</div></div>')
    body.append(f'<div class="cols" data-page="{n}" style="top:{top}pt;height:{bottom - top}pt">'
                + "".join(section_html(SECTIONS[s]) for s in sections) + "</div>")
    return f'<div class="page">{"".join(body)}</div>'


OVERFLOW_JS = """[...document.querySelectorAll('.cols')].filter(c => { const r = c.getBoundingClientRect();
  return [...c.querySelectorAll('.it, .sec-h, .grp')].some(el => { const b = el.getBoundingClientRect();
    return b.right > r.right + 1 || b.bottom > r.bottom + 1; }); }).map(c => c.dataset.page)"""


def build_pdf():
    from playwright.sync_api import sync_playwright
    import pikepdf
    layout = DATA["pdf_pages"]  # list of {"page": n, "sections": [...], "cover": bool} or {"page": n, "insert": file}
    pages = [page_html(p["page"], p["sections"], p.get("cover", False)) for p in layout if "sections" in p]
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    tmp = MENU / "_menu_render.html"
    tmp.write_text(doc, encoding="utf-8")
    tmp_pdf = MENU / "_menu_render.pdf"
    try:
        with sync_playwright() as pw:
            kw = {}
            for exe in ("/usr/bin/google-chrome", "/usr/bin/chromium"):
                if Path(exe).exists():
                    kw["executable_path"] = exe
                    break
            b = pw.chromium.launch(**kw)
            pg = b.new_page()
            pg.goto(tmp.as_uri(), wait_until="load")
            pg.evaluate("document.fonts.ready")
            over = pg.evaluate(OVERFLOW_JS)
            if over:
                raise SystemExit(f"Content does not fit on PDF page(s) {over}: move a section in menu.json 'pdf_pages'.")
            pg.pdf(path=str(tmp_pdf), prefer_css_page_size=True, print_background=True)
            b.close()
        made = pikepdf.open(tmp_pdf)
        out = pikepdf.new()
        it = iter(made.pages)
        for p in layout:
            if "insert" in p:
                ins = pikepdf.open(MENU / p["insert"])
                out.pages.extend(ins.pages)
            else:
                out.pages.append(next(it))
        out.docinfo["/Title"] = "Bangla Ekhane Dine-in Menu"
        out.save(OUT_PDF)
    finally:
        tmp.unlink(missing_ok=True)
        tmp_pdf.unlink(missing_ok=True)
    print("PDF written:", OUT_PDF.relative_to(ROOT))


# ───────────────────────── Website ─────────────────────────
FISH_LABELS = {"katla": "Katla", "rohu": "Rohu", "hilsa": "Hilsa", "pabda": "Pabda", "prawn": "Prawn", "bhetki": "Bhetki"}


def web_qty(q):
    return f' <small>({e(q)})</small>' if q else ""


def web_card(it, extra=""):
    return (f'          <div class="menu-card{extra}"><span class="badge badge-{"veg" if it["veg"] else "nonveg"}"></span>'
            f'<div><h3>{e(it["name"])}{web_qty(it.get("qty"))}</h3><p class="menu-bengali">{e(it["bn"])}</p>'
            f'<p class="menu-price">₹{it["price"]}</p></div></div>')


def build_web():
    src = INDEX.read_text(encoding="utf-8")
    secs = DATA["sections"]
    tabs = [f'        <button class="tab-btn{" active" if i == 0 else ""}" data-tab="{s["id"]}" role="tab" '
            f'aria-selected="{"true" if i == 0 else "false"}">{e(s["bn"])} · {e(s["en"])}</button>' for i, s in enumerate(secs)]
    panels = []
    for i, s in enumerate(secs):
        p = [f'      <!-- {e(s["en"])} -->', f'      <div class="tab-panel" id="tab-{s["id"]}"{"" if i == 0 else " hidden"}>']
        groups = [g for g in dict.fromkeys(it.get("group") for it in s["items"]) if g]
        if groups:
            p.append('        <div class="fish-filters" role="tablist">')
            p.append('          <button class="fish-chip active" data-fish-filter="all">All</button>')
            p += [f'          <button class="fish-chip" data-fish-filter="{g}">{FISH_LABELS.get(g, g.title())}</button>' for g in groups]
            p.append('        </div>')
        p.append('        <div class="menu-grid">')
        last = None
        for it in s["items"]:
            g = it.get("group")
            if groups and g != last:
                p.append(f'          <div class="menu-group-label fish-{g}"><span>{FISH_LABELS.get(g, g.title())}</span></div>')
                last = g
            p.append(web_card(it, f" fish-{g}" if g else ""))
        p += ['        </div>', '      </div>', '']
        panels.append("\n".join(p))
    tab_re = re.compile(r'(<!-- MENU-TABS:START -->\n).*?(\n\s*<!-- MENU-TABS:END -->)', re.S)
    pan_re = re.compile(r'(<!-- MENU-PANELS:START -->\n).*?(\s*<!-- MENU-PANELS:END -->)', re.S)
    if not tab_re.search(src) or not pan_re.search(src):
        raise SystemExit("index.html is missing the MENU-TABS / MENU-PANELS markers")
    src = tab_re.sub(lambda m: m.group(1) + "\n".join(tabs) + m.group(2), src)
    src = pan_re.sub(lambda m: m.group(1) + "\n".join(panels) + m.group(2), src)
    INDEX.write_text(src, encoding="utf-8")
    print("Website menu updated:", sum(len(s["items"]) for s in secs), "dishes in", len(secs), "tabs")


if __name__ == "__main__":
    args = set(sys.argv[1:])
    if "--pdf-only" not in args:
        build_web()
    if "--web-only" not in args:
        build_pdf()
