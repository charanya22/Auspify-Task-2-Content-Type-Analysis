import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

folder = Path(__file__).parent
df = pd.read_csv(folder / "Dataset.csv")

# Count each content type
counts = df["type"].value_counts()
print("Netflix Content Type Analysis")
print("=" * 35)
print(counts)
print("\nPercentage distribution:")
print((counts / counts.sum() * 100).round(2).astype(str) + "%")

# Create output folder for charts
charts = folder / "charts"
charts.mkdir(exist_ok=True)

# Bar chart
plt.figure(figsize=(8, 5))
counts.plot(kind="bar")
plt.title("Netflix Content Type Distribution")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(charts / "content_type_distribution.png", dpi=300)
plt.close()

# Pie chart
plt.figure(figsize=(7, 7))
counts.plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Netflix Movies vs TV Shows")
plt.ylabel("")
plt.tight_layout()
plt.savefig(charts / "content_type_share.png", dpi=300)
plt.close()

print("\nCharts saved in:", charts)
