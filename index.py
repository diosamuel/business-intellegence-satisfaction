import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# Load dataset
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    layout="wide"  # <- this makes it full-width
)
st.title("Customer Demographics vs Purchase Intent")
st.write("This dataset provides insights into consumer electronics sales, featuring product categories, brands, prices, customer demographics, purchase behavior, and satisfaction metrics. It aims to analyze factors influencing purchase intent and customer satisfaction in the consumer electronics market.")
st.write("https://www.kaggle.com/datasets/rabieelkharoua/consumer-electronics-sales-dataset/data")
df = pd.read_csv("./dataset/consumer_electronics_sales_data.csv")

def ratakepuasan():
    st.subheader("🧾 Data Awal")
    st.dataframe(df.head())
    # Cek kolom yang dibutuhkan
    if 'ProductCategory' in df.columns and 'CustomerSatisfaction' in df.columns:
        # Hitung rata-rata kepuasan per kategori
        avg_satisfaction = df.groupby('ProductCategory')['CustomerSatisfaction'].mean().reset_index()
        avg_satisfaction['CustomerSatisfaction'] = np.ceil(avg_satisfaction['CustomerSatisfaction'])
        avg_satisfaction = avg_satisfaction.sort_values(by='CustomerSatisfaction', ascending=False)
        st.subheader("📈 Rata-Rata Kepuasan Pelanggan per Kategori Produk")
        fig = px.bar(
            avg_satisfaction,
            x='ProductCategory',
            y='CustomerSatisfaction',
            color='CustomerSatisfaction',
            color_continuous_scale='Blues',
            labels={'CustomerSatisfaction': 'Rata-Rata Kepuasan'},
            title='Rata-Rata Tingkat Kepuasan Pelanggan Berdasarkan Kategori Produk'
        )
        fig.update_layout(xaxis_title="Kategori Produk", yaxis_title="Rata-Rata Kepuasan (1-5)")
        st.plotly_chart(fig, use_container_width=True)

ratakepuasan()
col1, col2 = st.columns(2)

with col1:
    if 'ProductBrand' in df.columns and 'CustomerSatisfaction' in df.columns:
        st.subheader("⭐ Top 5 Brand dengan Total Kepuasan Tertinggi")
        # Hitung Total satisfaction per brand
        top_brands = df.groupby('ProductBrand')['CustomerSatisfaction'].sum().reset_index()
        top_brands = top_brands.sort_values(by='CustomerSatisfaction', ascending=False).head(5)
        fig = px.bar(
            top_brands,
            x='ProductBrand',
            y='CustomerSatisfaction',
            title='Top 5 Brand dengan Total Kepuasan Pelanggan Tertinggi',
            labels={'CustomerSatisfaction': 'Total Kepuasan', 'ProductBrand': 'Brand'},
            color='CustomerSatisfaction',
            color_continuous_scale='Tealgrn'
        )
        fig.update_layout(xaxis_title="Brand", yaxis_title="Rata-Rata Kepuasan (1–5)")
        st.plotly_chart(fig, use_container_width=True)
with col2:
    if 'ProductBrand' in df.columns and 'PurchaseIntent' in df.columns:
        st.subheader("⭐ Top 5 Brand dengan Purchase Intent Tertinggi")
        # Hitung jumlah PurchaseIntent = 1 per brand
        top_purchased = df[df['PurchaseIntent'] == 1] \
            .groupby('ProductBrand') \
            .size() \
            .reset_index(name='TotalIntent')
        # Ambil 5 teratas
        top_purchased = top_purchased.sort_values(by='TotalIntent', ascending=False).head(5)
        # Visualisasi
        fig = px.bar(
            top_purchased,
            x='ProductBrand',
            y='TotalIntent',
            title='Top 5 Brand yang Paling Sering Dibeli Berdasarkan Purchase Intent',
            labels={'ProductBrand': 'Brand Produk', 'TotalIntent': 'Jumlah Purchase Intent (1)'},
            color='TotalIntent',
            color_continuous_scale='YlGnBu'
        )
        st.plotly_chart(fig, use_container_width=True)

if 'CustomerAge' in df.columns and 'CustomerGender' in df.columns and 'PurchaseFrequency' in df.columns:
    st.subheader("📊 Grafik Stacked Bar: Frekuensi Pembelian Berdasarkan Usia dan Gender")
    # Buat rentang usia
    bins = [0, 20, 30, 40, 50, 60, 100]
    labels = ['<21', '21-30', '31-40', '41-50', '51-60', '60+']
    df['AgeGroup'] = pd.cut(df['CustomerAge'], bins=bins, labels=labels, right=False)
    # Mapping gender ke label
    df['Gender'] = df['CustomerGender'].map({0: 'Male', 1: 'Female'})
    # Grouping data
    grouped = df.groupby(['AgeGroup', 'Gender'])['PurchaseFrequency'].sum().reset_index()
    # Plot stacked bar
    fig = px.bar(
        grouped,
        x='AgeGroup',
        y='PurchaseFrequency',
        color='Gender',
        title='Total Frekuensi Pembelian Berdasarkan Rentang Usia dan Jenis Kelamin',
        labels={'AgeGroup': 'Rentang Usia', 'PurchaseFrequency': 'Frekuensi Pembelian'},
        barmode='stack'
    )
    fig.update_layout(xaxis_title="Rentang Usia", yaxis_title="Total Frekuensi Pembelian")
    st.plotly_chart(fig, use_container_width=True)