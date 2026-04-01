import pandas as pd

products = pd.read_csv("dataset.csv")
reviews = pd.read_csv("reviews_with_sentiment.csv")

merged = pd.merge(
    reviews,
    products,
    left_on="Brand",
    right_on="Brand",
    how="left"
)

merged.to_csv("final_dataset.csv", index=False)

print("Final dataset created")