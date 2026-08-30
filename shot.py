import sys
from playwright.sync_api import sync_playwright

url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/site/"
out = sys.argv[2] if len(sys.argv) > 2 else "shot.png"
theme = sys.argv[3] if len(sys.argv) > 3 else "light"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 1000},
                    color_scheme=theme, device_scale_factor=2)
    errors = []
    pg.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    pg.goto(url, wait_until="networkidle", timeout=60000)
    pg.wait_for_timeout(1800)
    pg.screenshot(path=out, full_page=True)
    b.close()

print("saved", out)
if errors:
    print("CONSOLE ERRORS:")
    for e in errors[:20]:
        print("  ", e)
else:
    print("no console errors")
