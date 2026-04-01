# 🧠 Moonshot Luggage Competitive Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)
![NLP](https://img.shields.io/badge/NLP-Aspect%20Sentiment-green.svg)
![AI Agent](https://img.shields.io/badge/AI-Agent%20Powered-purple.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-orange.svg)
![Playwright](https://img.shields.io/badge/Scraping-Playwright-blue)
![Plotly](https://img.shields.io/badge/Charts-Plotly-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🚀 AI Agent Internship Assignment — Moonshot

An **end-to-end AI-powered competitive intelligence platform** designed to analyze **pricing, sentiment, and competitive positioning** across top luggage brands on **Amazon India**.

This project combines:

* Automated Data Scraping
* Aspect-Level NLP Sentiment
* Competitive Benchmarking
* Anomaly Detection
* Generative AI Agent

To convert **raw Amazon data into strategic business intelligence.**

---

# 🎯 Project Highlights

✅ End-to-End Data Pipeline
✅ Aspect-Level NLP Sentiment Analysis
✅ Value-For-Money Index
✅ Trust & Anomaly Detection
✅ Interactive Competitive Dashboard
✅ Generative AI Agent Insights

---

# 📸 Dashboard Screenshots

## 📊 Market Overview Dashboard

Shows high-level metrics including:

* Total Brands
* Products Tracked
* Reviews Analyzed
* Market Average Price
* Price vs Sentiment Positioning

From your dashboard:

* 6 brands tracked
* 1200 products analyzed
* 372 reviews processed
* ₹3019 average price
* 76.1% positive sentiment 

<img width="1907" height="787" alt="image" src="https://github.com/user-attachments/assets/9d00c2bc-6fdd-4ba9-ac40-361f1c098660" />

---

## 🏆 Brand Comparison & Competitive Benchmarking

Includes:

* Average Price vs Discount
* Value-for-Money Index
* Sentiment Comparison
* Brand Ranking

Example Insights:

* Safari emerging as value leader
* American Tourister premium positioning
* Vip highest pricing cluster 

<img width="1886" height="801" alt="image" src="https://github.com/user-attachments/assets/167eae26-a980-44f4-9e4d-a5bc3b1b5e60" />


---

## 🔍 Product Drilldown Analysis

Granular product-level insights:

* Price
* Discount
* Rating
* Review Volume
* Hardware Sentiment

Example from Dashboard:

Safari flagged with anomaly:

> "High rating despite deep discounting — potential durability concerns" 

<img width="1868" height="991" alt="image" src="https://github.com/user-attachments/assets/5b42e8ec-24da-40e0-be25-26ec1b716927" />

---

## 🤖 AI Agent Strategic Insights

Generative AI Agent analyzes:

* Market gaps
* Competitive threats
* Pricing inefficiencies

Example Insights:

* Safari emerging as value leader
* Nasher Miles overpriced warning
* Premium positioning gaps detected 

<img width="1840" height="764" alt="image" src="https://github.com/user-attachments/assets/ca785922-eaef-4784-ae93-aecc09c167d8" />

---

# ✨ Key Features

## 🤖 Automated Data Pipeline

* Playwright-based scraping
* Extracts pricing, reviews, ratings
* Detects luggage size from titles
* Collects discount and brand data

---

## 🧠 Aspect-Level Sentiment Analysis

Analyzes hardware components:

* Wheels
* Zippers
* Handles
* Material
* Capacity

Uses:

* NLTK
* VADER
* Sentence-level scoring

---

## 💰 Value-For-Money Index

Custom metric:

```
(Sentiment Score / Avg Price) * 1000
```

Identifies:

* Budget disruptors
* Overpriced competitors
* Hidden value brands

---

## 🚨 Anomaly Detection

Flags:

* Suspicious high ratings
* Deep discount masking
* Poor hardware sentiment

---

## 🤖 Generative AI Agent

Uses **Google Gemini API** to generate:

* Competitive threats
* Market opportunities
* Product weaknesses
* Strategic recommendations

---

# 🛠️ Tech Stack

## Data Collection

* Python
* Playwright

## NLP & Processing

* Pandas
* NLTK
* Scikit-learn
* NumPy

## Dashboard

* Streamlit
* Plotly

## AI Agent

* Google Gemini API

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repo-link>
cd moonshot-dashboard
```

---

## Install Dependencies

```bash
pip install streamlit pandas numpy plotly scikit-learn nltk playwright google-generativeai
playwright install
```

---

# ▶️ Run Project

## Live Scraping Pipeline

```bash
python scraper.py
python review_scraper.py
python sentiment.py
streamlit run app.py
```

---

## Fallback Dataset (Recommended)

```bash
python bypass.py
streamlit run app.py
```

---

# 📁 Project Structure

```
app.py
scraper.py
review_scraper.py
sentiment.py
bypass.py
final_dataset.csv
reviews_with_sentiment.csv
README.md
```

---

# 🔍 Analytical Methodology

## Sentiment Calibration

Cross-checks:

* Star rating
* Review sentiment

Detects rating skew.

---

## Theme Extraction

Uses CountVectorizer with custom stop words:

Removes:

* good
* quality
* bag

Extracts hardware-specific insights.

---

## Market Positioning

Scatter Plot:

* X Axis → Price
* Y Axis → Sentiment

Identifies:

* Premium leaders
* Budget disruptors
* Overpriced competitors

---

# 💡 Business Impact

This dashboard enables:

* Competitive intelligence
* Product strategy decisions
* Pricing optimization
* Market gap discovery
* Customer pain-point detection

---

# 🏁 Future Improvements

* Real-time tracking
* Multi-category expansion
* Alert system
* ML clustering
* Demand forecasting

---

# ⭐ Why This Project Stands Out

Unlike traditional dashboards:

✅ AI Agent Powered
✅ Aspect Sentiment
✅ Anomaly Detection
✅ End-to-End Pipeline
✅ Strategic Intelligence

---

# 👩‍💻 Author

**Gnaneswari Khyati**
AI Agent Developer Candidate
