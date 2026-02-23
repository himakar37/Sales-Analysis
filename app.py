import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Professional Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# SIDEBAR SETTINGS
# -------------------------------------------------
st.sidebar.title("🎨 Dashboard Settings")

theme = st.sidebar.selectbox(
    "Select Theme",
    ["Light", "Dark", "Blue Corporate"]
)

# -------------------------------------------------
# THEME COLORS
# -------------------------------------------------
if theme == "Light":
    background = "#f4f6f9"
    card_color = "#ffffff"
    text_color = "black"

elif theme == "Dark":
    background = "#0e1117"
    card_color = "#1c1f26"
    text_color = "white"

elif theme == "Blue Corporate":
    background = "#e8f1f8"
    card_color = "#ffffff"
    text_color = "#0a3d62"

st.markdown(f"""
    <style>
        .main {{
            background-color: {background};
        }}
        div[data-testid="stMetric"] {{
            background-color: {card_color};
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4 {{
            color: {text_color};
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# COMPANY LOGO UPLOAD
# -------------------------------------------------
st.sidebar.subheader("🏢 Company Branding")

logo = st.sidebar.file_uploader(
    "Upload Company Logo",
    type=["png", "jpg", "jpeg"]
)

# -------------------------------------------------
# HEADER SECTION
# -------------------------------------------------
header_col1, header_col2 = st.columns([1, 4])

with header_col1:
    if logo is not None:
        image = Image.open(logo)
        st.image(image, width=120)

with header_col2:
    st.markdown("""
        <h1 style='margin-bottom:0;'>📊 Professional Sales Analytics Dashboard</h1>
        <p style='margin-top:0;'>Interactive Business Intelligence & Performance Insights</p>
    """, unsafe_allow_html=True)

st.divider()

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
uploaded_file = st.file_uploader("📂 Upload Sales CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Convert Date column
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month_name()

    # -------------------------------------------------
    # FILTER SECTION
    # -------------------------------------------------
    st.sidebar.header("🔍 Filters")

    if "Region" in df.columns:
        selected_region = st.sidebar.multiselect(
            "Select Region",
            df["Region"].unique(),
            default=df["Region"].unique()
        )
        df = df[df["Region"].isin(selected_region)]

    if "Category" in df.columns:
        selected_category = st.sidebar.multiselect(
            "Select Category",
            df["Category"].unique(),
            default=df["Category"].unique()
        )
        df = df[df["Category"].isin(selected_category)]

    # -------------------------------------------------
    # KPI SECTION
    # -------------------------------------------------
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df.shape[0]
    avg_order = total_sales / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
    col2.metric("📈 Total Profit", f"₹ {total_profit:,.0f}")
    col3.metric("🛒 Orders", total_orders)
    col4.metric("📊 Avg Order Value", f"₹ {avg_order:,.0f}")

    st.divider()

    # -------------------------------------------------
    # CHART SECTION (2 COLUMN LAYOUT)
    # -------------------------------------------------
    colA, colB = st.columns(2)

    # PIE CHART - CATEGORY
    if "Category" in df.columns:
        with colA:
            st.subheader("🥧 Sales by Category")
            category_sales = df.groupby("Category")["Sales"].sum()

            fig1, ax1 = plt.subplots()
            ax1.pie(category_sales, labels=category_sales.index, autopct='%1.1f%%')
            ax1.set_title("Category Distribution")
            st.pyplot(fig1)

    # BAR CHART - PRODUCT
    if "Product" in df.columns:
        with colB:
            st.subheader("📦 Top Products")
            product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

            fig2, ax2 = plt.subplots()
            sns.barplot(x=product_sales.values, y=product_sales.index, ax=ax2)
            ax2.set_title("Product Sales")
            st.pyplot(fig2)

    # -------------------------------------------------
    # MONTHLY TREND
    # -------------------------------------------------
    if "Month" in df.columns:
        st.subheader("📅 Monthly Sales Trend")

        monthly_sales = df.groupby("Month")["Sales"].sum()

        fig3, ax3 = plt.subplots()
        monthly_sales.plot(marker="o", ax=ax3)
        ax3.set_title("Monthly Sales")
        ax3.set_ylabel("Total Sales")
        st.pyplot(fig3)

    # -------------------------------------------------
    # PROFIT BY REGION
    # -------------------------------------------------
    if "Region" in df.columns and "Profit" in df.columns:
        st.subheader("🌍 Profit by Region")

        region_profit = df.groupby("Region")["Profit"].sum()

        fig4, ax4 = plt.subplots()
        region_profit.plot(kind="bar", ax=ax4)
        ax4.set_title("Region Profit")
        st.pyplot(fig4)

    # -------------------------------------------------
    # DATA TABLE
    # -------------------------------------------------
    st.subheader("📋 Detailed Data")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Upload a CSV file to start analysis.")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
---
<center>
Professional Sales Dashboard | Created by Himakar 🚀
</center>
""", unsafe_allow_html=True)