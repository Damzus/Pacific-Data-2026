# Submission pack — Pacific Dataviz Challenge 2026

**Team:** Saurab Nand · Mohammed Junaid Hanif · Karan Parmar
**Team contact (§10):** _to be designated — one person, receives the prize and distributes it_
**Pacific Islander self-identification (§12):** all three — must be stated in the registration form

**Entries:** two, both in the **main competition**, both as a **team**.
1. Static dataviz — A1 poster, `out/poster/island-stays-village-goes-A1.pdf`
2. Interactive dataviz — `site/` (needs a public URL before submitting)

**Deadline:** Monday 31 August 2026, 23:00 Fiji = 21:00 AEST. **Submit Sunday 30 August.**

---

## 1. Problem statement — static entry

*(paste into the registration form; §10 requires the problem and how the dataviz answers it)*

**The problem.** The Pacific is described to the world in a single sentence: the islands
are sinking. That sentence drives global attention, adaptation finance and the political
category of "climate refugee" — and it is not what the measurements show. It is wrong in
both directions at once. In Choiseul Province, Solomon Islands, five vegetated reef islands
have already vanished entirely, which the regional averages conceal. In the Carteret Islands,
Papua New Guinea, whose people are being relocated to Bougainville as the world's most-cited
climate refugees, the shoreline is *gaining* land. Funafuti and Tarawa are named in the same
breath as each other, and they are moving in opposite directions. When one story is applied
to thousands of islands, adaptation is planned for a coast that does not exist, and the
islands that are genuinely disappearing are averaged out of view.

**How the dataviz responds.** It measures the islands one at a time. Using twenty-five years
of Landsat-derived shoreline transects from Digital Earth Pacific, it maps nine islands
across Melanesia, Micronesia and Polynesia at their true coordinates, colouring every
measurement point by whether it gained or lost land — so the reader sees nine different
answers rather than one. It then sets the driver against the response: sea level is rising
at all nine sites and the ocean is warmer at all of them, yet the shoreline outcome is not
predicted by the rate of sea-level rise (r = +0.13, p = 0.74). The forcing is regional; the
outcome is local. Finally it places the satellite record beside the documented human record
— Choiseul's lost islands, the Carteret relocation, Vunidogoloa's move inland in 2014 — to
show that land area and habitability are not the same measurement. People are leaving
islands that are growing, because the wells turned salty. The conclusion the poster asks for
is operational: adaptation planned on a regional average will protect the wrong coast.

---

## 2. Problem statement — interactive entry

**The problem.** As above: a single regional narrative is standing in for thousands of
distinct, measurable local outcomes. But the deeper problem is that the evidence which would
correct it is locked in a two-gigabyte geospatial file that almost nobody can open. The
Digital Earth Pacific shoreline record contains two million quality-controlled measurement
points across fourteen Pacific countries and territories. A community leader, a provincial
planner or a journalist cannot use it. So the single story survives because the evidence
against it is inaccessible.

**How the dataviz responds.** It turns that file into something anyone can interrogate in a
browser. Nine islands can be selected and compared; every transect is drawn at its true
position, so the measurements themselves trace the coastline with no basemap; the reader can
filter to statistically significant points only, scrub the shoreline year by year from 1999
to 2023, and hover any point for its rate, its swept range and its significance. Each island
carries its own documented human record with sources. Every figure in the piece is exposed
in a table, and the method and its limits are stated on the page — including that mapped
shoreline length grows with satellite coverage rather than with real coastal change, which
is the trap this dataset sets for anyone who uses it casually. It is built as static files
with no external dependencies, so it will still run unchanged in 2029.

---

## 3. Rule-by-rule compliance register

### Done

