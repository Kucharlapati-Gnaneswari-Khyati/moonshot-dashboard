# 🧠 Munshot Luggage Competitive Intelligence Dashboard

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
---

# 🎯 Problem Statement

Companies launching luggage products lack structured competitive intelligence.

Competitor data exists across marketplaces like Amazon, but:

- Pricing trends are unclear
- Customer sentiment is scattered
- Product strengths & weaknesses are hidden
- Market gaps are difficult to identify

This project solves this by building an AI-powered competitive intelligence dashboard that:

- Collects competitor product data
- Analyzes customer sentiment
- Extracts product themes
- Generates market insights

This helps decision-makers understand where to compete and how to improve products.

An **end-to-end AI-powered competitive intelligence platform** designed to analyze **pricing, sentiment, and competitive positioning** across top luggage brands on **Amazon India**.

This project combines:

* Automated Data Scraping
* Aspect-Level NLP Sentiment
* Competitive Benchmarking
* Anomaly Detection
* Generative AI Agent

To convert **raw Amazon data into strategic business intelligence.**
## 🏗️ System Architecture

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/c68c3d7d-9062-48d6-a170-b19682910568" />

The system follows a multi-layer AI architecture consisting of data acquisition, NLP processing, autonomous intelligence, and presentation layers. Data flows from Amazon scraping to sentiment analysis, anomaly detection, and AI-generated strategic insights displayed in an interactive Streamlit dashboard.
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

<img width="1865" height="752" alt="image" src="https://github.com/user-attachments/assets/89c7c3d2-b80a-4d15-81c0-200a5a2277cb" />

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

<img width="1895" height="640" alt="image" src="https://github.com/user-attachments/assets/e0814a3b-3cb4-4d6f-bd36-5d45f7c606b0" />

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
# 📊 Cleaned Dataset

The dashboard uses cleaned datasets generated from the pipeline:

- final_dataset.csv — Product data
- reviews.csv — Generated reviews
- reviews_with_sentiment.csv — Sentiment analysis results

These datasets are used directly by the dashboard.

Dataset includes:

- Product Name
- Brand
- Price
- Rating
- Reviews
- Sentiment Score
- Extracted Themes

These datasets are included in the repository and used directly by the dashboard.
# 🧭 Project Approach

The project follows an end-to-end AI competitive intelligence pipeline:

1. Data Collection  
Scrape competitor luggage products from Amazon India

2. Data Cleaning  
Remove duplicates and normalize pricing and ratings

3. Sentiment Analysis  
Perform aspect-level sentiment analysis on product reviews

4. Theme Extraction  
Extract customer pain points and strengths

5. Competitive Intelligence  
Compare brands across price, sentiment, and value

6. Dashboard Visualization  
Display insights in interactive Streamlit dashboard

7. AI Agent Insights  
Generate strategic recommendations using Gemini API
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

This dashboard enables product and strategy teams to make data-driven decisions:

## Product Strategy
- Identify competitor strengths and weaknesses
- Detect durability complaints and feature gaps
- Improve hardware quality decisions

## Pricing Strategy
- Detect overpriced competitors
- Identify value-for-money leaders
- Optimize pricing positioning

## Competitive Intelligence
- Compare brands across sentiment and pricing
- Identify premium vs budget clusters
- Detect emerging challenger brands

## Customer Insights
- Understand customer pain points
- Identify most discussed product features
- Track sentiment trends across brands

This transforms raw marketplace data into actionable business intelligence.
---
# ⚠️ Limitations

- Dataset limited to selected luggage brands
- Static scraping (not real-time monitoring)
- Limited review sample size
- Sentiment model based on rule-based VADER
- No historical trend tracking
- Amazon-only data source

These limitations can be addressed in future iterations.

---
# 🚀 Future Improvements

## Real-Time Competitive Monitoring
- Scheduled scraping
- Daily competitor tracking

## Multi-Marketplace Expansion
- Flipkart
- Myntra
- Brand websites

## Advanced AI Intelligence
- LLM-based review summarization
- Trend prediction
- Market opportunity detection

## Alert System
- Competitor price drop alerts
- Sentiment drop alerts
- New product launch alerts

## Advanced Analytics
- ML clustering
- Demand forecasting
- Market share estimation

---

# ⭐ Why This Project Stands Out

Unlike traditional dashboards:

✅ AI Agent Powered
✅ Aspect Sentiment
✅ Anomaly Detection
✅ End-to-End Pipeline
✅ Strategic Intelligence

---
# 📦 Submission Contents

This submission includes:

✅ Working Dashboard  
✅ Source Code  
✅ README with setup and approach  
✅ Cleaned dataset  

Recommended additions:

✅ Architecture diagram  
✅ Dashboard screenshots  
✅ Notes on limitations and improvements  

# 👩‍💻 Author

**Gnaneswari Khyati**
AI Agent Developer Candidate
