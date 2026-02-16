import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Customer Segmentation Dashboard")

st.title("Customer Segmentation Dashboard")

# Load Data
df = pd.read_csv("data/mall_customers.csv")

# Encode categorical column
df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

# Drop unnecessary column
df = df.drop("CustomerID", axis=1)

# Feature Selection
features = df[["Annual Income (k$)", "Spending Score (1-100)"]]

# Scaling
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# KMeans Model
kmeans = KMeans(n_clusters=5, random_state=42)
df["Cluster"] = kmeans.fit_predict(scaled_features)

# Show Raw Data
if st.checkbox("Show Raw Data"):
    st.write(df.head())

# Cluster Summary
st.subheader("Cluster Summary (Mean Values)")
st.write(df.groupby("Cluster").mean(numeric_only=True))

# Visualization
st.subheader("Cluster Visualization")

fig, ax = plt.subplots()
sns.scatterplot(
    x=df["Annual Income (k$)"],
    y=df["Spending Score (1-100)"],
    hue=df["Cluster"],
    palette="Set1",
    ax=ax
)

plt.title("Customer Segments")
st.pyplot(fig)

st.subheader("Business Insights")

st.markdown("""
- Cluster 0: High income, high spending — Premium customers.
- Cluster 1: Low income, low spending — Budget customers.
- Cluster 2: High income, low spending — Conservative spenders.
- Cluster 3: Low income, high spending — Impulsive buyers.
- Cluster 4: Moderate income and spending — Average customers.
""")

st.subheader("Cluster Distribution")

cluster_counts = df["Cluster"].value_counts().sort_index()
st.bar_chart(cluster_counts)
