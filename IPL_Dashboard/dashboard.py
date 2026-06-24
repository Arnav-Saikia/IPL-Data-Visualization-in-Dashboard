import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load Dataset
# -----------------------------
DS = pd.read_csv(
    r"C:\Users\rishi\OneDrive\Desktop\Matplotlib & Seaborn\IPL_Dataset\IPL.csv",
    low_memory=False
)

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("IPL Data Visualization Dashboard")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

selected_team = st.sidebar.selectbox(
    "Select Team",
    sorted(DS['batting_team'].dropna().unique())
)

selected_season = st.sidebar.selectbox(
    "Select Season",
    sorted(DS['season'].dropna().unique())
)

# Apply Filters
filtered_data = DS[
    (DS['batting_team'] == selected_team) &
    (DS['season'] == selected_season)
]

# -----------------------------
# Metrics
# -----------------------------
st.subheader("Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Records", len(filtered_data))

with col2:
    st.metric(
        "Total Runs",
        int(filtered_data['runs_total'].sum())
    )

with col3:
    st.metric(
        "Total Extras",
        int(filtered_data['runs_extras'].sum())
    )

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_data.head())

# -----------------------------
# Bar Chart
# -----------------------------
st.subheader("Top 10 Batsmen by Runs")

top_batsmen = (
    filtered_data.groupby('batter')['runs_batter']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots(figsize=(10,5))

sns.barplot(
    x=top_batsmen.values,
    y=top_batsmen.index,
    ax=ax1
)

ax1.set_title("Top 10 Run Scorers")

st.pyplot(fig1)

# -----------------------------
# Pie Chart
# -----------------------------
st.subheader("Top 5 Wicket Types")

filtered_data['wicket_kind'] = filtered_data['wicket_kind'].fillna('No Wicket')

wickets = filtered_data['wicket_kind'].value_counts().head(5)

fig2, ax2 = plt.subplots(figsize=(7,7))

ax2.pie(
    wickets,
    labels=wickets.index,
    autopct='%1.1f%%'
)

ax2.set_title("Top 5 Wicket Types")

st.pyplot(fig2)

# -----------------------------
# Line Plot
# -----------------------------
st.subheader("Runs Trend")

runs_per_over = (
    filtered_data.groupby('over')['runs_total']
    .sum()
)

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.plot(
    runs_per_over.index,
    runs_per_over.values,
    marker='o'
)

ax3.set_title("Runs Scored Per Over")
ax3.set_xlabel("Over")
ax3.set_ylabel("Runs")

st.pyplot(fig3)

# -----------------------------
# Histogram
# -----------------------------
st.subheader("Runs Distribution")

fig4, ax4 = plt.subplots(figsize=(10,5))

sns.histplot(
    filtered_data['runs_batter'],
    bins=10,
    kde=True,
    ax=ax4
)

ax4.set_title("Distribution of Batter Runs")

st.pyplot(fig4)

# -----------------------------
# Correlation Heatmap
# -----------------------------
st.subheader("Correlation Heatmap")

numeric_cols = [
    'runs_batter',
    'runs_extras',
    'runs_total'
]

corr_matrix = filtered_data[numeric_cols].corr()

fig5, ax5 = plt.subplots(figsize=(6,4))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap='coolwarm',
    ax=ax5
)

st.pyplot(fig5)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.write("IPL Dashboard created using Streamlit, Pandas, Matplotlib and Seaborn")