| Rule | Requirement | Status |
|---|---|---|
| §5, §6 | Main competition, team entry | Two team entries planned |
| §6 | Pacific Islander self-identification unlocks Pacific prizes | All team members self-identify — **state this in the form** |
| §8 | Entries and explanations in English or French | English throughout |
| §9 | Use ≥1 dataset from the official list | **Two**: Coastline (`dep_ls_coastlines`) and `DF_CLIMATE_CHANGE` (SEA_LVL, SST_ANOM) — both verified on the official list |
| §9 | Cite all datasets used | Cited on poster footer and site footer, with STAC/PDH references |
| §9 | Comply with dataset licence terms | CC-BY-4.0 attributed; see open item below |
| §9 | Original work, not previously published | Built from scratch for this Challenge |
| §10 | Problem statement | Sections 1 and 2 above |
| §10 | Static: vector PDF, ≤100 MB | A1 594.1×841.4 mm, 1 page, fully vector (0 raster images), 2.38 MB |
| §13 | Contestants hold unrestricted rights | Own analysis and code; data is openly licensed |

### Open — needs your action

| # | Item | Why it matters |
|---|---|---|
| 1 | **Register both entries** at pacificdatavizchallenge.org | Nothing is submitted yet |
| 2 | **Designate one team contact** (§10) | Teams must submit a single entry under one contact; the prize is paid to that person, who then distributes it internally |
| 3 | **Host the interactive and supply the URL** (§10) | Must stay public until **31 Aug 2029**. GitHub Pages under an org account, not a personal one someone may lose access to |
| 4 | **Confirm eligibility** (§6) | No team member may be an SPC employee, jury member, or otherwise involved in organising |
| 5 | **Parental consent if anyone is under 18** (§6) | Form is on the Challenge website |
| 6 | **Consider individual Youth entries** (§7, §12) | Anyone ≤25 can *also* enter individually; Static and Interactive Youth 1st are USD 1000 each in a far shallower field |
| 7 | **AI declaration** (§9) | AI may assist but must not replace the core creative and analytical process. Be ready to explain the thesis, the site selection, and the methodological calls in your own words — that is what a jury will probe |
| 8 | **Ask the organisers about the licence** | The PDH catalogue page lists the coastlines dataset as CC-BY-**NC**-4.0; the upstream STAC collection says CC-BY-4.0. §13 requires granting SPC a licence that includes commercial use. Almost certainly a stale catalogue record — SPC publishes the data and put it on their own official list — but one email to datavizchallenge@spc.int removes a disqualification risk |

---

## 4. Timeline to submission

| Day | Work |
|---|---|
| Mon 25 Aug | Set up repo + GitHub Pages; test the public URL cold on a phone |
| Tue 26 Aug | Simplify the three heavy shoreline files (Natewa 2.8 MB, Choiseul 1.8 MB, Kayangel 1.5 MB) |
| Wed 27 Aug | Team review of poster copy — replace my wording with your own voice |
| Thu 28 Aug | Add a home island if any team member is from a covered territory |
| Fri 29 Aug | Final proof, accessibility check, re-render poster PDF |
| Sat 30 Aug | Register both entries, paste problem statements, upload PDF, submit |
| Sun 31 Aug | Reserve only — do not plan to submit on deadline day |

---

## 5. Known limits, stated on both entries

- 30 m Landsat pixels are coarse for small motu; short transect records carry real uncertainty.
- The Carteret group yields 251 usable transects of which only 36 are statistically
  significant — it is presented as indicative, not headline-grade.
- With nine sites, the sea-level correlation can rule out a strong relationship, not a weak one.
- The five islands lost in Choiseul predate the satellite record and come from Albert et al. (2016).
- Shoreline traces begin in a different year at each site (Funafuti 2007, Tarawa 1999,
  Majuro 2002) because early years fail the quality filter; transect rates always use the
  full 1999–2023 record. This is stated in the interface.

---

## 6. Reproducing the analysis

```
python pipeline.py --source local --geo   # transects + shorelines -> out/geo, out/*.csv
python drivers.py                         # sea level + SST trends -> out/drivers.json
python webprep.py                         # compact 84 MB -> 7.9 MB in site/data
python -m http.server 8765                # then open /site/
python make_poster.py                     # renders the A1 vector PDF
```
