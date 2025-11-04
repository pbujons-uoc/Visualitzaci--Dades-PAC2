import pandas as pd
import matplotlib.pyplot as plt
import joypy
import os

# Load dataset
df = pd.read_csv("./data/2015.csv")

# Use correct column names
region_col = "Region"
score_col = "Happiness Score"

# Drop missing values (important!)
df = df[[region_col, score_col]].dropna()


region_counts = df[region_col].value_counts()
valid_regions = region_counts[region_counts >= 5].index
df_filtered = df[df[region_col].isin(valid_regions)]

# Create /plots directory if it doesn’t exist
os.makedirs("./plots", exist_ok=True)


# Create ridgeline plot
plt.figure(figsize=(10, 6))
joypy.joyplot(
    df_filtered,
    by=region_col,
    column=score_col,
    colormap=plt.cm.viridis,
    fade=True,
    linewidth=1,
)

plt.title("Distribution of Happiness Score by Region (2015)", fontsize=14)
plt.xlabel("Happiness Score")
plt.tight_layout()

# Save as JPEG
plt.savefig("./plots/ridgeline_happiness_by_region.jpeg", dpi=300, bbox_inches="tight")

plt.show()
