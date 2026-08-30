import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

SRC = Path("out/geo")
DST = Path("site/data")
SUMMARY = Path("out/island_summary.csv")
TRAJ = Path("out/island_trajectory.csv")

SIMPLIFY_M = 12
COORD_DP = 5


def ring(coords):
    return [[round(x, COORD_DP), round(y, COORD_DP)] for x, y in coords]


def lines_of(geom):
    if geom is None or geom.is_empty:
        return []
    if geom.geom_type == "LineString":
        return [ring(geom.coords)]
    if geom.geom_type == "MultiLineString":
        return [ring(g.coords) for g in geom.geoms]
    return []


def prep_transects(site):
    f = SRC / f"transects_{site}.geojson"
    if not f.exists():
        return None
    g = gpd.read_file(f)
    g = g[g.rate_time.notna()]
    return {
        "lon": [round(v, COORD_DP) for v in g.geometry.x],
        "lat": [round(v, COORD_DP) for v in g.geometry.y],
        "rate": [round(float(v), 2) for v in g.rate_time],
        "sce": [round(float(v), 1) for v in g.sce.fillna(0)],
        "sig": [int(bool(v)) for v in (g.sig_time < 0.05)],
    }


def prep_shorelines(site):
    f = SRC / f"shorelines_{site}.geojson"
    if not f.exists():
        return None
    g = gpd.read_file(f)
    if g.empty:
        return None
    g = g.to_crs(3832)
    g["geometry"] = g.geometry.simplify(SIMPLIFY_M, preserve_topology=False)
    g = g.to_crs(4326)
    out = {}
    for yr, sub in g.groupby(g.year.astype(int)):
        segs = []
        for geom in sub.geometry:
            segs.extend(lines_of(geom))
        segs = [s for s in segs if len(s) > 1]
        if segs:
            out[str(yr)] = segs
    return out or None


def main():
    DST.mkdir(parents=True, exist_ok=True)
    summary = pd.read_csv(SUMMARY)
    traj = pd.read_csv(TRAJ) if TRAJ.exists() else pd.DataFrame()
    reloc = json.loads(Path("relocations.json").read_text(encoding="utf-8"))
    dpath = Path("out/drivers.json")
    drivers = json.loads(dpath.read_text()) if dpath.exists() else {"by_geo": {}, "site_geo": {}}

    manifest = []
    for _, r in summary.iterrows():
        site = r["site"]
        t = prep_transects(site)
        s = prep_shorelines(site)
        rec = {k: (None if pd.isna(v) else v) for k, v in r.items()}
        rec["has_transects"] = t is not None
        rec["has_shorelines"] = s is not None
        rec["years"] = sorted(int(y) for y in s.keys()) if s else []
        rec["relocation"] = reloc.get(site)
        geo = drivers["site_geo"].get(site)
        dv = drivers["by_geo"].get(geo) if geo else None
        if dv:
            rec["geo"] = geo
            rec["territory"] = dv["name"]
            rec["sea_level_mm_yr"] = dv["sea_level_mm_yr"]
            rec["sst_warming_c"] = (
                round(dv["sst_recent_c"] - dv["sst_baseline_c"], 2)
                if dv["sst_recent_c"] is not None and dv["sst_baseline_c"] is not None else None)
            rec["sea_level_series"] = dv["sea_level"]
        if not traj.empty:
            sub = traj[traj.site == site].sort_values("year")
            rec["traj"] = [
                {"y": int(a), "d": round(float(b), 2), "n": int(c)}
                for a, b, c in zip(sub.year, sub.median_dist_m, sub.n_valid)
            ]
        manifest.append(rec)

        if t:
            (DST / f"t_{site}.json").write_text(json.dumps(t, separators=(",", ":")))
        if s:
            (DST / f"s_{site}.json").write_text(json.dumps(s, separators=(",", ":")))

    (DST / "sites.json").write_text(json.dumps(manifest, separators=(",", ":")))

    total = sum(f.stat().st_size for f in DST.glob("*.json"))
    print(f"wrote {len(list(DST.glob('*.json')))} files to {DST}  total {total/1e6:.1f} MB")
    for f in sorted(DST.glob("*.json"), key=lambda p: -p.stat().st_size)[:12]:
        print(f"   {f.name:26s} {f.stat().st_size/1024:8.0f} KB")


if __name__ == "__main__":
    main()
