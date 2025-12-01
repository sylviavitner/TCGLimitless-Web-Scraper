import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("pokemon.csv")

# Only include SAR cards
special_art_rares = df[df["rarity"] == "Special Art Rare"].copy()
special_art_rares["price"] = pd.to_numeric(special_art_rares["price"], errors="coerce")

# Strip common prefixes and suffixes from the name
def clean_name(name):
    name = str(name)
    if "s" in name:
        name = name.split("'s ")[-1]
    if " Mask " in name:
        name = name.split(" Mask ")[-1]
    suffixes = [" ex", " V", " VMAX", " VSTAR", " GX", " X"]
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]  # strip suffix off name
    return name.strip()

# Apply the clean name function and count the occurences of each SAR card
special_art_rares["clean_name"] = special_art_rares["name"].apply(clean_name)
name_counts = special_art_rares["clean_name"].value_counts()
n = 60
top_n_names = name_counts.head(n).index.tolist()
top_n_names.reverse()
top_n_data = special_art_rares[special_art_rares["clean_name"].isin(top_n_names)] # include only top n

# Convert name to categorical type
top_n_data["clean_name"] = pd.Categorical(top_n_data["clean_name"],
                                    categories=top_n_names,
                                    ordered=True)

# create x values for each one
top_n_data["x_position"] = top_n_data["clean_name"].cat.codes

# Plot
plt.figure(figsize = (10, 6))
plt.scatter(top_n_data["x_position"], top_n_data["price"], alpha=0.6, s=25)
plt.title("Price of Special and Art Rare Cards by Name (Top 60)")
plt.xlabel("Card Name")
plt.ylabel("Price ($)")
plt.xticks(range(len(top_n_names)), top_n_names, rotation=90)
plt.tight_layout()
plt.grid(True, alpha=0.3)
plt.show()


