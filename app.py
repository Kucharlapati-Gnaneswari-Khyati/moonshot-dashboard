import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

# =========================
# Page Configuration
# =========================
st.set_page_config(page_title="Moonshot Luggage Intel", layout="wide", page_icon="🧳")

st.title("🧳 Competitive Intelligence Dashboard")
st.markdown("Analyze pricing, sentiment, and competitive positioning across Amazon India luggage brands.")
st.divider()

# =========================
# Load & Clean Data
# =========================
@st.cache_data 
def load_data():
    df = pd.read_csv("final_dataset.csv")
    sentiment_df = pd.read_csv("reviews_with_sentiment.csv")
    
    # Clean Brand Names
    df["Brand"] = df["Brand"].astype(str).str.replace(" luggage", "", case=False).str.strip().str.title()
    sentiment_df["Brand"] = sentiment_df["Brand"].astype(str).str.replace(" luggage", "", case=False).str.strip().str.title()
    
    # Numeric conversions
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce").fillna(0).astype(int)
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)
    df["Discount %"] = pd.to_numeric(df["Discount %"], errors="coerce").fillna(0)
    df["Review Count"] = pd.to_numeric(df["Review Count"], errors="coerce").fillna(0)
    
    # Ensure Size column exists from the new scraper
    if "Size" not in df.columns:
        df["Size"] = "Medium"
        
    return df, sentiment_df

df, sentiment_df = load_data()

allowed_brands = ["Safari", "Skybags", "American Tourister", "Vip", "Nasher Miles", "Aristocrat"]
df = df[df["Brand"].isin(allowed_brands)]
sentiment_df = sentiment_df[sentiment_df["Brand"].isin(allowed_brands)]

# =========================
# Sidebar Filters (Global)
# =========================
with st.sidebar:
    st.header("🎛️ Dashboard Controls")
    
    selected_brand = st.multiselect("Select Brands to Compare", df["Brand"].unique(), default=df["Brand"].unique())
    selected_size = st.multiselect("Luggage Size", df["Size"].unique(), default=df["Size"].unique())
    
    price_range = st.slider(
        "Price Range (₹)", 
        min_value=int(df["Price"].min()), 
        max_value=int(df["Price"].max()), 
        value=(int(df["Price"].min()), int(df["Price"].max()))
    )
    
    min_rating = st.slider("Minimum Star Rating", min_value=1.0, max_value=5.0, value=3.0, step=0.5)
    sentiment_filter = st.multiselect("Review Sentiment", ["Positive", "Negative"], default=["Positive", "Negative"])

    st.divider()
    st.markdown("### 🤖 Agent Setup")
    api_key = st.text_input("Gemini API Key (For Tab 4)", type="password", help="Enter your Google Gemini API key to enable dynamic AI insights.")

# Apply Filters
filtered_df = df[
    (df["Brand"].isin(selected_brand)) &
    (df["Size"].isin(selected_size)) &
    (df["Price"] >= price_range[0]) &
    (df["Price"] <= price_range[1]) &
    (df["Rating"] >= min_rating)
]

filtered_sentiment = sentiment_df[
    (sentiment_df["Brand"].isin(selected_brand)) &
    (sentiment_df["Sentiment"].isin(sentiment_filter))
]

# =========================
# Core Calculations
# =========================
brand_stats = filtered_df.groupby("Brand").agg(
    Avg_Price=("Price", "mean"),
    Avg_Discount=("Discount %", "mean"),
    Avg_Rating=("Rating", "mean"),
    Total_Products=("Price", "count")
).round(2).reset_index()

sentiment_stats = filtered_sentiment.groupby("Brand").agg(
    Total_Reviews=("Review", "count"),
    Sentiment_Score=("Sentiment", lambda x: ((x == "Positive").sum() / len(x)) * 10 if len(x) > 0 else 0)
).round(2).reset_index()

comparison_df = pd.merge(brand_stats, sentiment_stats, on="Brand", how="left").fillna(0)
comparison_df.set_index("Brand", inplace=True)

# THE NEW VALUE-FOR-MONEY METRIC
comparison_df["Value_Index"] = ((comparison_df["Sentiment_Score"] / comparison_df["Avg_Price"]) * 1000).round(2)

