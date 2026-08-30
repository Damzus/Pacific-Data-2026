import hashlib
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/site/"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1200)
    pg.click("#picker .chip[data-site='tarawa']")
    pg.wait_for_timeout(900)

    def frame():
        svg = pg.inner_html("#stageBody svg")
        return {
            "year": pg.inner_text("#yrLabel"),
            "paths": pg.eval_on_selector_all("#stageBody svg path", "e => e.length"),
            "hi": pg.eval_on_selector_all(
                "#stageBody svg path[stroke='var(--hi)']", "e => e.length"),
            "hash": hashlib.md5(svg.encode()).hexdigest()[:10],
        }

    print("scrubbing the year slider:")
    seen = []
    for v in [0, 4, 8, 12, 16, 20]:
        pg.fill("#yrRange", str(v)); pg.dispatch_event("#yrRange", "input")
        pg.wait_for_timeout(450)
        f = frame(); seen.append(f)
        print(f"   idx {v:2d}  year {f['year']}  paths {f['paths']:5d}  "
              f"highlighted {f['hi']:4d}  svg {f['hash']}")

    uniq = len({f["hash"] for f in seen})
    growing = all(seen[i]["paths"] <= seen[i + 1]["paths"] for i in range(len(seen) - 1))
    print(f"\n   distinct frames: {uniq}/{len(seen)}   paths accumulate: {growing}")

    print("\npress Play and sample:")
    pg.fill("#yrRange", "0"); pg.dispatch_event("#yrRange", "input")
    pg.wait_for_timeout(300)
    pg.click("#playBtn")
    shots = []
    for _ in range(4):
        pg.wait_for_timeout(1000)
        shots.append(frame())
        print(f"   year {shots[-1]['year']}  paths {shots[-1]['paths']:5d}  "
              f"svg {shots[-1]['hash']}")
    pg.click("#playBtn")
    print(f"\n   distinct frames while playing: {len({s['hash'] for s in shots})}/{len(shots)}")
    b.close()

print("\nERRORS:", errs if errs else "none")
