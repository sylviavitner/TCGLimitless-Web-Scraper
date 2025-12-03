import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pokemon.csv")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Filter for high rarity cards
high_rarity_cards = df[df["rarity"].isin(["Art Rare", "Secret Rare", "Special Art Rare"])].copy()

# Get top n most expensive cards
top_n = 200
top_n_expensive = high_rarity_cards.nlargest(top_n, "price")

# Get unique artists from top n and sort in order of maximum price
artist_max_price = top_n_expensive.groupby("artist")["price"].max().sort_values()
unique_artists = artist_max_price.index.tolist()

# Create categorical artist variable for x axis
top_n_expensive["artist_cat"] = pd.Categorical(
    top_n_expensive["artist"],
    categories=unique_artists,
    ordered=True
)

# Assign x-positions based on artist category
top_n_expensive["x_position"] = top_n_expensive["artist_cat"].cat.codes

# Create the plot
plt.figure(figsize=(10, 6))

# Plot each rarity with its own color
for rarity in top_n_expensive["rarity"].unique():
    mask = top_n_expensive["rarity"] == rarity
    plt.scatter(
        top_n_expensive[mask]["x_position"],
        top_n_expensive[mask]["price"],
        label=rarity,
        alpha=0.7,
        s=50
    )

# Set labels and formatting
plt.xlabel("Artist (ordered by least to most expensive card)", fontsize=11)
plt.ylabel("Card Price ($)", fontsize=11)
plt.title(f"Top {top_n} Most Expensive Cards by Artist")

# Set x-ticks to show artist names (one per artist)
plt.xticks(
    range(len(unique_artists)),
    unique_artists,
    rotation=90,
    ha="right",
    fontsize=8
)

plt.legend(title="Rarity", loc="upper left")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()