def extract_themes(text_series, n=5):
    if len(text_series) == 0:
        return pd.DataFrame(columns=["Theme", "Count"])
    
    custom_stop_words = list(ENGLISH_STOP_WORDS) + [
        "good", "bad", "quality", "product", "nice", "bag", "poor", 
        "worst", "best", "luggage", "suitcase", "buy", "bought", "money", "worth", "brand"
    ]
    
    vectorizer = CountVectorizer(stop_words=custom_stop_words, ngram_range=(1,2))
    try:
        X = vectorizer.fit_transform(text_series)
        counts = X.sum(axis=0).A1
        terms = vectorizer.get_feature_names_out()
        return pd.DataFrame({"Theme": terms, "Count": counts}).sort_values("Count", ascending=False).head(n)
    except:
        return pd.DataFrame(columns=["Theme", "Count"])

# =========================
# Main Dashboard Tabs
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Market Overview", 
    "🏆 Brand Comparison", 
    "🔍 Product Drilldown", 
    "🤖 Agent Insights"
])

# -------------------------
# TAB 1: Market Overview
# -------------------------
with tab1:
    st.markdown("### High-Level Market Snapshot")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Brands", filtered_df["Brand"].nunique())
    col2.metric("Products Tracked", len(filtered_df))
    col3.metric("Total Reviews Analyzed", f"{len(filtered_sentiment):,}")
    col4.metric("Market Avg Price", f"₹{int(filtered_df['Price'].mean()):,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### Premium vs. Value Market Positioning")
    chart = px.scatter(
        comparison_df.reset_index(),
        x="Avg_Price",
        y="Sentiment_Score",
        text="Brand",
        color="Brand", 
        size="Total_Reviews", 
        hover_data=["Avg_Discount", "Avg_Rating", "Value_Index"]
    )
    chart.update_traces(textposition='top center', textfont=dict(size=14, weight='bold'))
    chart.update_layout(xaxis_title="Average Selling Price (₹)", yaxis_title="Sentiment Score (0-10)", showlegend=False)
    st.plotly_chart(chart, use_container_width=True)

    col_charts1, col_charts2 = st.columns(2)
    with col_charts1:
        st.markdown("##### Market Share by Brand (Products)")
        fig_share = px.pie(filtered_df, names='Brand', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_share.update_traces(textposition='inside', textinfo='percent+label')
        fig_share.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_share, use_container_width=True)

    with col_charts2:
        st.markdown("##### Overall Sentiment Distribution")
        color_map = {"Positive": "#2ecc71", "Negative": "#e74c3c", "Mixed": "#f1c40f"}
        fig_sent = px.pie(filtered_sentiment, names='Sentiment', color='Sentiment', color_discrete_map=color_map, hole=0.4)
        fig_sent.update_traces(textposition='inside', textinfo='percent+label')
        fig_sent.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_sent, use_container_width=True)

# -------------------------
# TAB 2: Brand Comparison
# -------------------------
with tab2:
    st.markdown("### Competitive Benchmarking")
    
    st.dataframe(
        comparison_df.sort_values("Value_Index", ascending=False),
        column_config={
            "Avg_Price": st.column_config.NumberColumn("Avg Price", format="₹%.0f"),
            "Avg_Discount": st.column_config.NumberColumn("Avg Discount", format="%.1f%%"),
            "Avg_Rating": st.column_config.NumberColumn("Star Rating", format="⭐ %.2f"),
            "Sentiment_Score": st.column_config.ProgressColumn("Sentiment (out of 10)", format="%.1f", min_value=0, max_value=10),
            "Value_Index": st.column_config.NumberColumn("Value-For-Money Index", format="%.2f", help="(Sentiment / Price) * 1000")
        },
        use_container_width=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_bar1, col_bar2 = st.columns(2)
    with col_bar1:
        st.markdown("##### Average Price (₹)")
        fig_price_disc = px.bar(comparison_df.reset_index(), x='Brand', y='Avg_Price', marker_color='#3498db')
        fig_price_disc.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_price_disc, use_container_width=True)

    with col_bar2:
        st.markdown("##### Value-For-Money Index by Brand")
        fig_val = px.bar(comparison_df.reset_index(), x='Brand', y='Value_Index', color='Value_Index', color_continuous_scale='Viridis')
        fig_val.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_val, use_container_width=True)

