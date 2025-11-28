import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pokemon.csv")

# Visual 1: Box plot of Price vs. Card Rarity
df["price"] = pd.to_numeric(df["price"], errors="coerce")

rarity_order = [
    "Common", "Uncommon", "Rare", "Double Rare","Ultra Rare","Art Rare","Special Art Rare"
]

df["rarity"] = pd.Categorical(df["rarity"], categories=rarity_order, ordered=True)

plt.figure(figsize=(10,6))
df.boxplot(column="price", by="rarity", grid=False)

plt.title("Price Distribution by Card Rarity")
plt.suptitle("")
plt.xlabel("Rarity")
plt.ylabel("Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()