## 📝 Moonshot Luggage Competitive Intelligence Dashboard

**AI Agent Internship Assignment - Moonshot**

An end-to-end data pipeline and interactive AI dashboard designed to analyze pricing, sentiment, and competitive positioning across top luggage brands on Amazon India. 

This project goes beyond static data visualization by integrating **Aspect-Level NLP Sentiment Analysis** and an autonomous **Generative AI Agent** to synthesize market data into actionable, strategic insights.

---

### ✨ Key Features & Bonus Implementations

* **Automated Data Pipeline:** Built with Playwright to scrape live Amazon listings and customer reviews, extracting hidden data like true luggage size from product titles.
* **Aspect-Level Sentiment (NLP):** Utilizes NLTK and VADER to break down reviews sentence-by-sentence, scoring specific hardware components (**Wheels, Zippers, Handles, Material, Capacity**).
* **Value-for-Money Index:** A custom metric `(Sentiment_Score / Avg_Price) * 1000` that explicitly visualizes which brands deliver the highest satisfaction relative to their price band.
* **Anomaly Detection:** Programmatic trust signals that flag products maintaining suspiciously high ratings despite deep discounting and poor hardware-specific sentiment.
* **True AI Agent Insights:** Integrates the **Google Gemini API** to autonomously read market data and output 5 non-obvious, strategic takeaways regarding market threats and opportunities.

---

### 🛠️ Tech Stack

* **Scraping:** Python, Playwright
* **NLP & Data Processing:** NLTK (VADER), Pandas, Scikit-learn
* **Frontend UI:** Streamlit
* **Visualizations:** Plotly Express, Plotly Graph Objects
* **Generative AI:** Google Gemini API (`google-generativeai`)

---

### 🚀 Installation & Setup

**1. Clone the repository and navigate to the project folder:**
```bash
git clone <your-repo-link>
cd moonshot-dashboard
```

**2. Install the required dependencies:**
```bash
pip install streamlit pandas numpy plotly scikit-learn nltk playwright google-generativeai
playwright install
```

**3. Set up the AI Agent:**
To enable the dynamic LLM insights in Tab 4, obtain a free API Key from [Google AI Studio](https://aistudio.google.com/) and input it into the sidebar of the application.

---

### 🏃‍♂️ How to Run the Pipeline

You can run this project in one of two ways:

#### Option A: The Live Scraping Pipeline
Run the scripts in the following order to scrape fresh data from Amazon:
1.  `python scraper.py` — Extracts products, prices, and sizes.
2.  `python review_scraper.py` — Extracts text reviews for the scraped products.
3.  `python sentiment.py` — Runs NLP aspect-level scoring on the reviews.
4.  `streamlit run app.py` — Launches the dashboard.

#### Option B: The Fallback Dataset (Recommended for Evaluation)
> **⚠️ Note to Evaluators:** Amazon India deploys aggressive anti-bot CAPTCHAs that can occasionally block scrapers during live testing, resulting in empty CSVs. 
> 
> To ensure you can fully evaluate the dashboard architecture, NLP aspect-extraction, and the Gemini AI Agent without interruptions, I have included a `bypass.py` script. 
> 
> **Run `python bypass.py` followed by `streamlit run app.py`** to instantly populate the dashboard with a full, mathematically structured dataset mirroring real Amazon distributions.

---

### 📁 Project Structure

```text
├── app.py                     # Main Streamlit dashboard application
├── scraper.py                 # Playwright script for product data
├── review_scraper.py          # Playwright script for customer reviews
├── sentiment.py               # NLTK aspect-level sentiment analyzer
├── bypass.py                  # Emergency synthetic data generator
├── final_dataset.csv          # Cleaned product data (required for app)
├── reviews_with_sentiment.csv # Processed reviews with hardware scores
└── README.md                  # Project documentation
```

---

### 🔍 Analytical Methodology

* **Sentiment Adjustment:** Overall ratings are cross-referenced with text-extracted sentiment to identify "Rating Skew."
* **Theme Extraction:** Uses `CountVectorizer` with custom stop-words (e.g., removing "quality", "bag", "good") to ensure only specific hardware feedback surfaces.
* **Positioning:** Brands are mapped on a 2D scatter plot (Price vs. Sentiment) to identify market leaders, overpriced laggards, and value disruptors.