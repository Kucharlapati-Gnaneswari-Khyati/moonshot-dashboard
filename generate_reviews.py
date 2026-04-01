import pandas as pd
import random

df = pd.read_csv("dataset.csv")

positive = [
    "Very durable and good quality",
    "Smooth wheels and easy to carry",
    "Lightweight and spacious",
    "Excellent value for money",
    "Strong build quality",
    "Stylish design and good finish",
    "Perfect for travel",
    "Good zipper and strong handle"
]

negative = [
    "Handle feels weak",
    "Zipper broke after few uses",
    "Not durable enough",
    "Scratches easily",
    "Poor wheel quality",
    "Overpriced for quality",
    "Material feels cheap",
    "Not spacious as expected"
]

neutral = [
    "Average product",
    "Okay for travel",
    "Decent quality",
    "Standard luggage",
    "Basic features",
    "Normal suitcase",
    "Nothing special",
    "Acceptable quality"
]

reviews = []

for _, row in df.iterrows():

    brand = row["Brand"]

    for _ in range(4):
        reviews.append({
            "Brand": brand,
            "Review": random.choice(positive)
        })

    for _ in range(3):
        reviews.append({
            "Brand": brand,
            "Review": random.choice(neutral)
        })

    for _ in range(3):
        reviews.append({
            "Brand": brand,
            "Review": random.choice(negative)
        })


reviews_df = pd.DataFrame(reviews)

reviews_df.to_csv("reviews.csv", index=False)

print("Reviews generated successfully")