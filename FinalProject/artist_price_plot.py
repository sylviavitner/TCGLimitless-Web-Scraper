import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pokemon.csv")

# Visual 2: Scatter plot of top-producing illustrators and SAR card price
df["price"] = pd.to_numeric(df["price"], errors="coerce") # get price as a numeric value

# Only include SAR cards
special_art_rare = df[df["rarity"] == "Special Art Rare"].copy()

# Groupby artist and get the ones who produced the most amount of cards (top n)
artist_counts = special_art_rare.groupby("artist").size().reset_index(name="card_count")
artist_counts_sorted = artist_counts.sort_values(by="card_count", ascending=False)
top_n = 50
artist_order = artist_counts_sorted.iloc[:top_n]["artist"].tolist() #
artist_order.reverse() # highest SAR card count on the right
special_art_rare = special_art_rare[special_art_rare["artist"].isin(artist_order)]

# Create x-axis positions based on artist order
special_art_rare["artist_cat"] = pd.Categorical(special_art_rare["artist"],
                                                  categories=artist_order,
                                                  ordered=True)
special_art_rare = special_art_rare.sort_values("artist_cat")

# plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(
    special_art_rare["artist_cat"].cat.codes,
    special_art_rare["price"],
    alpha=0.6,
    s=50
)

# Set labels and title and display figure
plt.xticks(range(len(artist_order)), artist_order, rotation=90, ha="right")
plt.xlabel("Artist (ordered by number of Special Art Rare cards illustrated, least -> most)")
plt.ylabel("Card Price ($)")
plt.title("Special Art Rare Card Prices by Artist")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()