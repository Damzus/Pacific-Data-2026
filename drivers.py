import json
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("data/stat/DF_CLIMATE_CHANGE.csv")
OUT = Path("out/drivers.json")

GEO = {
    "funafuti": "TV", "nanumea": "TV", "tarawa": "KI", "majuro": "MH",
    "kayangel": "PW", "choiseul": "SB", "carteret": "PG",
    "natewa": "FJ", "wallis": "WF",
}
NAMES = {
    "TV": "Tuvalu", "KI": "Kiribati", "MH": "Marshall Islands", "PW": "Palau",
    "SB": "Solomon Islands", "PG": "Papua New Guinea", "FJ": "Fiji",
    "WF": "Wallis and Futuna",
}


def series(d, ind, geo):
    s = d[(d.CLIMATE_CHANGE_INDICATORS == ind) & (d.GEO_PICT == geo)]
    s = s[["TIME_PERIOD", "OBS_VALUE"]].dropna()
    s = s.groupby("TIME_PERIOD", as_index=False).OBS_VALUE.mean()
    return s.sort_values("TIME_PERIOD")


def trend(s, y0, y1):
    w = s[(s.TIME_PERIOD >= y0) & (s.TIME_PERIOD <= y1)]
    if len(w) < 5:
        return None
    m = np.polyfit(w.TIME_PERIOD, w.OBS_VALUE, 1)[0]
    return float(m)


def main():
    d = pd.read_csv(SRC, low_memory=False)
    out = {}
    for geo in sorted(set(GEO.values())):
        sl = series(d, "SEA_LVL", geo)
        sst = series(d, "SST_ANOM", geo)
        sl_trend = trend(sl, 1993, 2023)
        rec = {
            "geo": geo,
            "name": NAMES[geo],
            "sea_level_mm_yr": round(sl_trend * 1000, 1) if sl_trend else None,
            "sea_level": [[int(a), round(float(b), 3)] for a, b in
                          zip(sl.TIME_PERIOD, sl.OBS_VALUE) if 1993 <= a <= 2023],
            "sst_recent_c": None,
            "sst_baseline_c": None,
            "sst": [[int(a), round(float(b), 2)] for a, b in
                    zip(sst.TIME_PERIOD, sst.OBS_VALUE) if a >= 1950],
        }
        base = sst[(sst.TIME_PERIOD >= 1951) & (sst.TIME_PERIOD <= 1980)]
        recent = sst[(sst.TIME_PERIOD >= 2014) & (sst.TIME_PERIOD <= 2023)]
        if len(base):
            rec["sst_baseline_c"] = round(float(base.OBS_VALUE.mean()), 2)
        if len(recent):
            rec["sst_recent_c"] = round(float(recent.OBS_VALUE.mean()), 2)
        out[geo] = rec

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"by_geo": out, "site_geo": GEO}, separators=(",", ":")))

    print(f"{'territory':22s} {'sea level':>12s} {'SST 51-80':>10s} {'SST 14-23':>10s} {'warming':>9s}")
    for g, r in sorted(out.items(), key=lambda kv: -(kv[1]["sea_level_mm_yr"] or 0)):
        warm = (r["sst_recent_c"] - r["sst_baseline_c"]) if (
            r["sst_recent_c"] is not None and r["sst_baseline_c"] is not None) else None
        print(f"{r['name']:22s} {str(r['sea_level_mm_yr'])+' mm/yr':>12s} "
              f"{str(r['sst_baseline_c']):>10s} {str(r['sst_recent_c']):>10s} "
              f"{('+'+format(warm,'.2f')+'C') if warm is not None else '-':>9s}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
