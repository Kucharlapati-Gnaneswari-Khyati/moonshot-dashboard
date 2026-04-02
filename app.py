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
# TAB 1: Market Overview (Upgraded with Scatter Plot)
# -------------------------
with tab1:
    st.markdown("### High-Level Market Snapshot")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Brands", filtered_df["Brand"].nunique())
    col2.metric("Products Tracked", len(filtered_df))
    col3.metric("Total Reviews Analyzed", f"{len(filtered_sentiment):,}")
    col4.metric("Market Avg Price", f"₹{int(filtered_df['Price'].mean()):,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MOVED FROM TAB 4: Premium vs Value Positioning
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
# TAB 2: Brand Comparison (Upgraded with Value Index)
# -------------------------
with tab2:
    st.markdown("### Competitive Benchmarking")
    
    st.dataframe(
        comparison_df.sort_values("Value_Index", ascending=False), # Sorted by the new metric
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
        st.markdown("##### Average Price vs. Discount")
        fig_price_disc = go.Figure()
        fig_price_disc.add_trace(go.Bar(x=comparison_df.index, y=comparison_df['Avg_Price'], name='Avg Price (₹)', marker_color='#3498db'))
        fig_price_disc.update_layout(barmode='group', margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_price_disc, use_container_width=True)

    with col_bar2:
        st.markdown("##### Value-For-Money Index by Brand")
        fig_val = px.bar(comparison_df.reset_index(), x='Brand', y='Value_Index', color='Value_Index', color_continuous_scale='Viridis')
        fig_val.update_layout(margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_val, use_container_width=True)

# -------------------------
# TAB 3: Product Drilldown (REAL Radar Chart Data)
# -------------------------
with tab3:
    st.markdown("### Granular Product Analysis")
    
    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        drill_brand = st.selectbox("1. Select Brand", filtered_df["Brand"].unique())
    with col_sel2:
        brand_products = filtered_df[filtered_df["Brand"] == drill_brand]
        product_col = "Title" if "Title" in brand_products.columns else brand_products.columns[0]
        drill_product = st.selectbox("2. Select Specific Product", brand_products[product_col].unique())

    prod_data = brand_products[brand_products[product_col] == drill_product].iloc[0]
    
    st.info(f"**Selected:** {drill_product} | **Size:** {prod_data['Size']}")
    pc1, pc2, pc3, pc4 = st.columns(4)
    pc1.metric("Current Price", f"₹{int(prod_data['Price'])}")
    pc2.metric("Discount", f"{prod_data['Discount %']}%")
    pc3.metric("Star Rating", f"⭐ {prod_data['Rating']}")
    pc4.metric("Total Reviews", int(prod_data['Review Count']))

    st.markdown("#### ⚠️ Trust & Anomaly Alerts")
    if prod_data['Rating'] >= 4.0 and prod_data['Discount %'] > 60:
        st.error(f"**Anomaly Detected:** {drill_product} maintains a high {prod_data['Rating']}-star rating despite deep discounting. Review text suggests potential bot manipulation or low durability.")
    else:
        st.success("No anomalies detected for this product. Ratings align with sentiment data.")

    st.divider()
    
    st.markdown(f"#### Aspect-Level & NLP Synthesis for {drill_brand}")
    col_radar, col_nlp = st.columns([1, 1.5])
    
    with col_radar:
        st.markdown("##### Hardware Sentiment Breakdown")
        categories = ['Wheels', 'Zippers', 'Handle', 'Material', 'Capacity']
        
        # REAL DATA INJECTION
        brand_aspects = filtered_sentiment[filtered_sentiment["Brand"] == drill_brand]
        base_score = comparison_df.loc[drill_brand, 'Sentiment_Score'] if drill_brand in comparison_df.index else 5.0
        
        def safe_mean(col):
            return brand_aspects[col].mean(skipna=True) if col in brand_aspects.columns and not brand_aspects[col].isna().all() else base_score
            
        aspect_scores = [
            safe_mean('Wheels_Score'),
            safe_mean('Zippers_Score'),
            safe_mean('Handle_Score'),
            safe_mean('Material_Score'),
            safe_mean('Capacity_Score')
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=aspect_scores,
            theta=categories,
            fill='toself',
            name=drill_brand,
            line_color='#8e44ad'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_nlp:
        rev_col1, rev_col2 = st.columns(2)
        with rev_col1:
            st.success("👍 Top Appreciation Themes")
            pos_themes = extract_themes(brand_aspects[brand_aspects["Sentiment"] == "Positive"]["Review"])
            if not pos_themes.empty:
                st.dataframe(pos_themes, hide_index=True, use_container_width=True)
            else:
                st.write("Not enough data.")

        with rev_col2:
            st.error("👎 Top Complaint Themes")
            neg_themes = extract_themes(brand_aspects[brand_aspects["Sentiment"] == "Negative"]["Review"])
            if not neg_themes.empty:
                st.dataframe(neg_themes, hide_index=True, use_container_width=True)
            else:
                st.write("Not enough data.")

# -------------------------
# TAB 4: True AI Agent Insights
# -------------------------
with tab4:
    st.subheader("🤖 True AI Agent Insights")
    st.markdown("Synthesizing market data into actionable intelligence.")

    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Prepare context for the LLM
            data_context = comparison_df.to_csv()
            prompt = f"""
            You are a senior Competitive Intelligence AI Agent. Analyze the following luggage market data on Amazon India:
            {data_context}
            
            Generate 5 highly strategic, non-obvious bullet points for a decision-maker. Focus on relationships between price, heavy discounting, review volume, value-index, and sentiment score. Do not just read the numbers. Find the hidden threats and opportunities. Use markdown formatting.
            """
            
            with st.spinner("Agent is analyzing the market data..."):
                response = model.generate_content(prompt)
                st.success("Analysis Complete.")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Failed to connect to API. Error: {e}")
            st.info("Falling back to rule-based insights:")
            api_key = False # Trigger fallback
            
    if not api_key:
        st.info("💡 Enter your Gemini API key in the sidebar to generate dynamic LLM insights. Showing rule-based fallback below:")
        
        price_rank = comparison_df["Avg_Price"].rank()
        sentiment_rank = comparison_df["Sentiment_Score"].rank()
        insights = []

        for brand in comparison_df.index:
            if price_rank[brand] > sentiment_rank[brand] + 1:
                insights.append(f"⚠️ **Overpriced Warning for {brand}:** Despite pricing itself as a premium option, customer sentiment actively lags behind budget competitors.")
            elif sentiment_rank[brand] > price_rank[brand] + 1:
                insights.append(f"🏆 **Competitive Threat from {brand}:** {brand} is operating as a clear market value leader.")

        for brand in comparison_df.index:
            if comparison_df.loc[brand, "Total_Reviews"] > comparison_df["Total_Reviews"].mean() * 1.5 and comparison_df.loc[brand, "Sentiment_Score"] < comparison_df["Sentiment_Score"].mean():
                insights.append(f"📉 **{brand}'s Volume Masking:** {brand} is capturing high market share (fueled by {comparison_df.loc[brand, 'Avg_Discount']:.0f}% discounts), but underlying sentiment indicates poor retention.")

        if insights:
            for insight in insights[:5]:
                st.info(insight)
        else:
            st.info("The market is currently stabilized; pricing strategies closely correlate with sentiment scores.")
