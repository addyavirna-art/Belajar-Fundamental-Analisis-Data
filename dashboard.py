import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from matplotlib.ticker import FuncFormatter

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Olist E-Commerce Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

# Custom CSS untuk mempercantik tampilan (Gaya Profesional)
st.markdown("""
    <style>
    .main { background-color: #f6f8fb; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dce4ec;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #183153; }
    </style>
    """, unsafe_allow_html=True)

# Formatters
currency_formatter = FuncFormatter(lambda x, pos: f"R${x:,.0f}")
percent_formatter = FuncFormatter(lambda x, pos: f"{x:.1%}")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Mengambil main_data.csv dari folder yang sama
    data_path = Path(__file__).resolve().parent / "main_data.csv"
    df = pd.read_csv(data_path)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

try:
    main_df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data. Pastikan 'main_data.csv' ada di folder dashboard. Error: {e}")
    st.stop()

# --- SIDEBAR FILTER ---
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png", width=200)
    st.header("Filter Transaksi")
    
    # Filter Rentang Tanggal
    min_date = main_df["order_purchase_timestamp"].min().date()
    max_date = main_df["order_purchase_timestamp"].max().date()
    
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Filter State (Wilayah)
    all_states = sorted(main_df["customer_state"].unique())
    selected_states = st.multiselect("Pilih Wilayah (State)", all_states, default=all_states)

# Filter Logic
filtered_df = main_df[
    (main_df["order_purchase_timestamp"].dt.date >= start_date) & 
    (main_df["order_purchase_timestamp"].dt.date <= end_date) &
    (main_df["customer_state"].isin(selected_states))
]

# --- MAIN PAGE ---
st.title("Brazilian E-Commerce Dashboard :bar_chart:")
st.markdown("Dashboard ini menyajikan analisis performa bisnis Olist berdasarkan data historis 2017-2018.")

# Kolom Informasi Bisnis (Expander)
with st.expander("Pertanyaan Bisnis"):
    st.write("1. Bagaimana tren jumlah pesanan & pendapatan serta kategori apa yang paling dominan?")
    st.write("2. Bagaimana tingkat keterlambatan pengiriman dan dampaknya pada rating?")
    st.write("3. Wilayah mana yang memiliki konsentrasi pelanggan terbanyak?")

# --- KEY METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_orders = filtered_df["order_id"].nunique()
    st.metric("Total Orders", f"{total_orders:,}")
with col2:
    total_revenue = filtered_df["revenue"].sum()
    st.metric("Total Revenue", f"R${total_revenue:,.0f}")
with col3:
    avg_score = filtered_df["review_score_mean"].mean()
    st.metric("Avg Review Score", f"{avg_score:.2f} / 5.0")
with col4:
    late_rate = filtered_df["is_late"].mean()
    st.metric("Late Delivery Rate", f"{late_rate:.1%}")

st.divider()

# --- VISUALIZATION 1: TRENDS & CATEGORIES ---
st.subheader("1. Tren Performa Bisnis & Kategori Unggulan")
tab1, tab2 = st.tabs(["Monthly Trend", "Product Categories"])

with tab1:
    # Agregasi Bulanan
    monthly_df = filtered_df.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "revenue": "sum"
    }).reset_index()
    monthly_df["order_purchase_timestamp"] = monthly_df["order_purchase_timestamp"].dt.strftime('%B %Y')

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=monthly_df, x="order_purchase_timestamp", y="order_id", marker="o", color="#1f4e79", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.caption("Grafik menunjukkan tren pesanan bulanan. Terjadi lonjakan signifikan pada November 2017.")

with tab2:
    # Top Kategori (Hardcoded names for demo based on common Olist data)
    # Catatan: Sesuaikan dengan kolom kategori di main_data.csv kamu
    st.write("Kategori Produk Teratas Berdasarkan Pendapatan")
    # Di sini diasumsikan ada kolom product_category_name_english
    if "product_category_name_english" in filtered_df.columns:
        top_cat = filtered_df.groupby("product_category_name_english")["revenue"].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=top_cat.values, y=top_cat.index, palette="viridis", ax=ax)
        ax.xaxis.set_major_formatter(currency_formatter)
        st.pyplot(fig)
    else:
        st.info("Tambahkan kolom kategori produk di notebook untuk melihat grafik ini.")

st.divider()

# --- VISUALIZATION 2: DELIVERY & REGION ---
st.subheader("2. Analisis Pengiriman & Wilayah")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**10 Wilayah dengan Konsentrasi Pelanggan Terbanyak**")
    state_cust = filtered_df.groupby("customer_state")["customer_unique_id"].nunique().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=state_cust.index, y=state_cust.values, color="#2a9d8f", ax=ax)
    st.pyplot(fig)

with col_b:
    st.markdown("**Dampak Keterlambatan pada Rating**")
    if "is_late" in filtered_df.columns:
        late_impact = filtered_df.groupby("is_late")["review_score_mean"].mean()
        fig, ax = plt.subplots()
        sns.barplot(x=late_impact.index.map({True: 'Terlambat', False: 'Tepat Waktu'}), y=late_impact.values, palette="Reds_r")
        plt.ylim(0, 5)
        st.pyplot(fig)
        st.caption("Pesanan yang terlambat secara signifikan menurunkan kepuasan pelanggan.")

st.caption("Copyright (c) 2024 - Addya | Proyek Analisis Data Dicoding")
