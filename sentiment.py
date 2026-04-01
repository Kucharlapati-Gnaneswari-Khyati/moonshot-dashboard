import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.tokenize import sent_tokenize
import numpy as np

# Download required NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')

print("Loading reviews...")
try:
    df = pd.read_csv("reviews.csv")
except FileNotFoundError:
    print("Error: 'reviews.csv' not found. Please ensure your review scraper has run.")
    exit()

sia = SentimentIntensityAnalyzer()

# Dictionary of keywords to isolate specific hardware sentiment
aspect_keywords = {
    'Wheels_Score': ['wheel', 'roller', 'spinner', 'caster', 'tyre'],
    'Zippers_Score': ['zip', 'chain', 'slider', 'zipper'],
    'Handle_Score': ['handle', 'trolley', 'pull', 'telescopic', 'button'],
    'Material_Score': ['shell', 'material', 'plastic', 'polycarbonate', 'scratch', 'body', 'sturdy', 'crack'],
    'Capacity_Score': ['space', 'size', 'capacity', 'room', 'spacious', 'packing', 'small', 'large']
}

sentiments = []
scores = []
aspect_results = {aspect: [] for aspect in aspect_keywords.keys()}

print("Analyzing sentiment and extracting aspect-level hardware scores...")

for review in df["Review"]:
    review_str = str(review)
    
    # 1. Overall VADER Sentiment
    overall_score = sia.polarity_scores(review_str)["compound"]
    if overall_score > 0.05:
        sentiment = "Positive"
    elif overall_score < -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    sentiments.append(sentiment)
    scores.append(overall_score)
    
    # 2. Aspect-Level Sentiment Extraction
    sentences = sent_tokenize(review_str.lower())
    for aspect, keywords in aspect_keywords.items():
        aspect_compounds = []
        for sentence in sentences:
            if any(keyword in sentence for keyword in keywords):
                sent_score = sia.polarity_scores(sentence)["compound"]
                aspect_compounds.append(sent_score)
        
        # Average the sentences and convert [-1, 1] VADER to [1, 10] scale for the radar chart
        if aspect_compounds:
            avg_compound = sum(aspect_compounds) / len(aspect_compounds)
            scaled_score = round(((avg_compound + 1) * 4.5) + 1, 1)
            aspect_results[aspect].append(scaled_score)
        else:
            aspect_results[aspect].append(np.nan)

df["Sentiment"] = sentiments
df["Sentiment Score"] = scores

for aspect, results in aspect_results.items():
    df[aspect] = results

df.to_csv("reviews_with_sentiment.csv", index=False)
print("✅ Sentiment analysis completed! Real hardware aspect scores added to 'reviews_with_sentiment.csv'")