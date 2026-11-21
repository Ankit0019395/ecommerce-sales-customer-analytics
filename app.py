import pandas as pd
import streamlit as st

st.set_page_config(page_title="E-commerce Sales & Customer Analytics", layout="wide")


@st.cache_data
def load(name):
    return pd.read_csv(f"dashboard_data/{name}.csv")


monthly = load("monthly_sales")
cats = load("top_categories")
segments = load("rfm_segments")
clusters = load("kmeans_clusters")
states = load("delivery_by_state")

st.title("E-commerce Sales & Customer Analytics")
st.caption("Olist Brazilian e-commerce dataset, Jan 2017 to Aug 2018. Amounts in R$.")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total revenue", f"R$ {monthly['revenue'].sum() / 1e6:.1f}M")
k2.metric("Total orders", f"{monthly['orders'].sum():,}")
k3.metric("Customers who bought twice", "3.0%")
k4.metric("Late deliveries", "8.1%")

tab1, tab2, tab3, tab4 = st.tabs(["Sales", "Customers", "Delivery", "Key findings"])

with tab1:
    st.subheader("Monthly revenue")
    st.line_chart(monthly.set_index("purchase_month")["revenue"])
    left, right = st.columns(2)
    with left:
        st.subheader("Average order value")
        st.line_chart(monthly.set_index("purchase_month")["avg_order_value"])
    with right:
        st.subheader("Top 10 categories by revenue")
        st.bar_chart(cats.set_index("product_category_name_english")["price"])

with tab2:
    st.subheader("RFM segments (business rules)")
    st.dataframe(segments, use_container_width=True)
    st.caption("Share of customers vs share of revenue (%)")
    st.bar_chart(segments.set_index("segment")[["pct_customers", "pct_revenue"]])

    st.subheader("K-Means clusters")
    names = {
        0: "Recent Budget Buyers",
        1: "High-Value One-Timers",
        2: "Repeat Buyers",
        3: "Dormant One-Timers",
    }
    clusters["name"] = clusters["cluster"].map(names)
    st.dataframe(clusters, use_container_width=True)

with tab3:
    a, b = st.columns(2)
    a.metric("Avg review, on-time orders", "4.29")
    b.metric("Avg review, late orders", "2.57")
    c, d = st.columns(2)
    c.metric("Repeat rate after on-time first order", "3.13%")
    d.metric("Repeat rate after late first order", "2.62%")

    st.subheader("Average delivery days by state (states with 100+ orders)")
    s = states[states["count"] > 100].sort_values("mean")
    st.bar_chart(s.set_index("customer_state")["mean"])

with tab4:
    st.markdown(
        """
- Revenue grew about 5.6x in 2017 through order volume, not bigger baskets, peaked at Black Friday (Nov 2017), then plateaued in 2018.
- 97% of customers never bought twice.
- One cluster (30% of customers, high-value one-time buyers) generates 58% of revenue.
- Late deliveries (8%) score 1.7 stars lower and cut repeat purchases by about 16%.
- Even 5-star customers repurchase only about 3% of the time, so retention needs active programs (follow-up offers, loyalty rewards), not just better service.
"""
    )