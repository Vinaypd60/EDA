import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Data Cleaner", layout="wide")

st.title("📊 Smart Data Cleaner & Visualizer")

uploaded_file = st.file_uploader("Upload your dataset (CSV/Excel)", type=["csv","xlsx"])

if uploaded_file:
    # Read file dynamically
    if uploaded_file.name.endswith(".csv"):
        dataset = pd.read_csv(uploaded_file)
    else:
        dataset = pd.read_excel(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(dataset.head())

    # Cleaning pipeline
    for col in dataset.columns:
        if dataset[col].dtype == 'object':
            dataset[col] = dataset[col].astype(str).str.replace(r'\W','',regex=True)
            # Try extracting numbers if mixed
            extracted = dataset[col].str.extract('(\d+)')
            if extracted.notna().sum()[0] > 0:
                dataset[col] = extracted[0]

    # Convert numeric columns
    for col in dataset.columns:
        try:
            dataset[col] = pd.to_numeric(dataset[col])
        except:
            pass

    # Fill missing values
    for col in dataset.columns:
        if dataset[col].dtype in ['int64','float64']:
            dataset[col] = dataset[col].fillna(dataset[col].mean())
        else:
            dataset[col] = dataset[col].fillna(dataset[col].mode()[0])

    st.subheader("✅ Cleaned Data")
    st.dataframe(dataset)

    # KPI cards
    st.subheader("📌 Key Stats")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Rows", dataset.shape[0])
    kpi2.metric("Columns", dataset.shape[1])
    kpi3.metric("Missing Values", dataset.isna().sum().sum())

    # Visualization section
    st.subheader("📈 Visualizations")
    selected_col = st.selectbox("Choose a column to visualize", dataset.columns)

    if dataset[selected_col].dtype in ['int64','float64']:
        fig, ax = plt.subplots()
        sns.histplot(dataset[selected_col], ax=ax)
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        sns.countplot(x=dataset[selected_col], ax=ax)
        st.pyplot(fig)

    # Download button
    st.download_button("Download Cleaned Data", dataset.to_csv(index=False), "cleaned_data.csv")
