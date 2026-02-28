# M.Himakar,rollno:33
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark", "Blue"])

if theme == "Dark":
    st.markdown("<style>body{background:#0e1117;color:white;}</style>", unsafe_allow_html=True)

logo = st.sidebar.file_uploader("Upload Logo", type=["png","jpg","jpeg"])

# ---------------- HEADER ----------------
col1, col2 = st.columns([1,4])
with col1:
    if logo:
        st.image(Image.open(logo), width=100)
with col2:
    st.title("📊 Professional Sales Dashboard")
    st.write("Business Performance Overview")

st.divider()

# ---------------- FILE UPLOAD ----------------
file = st.file_uploader("Upload Sales CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    # Date Handling
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.month_name()

    # ---------------- FILTERS ----------------
    st.sidebar.header("Filters")

    if "Region" in df.columns:
        region = st.sidebar.multiselect("Region", df["Region"].unique(), df["Region"].unique())
        df = df[df["Region"].isin(region)]

    if "Category" in df.columns:
        category = st.sidebar.multiselect("Category", df["Category"].unique(), df["Category"].unique())
        df = df[df["Category"].isin(category)]

    # ---------------- KPIs ----------------
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    orders = len(df)
    avg_order = total_sales/orders if orders else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("💰 Sales", f"₹ {total_sales:,.0f}")
    c2.metric("📈 Profit", f"₹ {total_profit:,.0f}")
    c3.metric("🛒 Orders", orders)
    c4.metric("📊 Avg Order", f"₹ {avg_order:,.0f}")

    st.divider()

    # ---------------- CHARTS ----------------
    colA,colB = st.columns(2)

    if "Category" in df.columns:
        with colA:
            st.subheader("Sales by Category")
            data = df.groupby("Category")["Sales"].sum()
            fig, ax = plt.subplots()
            ax.pie(data, labels=data.index, autopct="%1.1f%%")
            st.pyplot(fig)

    if "Product" in df.columns:
        with colB:
            st.subheader("Top Products")
            data = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
            fig, ax = plt.subplots()
            ax.barh(data.index, data.values)
            ax.invert_yaxis()
            st.pyplot(fig)

    if "Month" in df.columns:
        st.subheader("Monthly Sales Trend")
        data = df.groupby("Month")["Sales"].sum()
        fig, ax = plt.subplots()
        ax.plot(data.index, data.values, marker="o")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    if "Region" in df.columns:
        st.subheader("Profit by Region")
        data = df.groupby("Region")["Profit"].sum()
        fig, ax = plt.subplots()
        ax.bar(data.index, data.values)
        st.pyplot(fig)

    # ---------------- DATA TABLE ----------------
    st.subheader("Detailed Data")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Upload a CSV file to begin.")

st.markdown("---")
st.markdown("Created by Himakar 🚀")
