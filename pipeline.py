import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".gpkg")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")

import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer

from sites import SITES

REMOTE = ("/vsicurl/https://s3.us-west-2.amazonaws.com/dep-public-data/"
          "dep_ls_coastlines/dep_ls_coastlines_0-7-0-55.gpkg")
LOCAL = Path("data/dep_ls_coastlines.gpkg")
OUT = Path("out")
WORK_CRS = 3832
DIST_YEARS = list(range(1999, 2024))

_tf = Transformer.from_crs(4326, WORK_CRS, always_xy=True)


def bbox_work(bbox):
    lon0, lat0, lon1, lat1 = bbox
    xs, ys = _tf.transform([lon0, lon1, lon0, lon1], [lat0, lat0, lat1, lat1])
    return (min(xs), min(ys), max(xs), max(ys))


def summarise(key, spec, g):
    sig = g[g.sig_time < 0.05]
    net = g.rate_time * g.valid_span
    med_net = float(net.median())
    return {
        "site": key,
        "label": spec["label"],
        "country": spec["country"],
        "group": spec["group"],
        "n_good": int(len(g)),
        "n_sig": int(len(sig)),
        "pct_sig": round(100.0 * len(sig) / len(g), 1),
        "median_rate_m_yr": round(float(g.rate_time.median()), 3),
        "mean_rate_m_yr": round(float(g.rate_time.mean()), 3),
        "median_sig_rate_m_yr": round(float(sig.rate_time.median()), 3) if len(sig) else np.nan,
        "pct_eroding": round(100.0 * float((g.rate_time < 0).mean()), 1),
        "pct_sig_eroding": round(100.0 * float((sig.rate_time < 0).mean()), 1) if len(sig) else np.nan,
        "median_sce_m": round(float(g.sce.median()), 1),
        "p90_sce_m": round(float(g.sce.quantile(0.90)), 1),
        "median_net_m": round(med_net, 1),
        "churn_ratio": round(float(g.sce.median()) / max(abs(med_net), 0.1), 1),
        "rate_p10": round(float(g.rate_time.quantile(0.10)), 2),
        "rate_p90": round(float(g.rate_time.quantile(0.90)), 2),
        "median_valid_span_yr": int(g.valid_span.median()),
    }


def trajectory(key, spec, g):
    rows = []
    for yr in DIST_YEARS:
        col = f"dist_{yr}"
        if col not in g.columns:
            continue
        d = g[col].to_numpy(dtype=float)
        n = int(np.isfinite(d).sum())
        if n == 0:
            continue
        rows.append({
            "site": key,
            "label": spec["label"],
            "year": yr,
            "n_valid": n,
            "median_dist_m": round(float(np.nanmedian(d)), 2),
            "mean_dist_m": round(float(np.nanmean(d)), 2),
            "p25_dist_m": round(float(np.nanpercentile(d, 25)), 2),
            "p75_dist_m": round(float(np.nanpercentile(d, 75)), 2),
            "pct_landward": round(100.0 * float(np.nanmean(d < 0)), 1),
        })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["local", "remote"], default="local")
    ap.add_argument("--sites", default="all")
    ap.add_argument("--geo", action="store_true",
                    help="also export transect points and annual shorelines as GeoJSON")
    args = ap.parse_args()

    src = str(LOCAL) if args.source == "local" else REMOTE
    if args.source == "local" and not LOCAL.exists():
        raise SystemExit(f"missing {LOCAL} - run with --source remote or download first")

    wanted = list(SITES) if args.sites == "all" else [s.strip() for s in args.sites.split(",")]
    OUT.mkdir(exist_ok=True)
    (OUT / "geo").mkdir(exist_ok=True)

    summary, traj, coverage = [], [], []

    for key in wanted:
        spec = SITES[key]
        bb = bbox_work(spec["bbox"])
        g = gpd.read_file(src, layer="rates_of_change", bbox=bb, engine="pyogrio")
        n_all = len(g)
        g = g[g.certainty == "good"].reset_index(drop=True)
        if g.empty:
            print(f"  {spec['label']:26s} no good transects")
            continue

        summary.append(summarise(key, spec, g))
        traj.extend(trajectory(key, spec, g))
        r = summary[-1]
        print(f"  {spec['label']:26s} good={r['n_good']:5d}/{n_all:<5d} "
              f"rate={r['median_rate_m_yr']:+6.2f}  erod={r['pct_eroding']:5.1f}%  "
              f"sce={r['median_sce_m']:6.1f}  net={r['median_net_m']:+7.1f}  "
              f"churn={r['churn_ratio']:5.1f}x")

        if args.geo:
            pts = g[["uid", "rate_time", "sig_time", "se_time", "sce", "nsm",
                     "valid_obs", "valid_span", "geometry"]].copy()
            pts["significant"] = pts.sig_time < 0.05
            pts.to_crs(4326).to_file(OUT / "geo" / f"transects_{key}.geojson", driver="GeoJSON")

            sl = gpd.read_file(src, layer="shorelines_annual", bbox=bb, engine="pyogrio")
            sl_good = sl[sl.certainty == "good"].copy()
            coverage.append({
                "site": key,
                "label": spec["label"],
                "years_all": sorted(int(y) for y in sl.year.unique()),
                "years_good": sorted(int(y) for y in sl_good.year.unique()),
                "n_good_features": int(len(sl_good)),
            })
            if not sl_good.empty:
                sl_good["year"] = sl_good.year.astype(int)
                sl_good.to_crs(4326).to_file(
                    OUT / "geo" / f"shorelines_{key}.geojson", driver="GeoJSON")

    if not summary:
        raise SystemExit("no sites produced output")

    df = pd.DataFrame(summary).sort_values("median_rate_m_yr")
    df.to_csv(OUT / "island_summary.csv", index=False)
    pd.DataFrame(traj).to_csv(OUT / "island_trajectory.csv", index=False)

    meta = {
        "collection": "dep_ls_coastlines",
        "product": "Annual Shorelines (Landsat, 30 m), Digital Earth Pacific",
        "asset": "dep_ls_coastlines_0-7-0-55.gpkg",
        "source_url": REMOTE.replace("/vsicurl/", ""),
        "stac": "https://stac.digitalearthpacific.org/collections/dep_ls_coastlines",
        "licence": "CC-BY-4.0",
        "work_crs": WORK_CRS,
        "certainty_filter": "good",
        "significance": "sig_time < 0.05",
        "observed_years": [DIST_YEARS[0], DIST_YEARS[-1]],
        "notes": [
            "rate_time is metres/year; positive = seaward (land gain), negative = landward (erosion).",
            "sce = shoreline change envelope, the full range a transect swept over the record.",
            "median_net_m = median(rate_time * valid_span), the net displacement over the record.",
            "Totals from shorelines_annual are NOT comparable across years: mapped shoreline length",
            "grows with Landsat coverage, not with real coastal change. Use transects for all numbers.",
        ],
    }
    if coverage:
        meta["shoreline_coverage"] = coverage
    (OUT / "run_meta.json").write_text(json.dumps(meta, indent=2))

    print(f"\nwrote {OUT/'island_summary.csv'} ({len(df)} sites)")
    print(f"wrote {OUT/'island_trajectory.csv'} ({len(traj)} rows)")
    if args.geo:
        print(f"wrote GeoJSON to {OUT/'geo'}")


if __name__ == "__main__":
    main()
