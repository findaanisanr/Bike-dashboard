import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

st.set_page_config(page_title="Bike Sharing Dashboard Finda Nur Anisa", layout="wide")

@st.cache_data
def load_data():
    df_hour = pd.read_csv("dashboard/df_hour_clean.csv")
    df_day = pd.read_csv("dashboard/df_day_clean.csv")

    df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
    df_day["dteday"] = pd.to_datetime(df_day["dteday"])

    return df_hour, df_day

df_hour, df_day = load_data()

with st.sidebar:
    st.title("🚲 Bike Dashboard")
    st.markdown("Analisis penyewaan sepeda")

    
    min_date = df_hour["dteday"].min()
    max_date = df_hour["dteday"].max()

    start_date, end_date = st.date_input(
        "Filter Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    season = st.multiselect(
        "Pilih Season",
        options=sorted(df_hour["season"].unique()),
        default=sorted(df_hour["season"].unique())
    )

    weather = st.multiselect(
        "Pilih Cuaca",
        options=sorted(df_hour["weathersit"].unique()),
        default=sorted(df_hour["weathersit"].unique())
    )

df_filtered = df_hour[
    (df_hour["dteday"] >= pd.to_datetime(start_date)) &
    (df_hour["dteday"] <= pd.to_datetime(end_date)) &
    (df_hour["season"].isin(season)) &
    (df_hour["weathersit"].isin(weather))
]

def format_axis(ax):
    ticks = ax.get_yticks()
    if max(ticks) >= 1000:
        ax.set_yticklabels([f'{int(x/1000)}K' for x in ticks])
    else:
        ax.set_yticklabels([f'{int(x)}' for x in ticks])

st.title("🚲 Bike Sharing Dashboard")
st.caption(f"Data dari {start_date} sampai {end_date}")

col1, col2, col3 = st.columns(3)

col1.metric("Total Data", len(df_filtered))
col2.metric("Rata-rata / Jam", int(df_filtered["cnt"].mean()))
col3.metric("Maksimum", int(df_filtered["cnt"].max()))

st.subheader("📊 Total Penyewaan per Tahun")

df_filtered["year"] = df_filtered["dteday"].dt.year
df_year = df_filtered.groupby("year")["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(4,2))
sns.barplot(data=df_year, x="year", y="cnt", color="#4CAF50", ax=ax)


format_axis(ax)
st.pyplot(fig, use_container_width=False)

st.subheader("🌦️ Pengaruh Cuaca")

df_weather = df_filtered.groupby("weathersit")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(5,3))
sns.barplot(data=df_weather, x="weathersit", y="cnt", color="#2196F3", ax=ax)

ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

format_axis(ax)
st.pyplot(fig, use_container_width=False)

st.subheader("⏰ Pola Penyewaan per Jam")

df_hourly = df_filtered.groupby("hr")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(5,3))
sns.lineplot(data=df_hourly, x="hr", y="cnt", color="#2196F3", ax=ax)


format_axis(ax)
st.pyplot(fig, use_container_width=False)

st.subheader("📅 Weekday vs Weekend")

df_daytype = df_filtered.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
df_daytype["day_type"] = df_daytype["workingday"].map({
    0: "Weekend",
    1: "Weekday"
})

ax.set_xticklabels(ax.get_xticklabels(), rotation=30)

fig, ax = plt.subplots(figsize=(5,3))
sns.lineplot(
    data=df_daytype,
    x="hr",
    y="cnt",
    hue="day_type",
    palette={"Weekend": "#FF5722", "Weekday": "#2196F3"},
    ax=ax
)


format_axis(ax)
st.pyplot(fig, use_container_width=False)

st.subheader("🌡️ Korelasi Faktor Lingkungan")

corr = df_day[["temp", "hum", "windspeed", "cnt"]].corr()["cnt"].drop("cnt")

fig, ax = plt.subplots(figsize=(5,3))
corr.plot(kind="bar", color="#4CAF50", ax=ax)

st.pyplot(fig, use_container_width=False)

st.caption("Dashboard by Finda Nur Anisa")