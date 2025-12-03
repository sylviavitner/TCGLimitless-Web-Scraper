import pandas as pd
import matplotlib.pyplot as plt

# Visual 1: Box plot of Price vs. Card Rarity

df = pd.read_csv("pokemon.csv")
df["price"] = pd.to_numeric(df["price"], errors="coerce") # convert price

# Order of rarities from least to greatest
rarity_order = [
    "Common", "Uncommon", "Rare", "Double Rare", "Ultra Rare", "Art Rare" , "Secret Rare", "Special Art Rare"
]

# Create a boxplot separated by rarity categories
df["rarity"] = pd.Categorical(df["rarity"], categories=rarity_order, ordered=True)
df.boxplot(column="price", by="rarity", grid=False, figsize=(10,6))
plt.suptitle("")
plt.title("Price Distribution by Card Rarity")
plt.xlabel("Rarity")
plt.ylabel("Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()