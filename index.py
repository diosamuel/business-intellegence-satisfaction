import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
st.title("📊 Customer Demographics vs Purchase Intent")
df = pd.read_csv("./dataset/consumer_electronics_sales_data.csv")
# Gender Mapping
gender_map = {0: "Male", 1: "Female"}
df["CustomerGenderLabel"] = df["CustomerGender"].map(gender_map)
df["PurchaseIntentLabel"] = df["PurchaseIntent"].map({0: "No", 1: "Yes"})
# Bar Chart: Purchase Intent by Gender
st.subheader("📊 Purchase Intent by Gender")
gender_intent = df.groupby("CustomerGenderLabel")["PurchaseIntent"].mean().reset_index()
fig1 = px.bar(gender_intent, x="CustomerGenderLabel", y="PurchaseIntent",
              labels={"CustomerGenderLabel": "Gender", "PurchaseIntent": "Average Purchase Intent"},
              title="Average Purchase Intent by Gender",
              color="CustomerGenderLabel")
st.plotly_chart(fig1, use_container_width=True)
# Boxplot: Age by Purchase Intent
st.subheader("📈 Age Distribution by Purchase Intent")
fig2 = px.box(df, x="PurchaseIntentLabel", y="CustomerAge",
              labels={"PurchaseIntentLabel": "Purchase Intent", "CustomerAge": "Age"},
              title="Customer Age vs Purchase Intent",
              color="PurchaseIntentLabel")
st.plotly_chart(fig2, use_container_width=True)