import os
import sys

os.environ["CPL_VSIL_CURL_ALLOWED_EXTENSIONS"] = ".gpkg"
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "EMPTY_DIR"

import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer

from sites import SITES

REMOTE = ("/vsicurl/https://s3.us-west-2.amazonaws.com/dep-public-data/"
          "dep_ls_coastlines/dep_ls_coastlines_0-7-0-55.gpkg")
LOCAL = "data/dep_ls_coastlines.gpkg"

src = LOCAL if (len(sys.argv) > 1 and sys.argv[1] == "local") else REMOTE
tf = Transformer.from_crs(4326, 3832, always_xy=True)

rows = []
for key, spec in SITES.items():
    lon0, lat0, lon1, lat1 = spec["bbox"]
    xs, ys = tf.transform([lon0, lon1, lon0, lon1], [lat0, lat0, lat1, lat1])
    bb = (min(xs), min(ys), max(xs), max(ys))
    try:
        g = gpd.read_file(src, layer="rates_of_change", bbox=bb, engine="pyogrio")
    except Exception as e:
        print(f"{spec['label']:26s} ERROR {e}")
        continue

    n_all = len(g)
    g = g[g.certainty == "good"]
    if g.empty:
        print(f"{spec['label']:26s} n={n_all:6d} -> 0 good")
        continue

    sig = g[g.sig_time < 0.05]
    net = (g.rate_time * g.valid_span)
    rows.append({
        "site": key,
        "label": spec["label"],
        "country": spec["country"],
        "group": spec["group"],
        "n_all": n_all,
        "n_good": len(g),
        "n_sig": len(sig),
        "median_rate_m_yr": round(g.rate_time.median(), 3),
        "median_sig_rate_m_yr": round(sig.rate_time.median(), 3) if len(sig) else np.nan,
        "pct_eroding": round(100 * (g.rate_time < 0).mean(), 1),
        "pct_sig_eroding": round(100 * (sig.rate_time < 0).mean(), 1) if len(sig) else np.nan,
        "median_sce_m": round(g.sce.median(), 1),
        "median_net_m": round(net.median(), 1),
        "churn_ratio": round(g.sce.median() / max(abs(net.median()), 0.1), 1),
        "worst_rate_m_yr": round(g.rate_time.min(), 2),
        "best_rate_m_yr": round(g.rate_time.max(), 2),
    })
    r = rows[-1]
    print(f"{spec['label']:26s} good={r['n_good']:5d} sig={r['n_sig']:5d} "
          f"medrate={r['median_rate_m_yr']:+6.2f} m/yr  erod={r['pct_eroding']:5.1f}%  "
          f"sce={r['median_sce_m']:6.1f}m  net={r['median_net_m']:+7.1f}m")

df = pd.DataFrame(rows)
os.makedirs("out", exist_ok=True)
df.to_csv("out/site_scan.csv", index=False)
print("\nwrote out/site_scan.csv")
