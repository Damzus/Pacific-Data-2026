from pathlib import Path
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/site/poster.html"
OUT = Path("out/poster")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1980})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(URL, wait_until="networkidle", timeout=90000)
    pg.wait_for_selector("body[data-ready='1']", timeout=90000)
    pg.wait_for_timeout(1500)

    pg.emulate_media(media="print")
    pg.pdf(path=str(OUT / "island-stays-village-goes-A1.pdf"),
           width="594mm", height="841mm", print_background=True,
           margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})

    pg.emulate_media(media="screen")
    pg.screenshot(path=str(OUT / "poster-preview.png"), full_page=True)
    b.close()

for f in sorted(OUT.iterdir()):
    print(f"{f.name:44s} {f.stat().st_size/1e6:7.2f} MB")
print("errors:", errs if errs else "none")
