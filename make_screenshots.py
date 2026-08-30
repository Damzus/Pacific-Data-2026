from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

OUT = Path("out/submission")
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://127.0.0.1:8765/site/"

with sync_playwright() as p:
    b = p.chromium.launch()

    pg = b.new_page(viewport={"width": 1400, "height": 1982}, device_scale_factor=1.6)
    pg.goto(BASE + "poster.html", wait_until="networkidle", timeout=90000)
    pg.wait_for_selector("body[data-ready='1']", timeout=90000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=str(OUT / "static-screenshot.png"), full_page=True)
    pg.close()

    pg = b.new_page(viewport={"width": 1500, "height": 1000}, device_scale_factor=2)
    pg.goto(BASE, wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(2000)
    pg.eval_on_selector("#picker .chip[data-site='tarawa']", "e => e.click()")
    pg.wait_for_timeout(1500)
    pg.fill("#yrRange", "23"); pg.dispatch_event("#yrRange", "input")
    pg.wait_for_timeout(1200)
    pg.screenshot(path=str(OUT / "_full.png"), full_page=True)
    end = pg.eval_on_selector(".explorer",
        "e => e.getBoundingClientRect().bottom + window.scrollY")
    (OUT / "_end.txt").write_text(str(end))
    pg.close()
    b.close()

full = Image.open(OUT / "_full.png")
scale = full.width / 1500
end = float((OUT / "_end.txt").read_text())
hero = full.crop((0, 0, full.width, min(full.height, int((end + 18) * scale))))
hero.save(OUT / "interactive-screenshot.png")
(OUT / "_full.png").unlink(); (OUT / "_end.txt").unlink()

for f in sorted(OUT.glob("*.png")):
    im = Image.open(f)
    ok = "OK" if im.width >= 800 and im.height >= 440 else "TOO SMALL"
    print(f"{f.name:32s} {im.width:5d} x {im.height:<5d} "
          f"{f.stat().st_size/1e6:5.2f} MB   min 800x440: {ok}")
