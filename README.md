# The island stays. The village goes.

Pacific Dataviz Challenge 2026 · Climate change · Saurab Nand (Fiji)

- `site/index.html`: interactive dataviz
- `site/poster.html` and `out/poster/island-stays-village-goes-A1.pdf`: static poster (A1)
- `SUBMISSION.md`: problem statements, compliance and how to reproduce the analysis

---

## Recording the video

Helper pages for recording (not part of the published site):

| File | What it is |
|---|---|
| `record.html` | The poster (or site) with your webcam in a round circle on top |
| `prompter.html` | Big-text script to read from: phone or a separate window |
| `VIDEO_SCRIPT.md` | The script, plus the recording and iMovie guide |

### 1. Start the local server

Run from the project folder and leave this terminal open:

```sh
cd ~/Downloads/Pacific-Data-2026
python3 -m http.server 8765
```

### 2. Open the pages

In a second terminal:

```sh
# Poster + round face circle (this is what you record)
open "http://localhost:8765/record.html?src=site/poster.html"

# Script in a separate window: drag the tab out and place it under the camera
open "http://localhost:8765/prompter.html"
```

Other versions of the recording page:

```sh
# The submitted PDF instead of the poster web page
open "http://localhost:8765/record.html?src=out/poster/island-stays-village-goes-A1.pdf"

# Interactive site instead of the poster
open "http://localhost:8765/record.html"

# Poster with the script strip built in at the top (record only the area below the red line)
open "http://localhost:8765/record.html?src=site/poster.html&prompt=1"
```

### 3. Script on your phone (optional)

Find your Mac's Wi-Fi address:

```sh
ipconfig getifaddr en0
```

On the phone (same Wi-Fi), open `http://<that-address>:8765/prompter.html`.
If macOS asks whether Python may accept incoming connections, click **Allow**.

### 4. Keys on the recording page

| Key | Action |
|---|---|
| `+` / `−` | Face circle bigger / smaller |
| `]` / `[` | Zoom poster in / out |
| `F` | Fit poster to screen width |
| `N` / `B` | Next / back in the script (only with `&prompt=1`) |
| `H` | Show / hide the tip |
| Drag the circle | Move it |

Click the page once before using the keys.

### 5. Record

1. Press **Cmd + Shift + 5**.
2. Go to **Options** and choose your microphone.
3. Choose one:
   - Script on your phone: **Record Entire Screen** (you can use full screen, Cmd + Ctrl + F).
   - Script in a separate window: **Record Selected Portion**, and drag the box over the poster window only.
4. Click **stop** in the menu bar when done. The file is saved to the Desktop.
5. Edit and export in iMovie (see `VIDEO_SCRIPT.md`).

### 6. Stop the server

Press **Ctrl + C** in the server terminal, or:

```sh
kill $(lsof -t -i :8765)
```

### Troubleshooting

| Problem | Fix |
|---|---|
| Face circle is black | Allow camera access for the page in the browser, close QuickTime/Photo Booth/Zoom, and reload. Check **System Settings → Privacy & Security → Camera**. |
| "Address already in use" | The server is already running. Skip step 1, or stop it first (step 6). |
| Phone can't open the script | Check the phone and Mac are on the same Wi-Fi, and click **Allow** if macOS asks about incoming connections. Or AirDrop `prompter.html` to the phone. |
| Poster won't scroll | Open it through `record.html`, not `site/poster.html` directly. |

---

## Reproducing the analysis

```sh
python pipeline.py --source local --geo   # transects + shorelines -> out/geo, out/*.csv
python drivers.py                         # sea level + SST trends -> out/drivers.json
python webprep.py                         # compact data into site/data
python make_poster.py                     # renders the A1 vector PDF
```

Data: Digital Earth Pacific Annual Shorelines (`dep_ls_coastlines`, CC-BY-4.0) and
Pacific Data Hub `DF_CLIMATE_CHANGE` (SEA_LVL, SST_ANOM).
