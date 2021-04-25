"""
This Python script was used to modify the contents of the HYG database:
https://github.com/astronexus/HYG-Database
"""
import pandas as pd


data = pd.read_csv("hygdata_v3.csv")

data = data.drop(["hip", "hd", "hr", "gl", "ra", "dec", "bf", "pmra", "pmdec", "rv",
                  "vx", "vy", "vz", "rarad", "decrad", "pmrarad", "absmag", "pmdecrad",
                  "bayer", "flam", "var", "var_min", "var_max", "base", "x", "y", "z", "spect"], axis=1)

data = data[data["con"].notna()]
data = data[data["ci"].notna()]
data = data[(data["mag"] < 7) | (data["dist"] < 20)]
data = data.drop(["mag"], axis=1)
# Calculate surface temperature of star from its color index.
data["temp"] = 4600 * (1/(0.92 * data["ci"] + 1.7) + 1/(0.92 * data["ci"] + 0.62))
data = data.drop(["ci"], axis=1)

# Calculate distance in light years instead of parsecs.
data["dist"] = 3.262 * data["dist"]
data = data[data["dist"] < 10000]

# Approximate star radius (in sol radii) from its temperature and luminosity.
data["rad"] = ((5800 / (data["temp"])) ** 2) * (data["lum"]**0.5)

# Calculate star's lifetime based on its luminosity, in millions of years.
data["lifetime"] = 10000 * (data["lum"] ** (-2.5/3.5))
data["lifetime"] = data["lifetime"].astype(int)

data = data.sort_values(by=["con", "dist"])
data = data.set_index("id")
print(data.info())
# print(data[data["rad"] == data["rad"].min()])
# print(data[data["dist"] < data["dist"].min() * 1.1])

data.to_csv("star_catalogue.csv")
