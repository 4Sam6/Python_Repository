import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Set up directory for saving charts
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define counties
counties = ["Bucharest", "Brașov", "Cluj", "Constanța", "Galați", "Sibiu", "Suceava"]

# Function to generate 7 random values with 30-60 twice as likely as other ranges
def generate_random_values():
    values = []
    for _ in range(7):
        if np.random.random() < 0.67:  # 67% chance to get a number between 30 and 60
            values.append(np.random.randint(30, 60))
        else:  # 33% chance to get a number outside 30-60 range (10-30 or 60-80)
            if np.random.random() < 0.5:
                values.append(np.random.randint(10, 30))
            else:
                values.append(np.random.randint(60, 80))
    return values

# Generate Romania dataset
rom = pd.DataFrame({
    "County": counties,
    "BCG": generate_random_values(),
    "HBV": generate_random_values(),
    "DTP": generate_random_values(),
    "VPI": generate_random_values(),
    "HiB": generate_random_values(),
    "VPC": generate_random_values(),
    "ROR": generate_random_values()
})
rom.insert(1, "Total", rom.iloc[:, 1:].sum(axis=1))

# Generate Ukraine dataset
ukr = pd.DataFrame({
    "County": counties,
    "BCG": generate_random_values(),
    "HBV": generate_random_values(),
    "DTP": generate_random_values(),
    "VPI": generate_random_values(),
    "HiB": generate_random_values(),
    "VPC": generate_random_values(),
    "ROR": generate_random_values()
})
ukr.insert(1, "Total", ukr.iloc[:, 1:].sum(axis=1))

# Combine both datasets with labels
rom["Dataset"] = "Romania"
ukr["Dataset"] = "Ukraine"
df_combined = pd.concat([rom, ukr])

# Create the PairGrid with different colors for each dataset
sns.set_theme(style="whitegrid")


g = sns.PairGrid(df_combined.sort_values("Total", ascending=False),
                 x_vars=df_combined.columns[1:-1], y_vars=["County"],
                 height=3, aspect=.5, hue="Dataset", palette=["blue", "orange"])

# Draw the dot plots with transparency for overlapping dots
g.map(sns.stripplot, size=10, orient="h", jitter=False, alpha=0.4,
      linewidth=1, edgecolor="w")

# Use meaningful titles
titles = ["Total", "BCG", "HBV", "DTP", "VPI", "HiB", "VPC", "ROR"]
for ax, title, col in zip(g.axes.flat, titles, df_combined.columns[1:-1]):
    
    col_min = df_combined[col].min() - 20  
    col_max = df_combined[col].max() + 20  
    ax.set_xlim(col_min, col_max)  
    ax.xaxis.grid(True, linestyle="--", alpha=0.9, linewidth=1.5)  # Make county gridlines bolder
    ax.yaxis.grid(True,  alpha=0.9, linewidth=1.5)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_color("black")  
    ax.spines['bottom'].set_color("black")
    ax.spines['left'].set_linewidth(1.5)  
    ax.spines['bottom'].set_linewidth(1.5)

# Add legend to indicate country representation
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, alpha=0.4, label='Romania'),
           plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=10, alpha=0.4, label='Ukraine')]



plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.05, 1), frameon=False)

sns.despine(left=False, bottom=False)
plt.subplots_adjust(top=0.9, left=0.2)


plt.savefig(os.path.join(OUTPUT_DIR, "vaccination_comparison_graph.png"), dpi=300, bbox_inches="tight", bbox_extra_artists=(plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(1.05, 1), frameon=False),))
