# This is the standard part of the script where you import all of the libraries 

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# This part of the script sets up a directory for the charts to be saved into 

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# The first part of this script is to generate a dataframe that can be used as example data

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

# Generate random values for each vaccine category
bcg_values = generate_random_values()
hbv_values = generate_random_values()
dtp_values = generate_random_values()
vpi_values = generate_random_values()
hib_values = generate_random_values()
vpc_values = generate_random_values()
ror_values = generate_random_values()

# Create the DataFrame
df = pd.DataFrame({
    "County": counties,
    "BCG": bcg_values,
    "HBV": hbv_values,
    "DTP": dtp_values,
    "VPI": vpi_values,
    "HiB": hib_values,
    "VPC": vpc_values,
    "ROR": ror_values
})

# Add the "Total" column as the sum of all vaccine values per row and ensure it's the second column
df.insert(1, "Total", df.iloc[:, 1:].sum(axis=1))


# The sceond  part of the script will create a dotplot based of the dataframe previously generated


sns.set_theme(style="whitegrid")

# Make the PairGrid
g = sns.PairGrid(df.sort_values("Total", ascending=False),
                 x_vars=df.columns[1:], y_vars=["County"],
                 height=3, aspect=.5)

# Draw a dot plot using the stripplot function
g.map(sns.stripplot, size=10, orient="h", jitter=False,
      palette="flare_r", linewidth=1, edgecolor="w")

# Use the same x axis limits on all columns and add better labels
g.set( xlabel="vaccinations", ylabel="")

# Use semantically meaningful titles for the columns
titles = ["Total", "BCG", "HBV",
          "DTP", "VPI", "HiB", "VPC", "ROR"]

for ax, title, col in zip(g.axes.flat, titles, df.columns[1:]):
    # Set a different title for each axis

    # Set a different title for each axes
    ax.set(title=title)

    # Compute min & max with margin
    col_min = df[col].min() - 20  # Subtract 20 for the lower limit
    col_max = df[col].max() + 20  # Add 20 for the upper limit
    ax.set_xlim(col_min, col_max)  # Set new limits

    # Make the grid horizontal instead of vertical
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)

    ax.spines['left'].set_color("black")  # Set spine color
    ax.spines['bottom'].set_color("black")


# Adjust the layout to increase top margin
plt.subplots_adjust(top=0.9, left=0.09)  # Adjusts the top and left  margin



#sns.despine(left=False, bottom=False)

#  creates a time stamp that can be added to file name
current_date = pd.Timestamp.now().strftime("%Y-%m-%d")
plt.savefig(f"{OUTPUT_DIR}/dotplot{current_date}.png")