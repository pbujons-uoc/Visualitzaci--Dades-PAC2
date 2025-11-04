import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# ---------- Load & prep ----------
df = pd.read_csv(
    "./data/SuperStoreOrders.csv",
    usecols=["ship_mode", "segment", "country", "region"],  # ship_mode ignored later
    nrows=1000
).dropna(subset=["segment", "country", "region"])

# Optional tidy-up (strip whitespace)
for col in ["segment", "country", "region"]:
    df[col] = df[col].astype(str).str.strip()

# Count buys at the leaf level (region, country, segment)
leaf = (
    df.groupby(["region", "country", "segment"], as_index=False)
      .size()
      .rename(columns={"size": "count"})
)

# Helper to create unique IDs (so labels with same text in different parents don't merge)
SEP = "⟂"  # unlikely to appear in real data
def reg_id(region): return f"reg{SEP}{region}"
def cty_id(region, country): return f"cty{SEP}{region}{SEP}{country}"
def seg_id(region, country, segment): return f"seg{SEP}{region}{SEP}{country}{SEP}{segment}"

# Aggregate for region and country nodes
region_counts = leaf.groupby("region", as_index=False)["count"].sum()
ctry_counts   = leaf.groupby(["region", "country"], as_index=False)["count"].sum()

# Build node arrays
labels, ids, parents, values = [], [], [], []

# Root node
labels.append("Buys")
ids.append("root")
parents.append("")
values.append(int(leaf["count"].sum()))

# Region nodes
for _, row in region_counts.iterrows():
    r, cnt = row["region"], int(row["count"])
    labels.append(r)
    ids.append(reg_id(r))
    parents.append("root")
    values.append(cnt)

# Country nodes (children of their region)
for _, row in ctry_counts.iterrows():
    r, c, cnt = row["region"], row["country"], int(row["count"])
    labels.append(c)
    ids.append(cty_id(r, c))
    parents.append(reg_id(r))
    values.append(cnt)

# Segment leaf nodes (children of their country)
for _, row in leaf.iterrows():
    r, c, s, cnt = row["region"], row["country"], row["segment"], int(row["count"])
    labels.append(s)
    ids.append(seg_id(r, c, s))
    parents.append(cty_id(r, c))
    values.append(cnt)

# Sunburst figure
fig = go.Figure(
    go.Sunburst(
        labels=labels,
        ids=ids,
        parents=parents,
        values=values,
        branchvalues="total",
        insidetextorientation="auto",
        hovertemplate="<b>%{label}</b><br>Buys: %{value}<extra></extra>",
        maxdepth=None
    )
)

fig.update_layout(
    title="Buys → Region → Country → Segment",
    margin=dict(t=60, l=10, r=10, b=10),
    paper_bgcolor="white"  # keeps the center looking like a white circle
)

# Write to HTML
Path("./plots").mkdir(parents=True, exist_ok=True)
fig.write_html("./plots/sunburst_buys_region_country_segment.html", include_plotlyjs="cdn")
print("Wrote ./plots/sunburst_buys_region_country_segment.html")