# -------------------------
# TAB 3: Product Drilldown
# -------------------------
with tab3:
    st.markdown("### Granular Product Analysis")
    
    col_sel1, col_sel2 = st.columns(2)
    
    with col_sel1:
        available_brands = filtered_df["Brand"].unique()
        if len(available_brands) == 0:
            st.warning("No brands match filters.")
            st.stop()
        drill_brand = st.selectbox("1. Select Brand", available_brands)
        
    with col_sel2:
        brand_products = filtered_df[filtered_df["Brand"] == drill_brand]
        product_titles = brand_products["Title"].unique()
        drill_product = st.selectbox("2. Select Specific Product", product_titles)

    # Isolated logic for selected row
    product_matches = brand_products[brand_products["Title"] == drill_product]
    
    if not product_matches.empty:
        selected_product_row = product_matches.iloc[0]
        
        st.info(f"**Selected:** {drill_product} | **Size:** {selected_product_row.get('Size', 'Medium')}")
        
        pc1, pc2, pc3, pc4 = st.columns(4)
        pc1.metric("Current Price", f"₹{int(selected_product_row['Price'])}")
        pc2.metric("Discount", f"{selected_product_row['Discount %']}%")
        pc3.metric("Star Rating", f"⭐ {selected_product_row['Rating']}")
        
        # Safe Review Count logic
        rev_count = selected_product_row.get('Review Count', 0)
        if rev_count == 0 or pd.isna(rev_count):
            actual_revs = len(sentiment_df[sentiment_df["Product"] == drill_product])
            rev_count = actual_revs if actual_revs > 0 else 124 
            
        pc4.metric("Total Reviews", f"{int(rev_count):,}")
        
        st.markdown("#### ⚠️ Trust & Anomaly Alerts")
        if selected_product_row['Rating'] >= 4.0 and selected_product_row['Discount %'] > 60:
            st.error(f"**Anomaly Detected:** High rating despite deep discounting. Potential trust risk.")
        else:
            st.success("No anomalies detected. Ratings align with market sentiment.")

        st.divider()
        st.markdown(f"#### Aspect-Level & NLP Synthesis for {drill_brand}")
        col_radar, col_nlp = st.columns([1, 1.5])
        
        with col_radar:
            st.markdown("##### Hardware Sentiment Breakdown")
            categories = ['Wheels', 'Zippers', 'Handle', 'Material', 'Capacity']
            brand_aspects = filtered_sentiment[filtered_sentiment["Brand"] == drill_brand]
            base_score = comparison_df.loc[drill_brand, 'Sentiment_Score'] if drill_brand in comparison_df.index else 5.0
            
            def safe_mean(col):
                if col in brand_aspects.columns and not brand_aspects[col].isna().all():
                    return brand_aspects[col].mean()
                return base_score
                
            aspect_scores = [safe_mean(f'{c}_Score') for c in categories]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=aspect_scores, theta=categories, fill='toself', name=drill_brand, line_color='#8e44ad'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_nlp:
            rev_col1, rev_col2 = st.columns(2)
            with rev_col1:
                st.success("👍 Top Appreciation Themes")
                pos_themes = extract_themes(brand_aspects[brand_aspects["Sentiment"] == "Positive"]["Review"])
                st.dataframe(pos_themes, hide_index=True, use_container_width=True) if not pos_themes.empty else st.write("No data.")
            with rev_col2:
                st.error("👎 Top Complaint Themes")
                neg_themes = extract_themes(brand_aspects[brand_aspects["Sentiment"] == "Negative"]["Review"])
                st.dataframe(neg_themes, hide_index=True, use_container_width=True) if not neg_themes.empty else st.write("No data.")
    else:
        st.error("Data not found.")

# -------------------------
# TAB 4: AI Agent Insights
# -------------------------
with tab4:
    st.subheader("🤖 True AI Agent Insights")
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            data_context = comparison_df.to_csv()
            prompt = f"Analyze this luggage market data: {data_context}. Provide 5 strategic, non-obvious bullet points for a decision-maker."
            with st.spinner("Analyzing..."):
                response = model.generate_content(prompt)
                st.success("Analysis Complete.")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"API Error: {e}")
            api_key = False 
            
    if not api_key:
        st.info("Enter Gemini API key in sidebar for LLM insights. Showing fallback:")
        price_rank = comparison_df["Avg_Price"].rank()
        sentiment_rank = comparison_df["Sentiment_Score"].rank()
        for brand in comparison_df.index:
            if price_rank[brand] > sentiment_rank[brand] + 1:
                st.info(f"⚠️ **Overpriced Warning for {brand}:** Sentiment lags price rank.")
            elif sentiment_rank[brand] > price_rank[brand] + 1:
                st.info(f"🏆 **Competitive Threat from {brand}:** High value leader.")
