import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset
data_set = pd.read_csv("./data/tips.csv")
data_set_chosen_columns = data_set.loc[:, ["total_bill", "tip", "sex"]]

plt.figure(figsize=(12, 8))

# Scatter points colored by sex
sns.scatterplot(
    data=data_set_chosen_columns,
    x="total_bill",
    y="tip",
    hue="sex",
    palette="Set1",
    s=80,
    edgecolor="w",
    alpha=0.8,
)

# Add regression lines for each sex category
sns.regplot(
    data=data_set_chosen_columns[data_set_chosen_columns["sex"] == "Male"],
    x="total_bill",
    y="tip",
    scatter=False,
    color="tab:blue",
    label="Trend (Male)"
)
sns.regplot(
    data=data_set_chosen_columns[data_set_chosen_columns["sex"] == "Female"],
    x="total_bill",
    y="tip",
    scatter=False,
    color="tab:red",
    label="Trend (Female)"
)

# Customize plot
plt.xlim(2, 52)
plt.ylim(0, 12)
plt.title("Tip Amount vs Total Bill by Sex with Trend Lines")
plt.xlabel("Total Bill ($)")
plt.ylabel("Tip ($)")
plt.legend()

# Save and show
plt.savefig("./plots/scatter_plot_tip_over_bill.jpeg", dpi=300, bbox_inches="tight")
plt.show()