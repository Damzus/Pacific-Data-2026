from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/site/"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1000})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1200)

    def state():
        return {
            "chip": pg.eval_on_selector_all(
                "#picker .chip[aria-pressed='true']", "els => els.map(e => e.textContent)"),
            "year": pg.inner_text("#yrLabel"),
            "max": pg.get_attribute("#yrRange", "max"),
            "dots": pg.eval_on_selector_all("#stageBody svg circle", "els => els.length"),
            "paths": pg.eval_on_selector_all("#stageBody svg path", "els => els.length"),
            "story": pg.inner_text("#story h3")[:52],
        }

    print("initial      ", state())

    pg.click("#picker .chip[data-site='tarawa']")
    pg.wait_for_timeout(900)
    print("click Tarawa ", state())

    pg.check("#sigOnly"); pg.wait_for_timeout(700)
    print("sig only     ", state())
    pg.uncheck("#sigOnly"); pg.wait_for_timeout(700)

    pg.uncheck("#showLines"); pg.wait_for_timeout(700)
    print("no lines     ", state())
    pg.check("#showLines"); pg.wait_for_timeout(700)

    pg.fill("#yrRange", "5"); pg.dispatch_event("#yrRange", "input")
    pg.wait_for_timeout(700)
    print("year idx 5   ", state())

    pg.click("#playBtn"); pg.wait_for_timeout(1500)
    playing = pg.inner_text("#playBtn")
    pg.click("#playBtn"); pg.wait_for_timeout(300)
    print("play toggles ", playing, "->", pg.inner_text("#playBtn"))

    pg.eval_on_selector("#rateChart .row[data-site='choiseul'] rect[fill='transparent']",
                        "e => e.dispatchEvent(new MouseEvent('click', {bubbles:true}))")
    pg.wait_for_timeout(900)
    print("bar click    ", state())

    pg.eval_on_selector("#table tr[data-site='majuro']",
                        "e => e.dispatchEvent(new MouseEvent('click', {bubbles:true}))")
    pg.wait_for_timeout(900)
    print("row click    ", state())

    yrs = pg.evaluate(
        "fetch('data/s_funafuti.json').then(r=>r.json()).then(o=>Object.keys(o).sort())")
    print("funafuti shoreline years:", yrs)

    b.close()

print("\nERRORS:", errs if errs else "none")
