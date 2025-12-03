import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pokemon.csv")

# Convert price to numeric
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Strip common prefixes and suffixes from name
def clean_name(name):
    name = str(name)
    prefixes = ["'s ", " Mask ", "Mega "]
    for prefix in prefixes:
        if name.startswith(prefix):
            name = name.split(prefix)[-1]
    suffixes = [" ex", " V", " VMAX", " VSTAR", " GX", " X"]
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    return name.strip()

# Apply clean name
df["clean_name"] = df["name"].apply(clean_name)

# Filter for high rarity cards
high_rarity_cards = df[df["rarity"].isin(["Art Rare", "Secret Rare", "Special Art Rare"])].copy()

# Get top N most expensive cards
top_n = 100
top_n_expensive = high_rarity_cards.nlargest(top_n, "price")

# Get unique Pokémon from top n and sort by max price
pokemon_max_price = top_n_expensive.groupby("clean_name")["price"].max().sort_values()
unique_pokemon = pokemon_max_price.index.tolist()

# Create categorical pokemon variable for x-axis positioning
top_n_expensive["pokemon_cat"] = pd.Categorical(
    top_n_expensive["clean_name"],
    categories=unique_pokemon,
    ordered=True
)

# Assign x-positions based on pokemon category
top_n_expensive["x_position"] = top_n_expensive["pokemon_cat"].cat.codes

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
plt.xlabel("Pokémon Name (ordered by most least to most expensive card)")
plt.ylabel("Card Price ($)")
plt.title(f"Top {top_n} Most Expensive High Rarity Cards by Pokémon")

# Set x-ticks to show pokemon names (one per pokemon)
plt.xticks(
    range(len(unique_pokemon)),
    unique_pokemon,
    rotation=90,
    ha="right",
    fontsize=8
)

plt.legend(title="Rarity", loc="upper left")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()