import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

@st.cache_data
def load_data(file_path):
    """Membaca data dari file CSV dan memproses kolom tambahan."""
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['hour'] = df['hr']
    df['day'] = df['dteday'].dt.day_name()
    return df

def plot_bar(data, x, y, title, xlabel, ylabel, order=None):
    """Fungsi untuk membuat bar plot."""
    fig, ax = plt.subplots()
    sns.barplot(data=data, x=x, y=y, order=order, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_line(data, x, y, title, xlabel, ylabel):
    """Fungsi untuk membuat line plot."""
    fig, ax = plt.subplots()
    sns.lineplot(data=data, x=x, y=y, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    st.pyplot(fig)

def plot_correlation_heatmap(data, title):
    """Fungsi untuk membuat heatmap korelasi."""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)

# Load dataset
file_path = 'all_data.csv'  
df = load_data(file_path)

# Sidebar untuk filter
st.sidebar.header("Pengaturan Dashboard")
selected_analysis = st.sidebar.selectbox(
    "Pilih Analisis",
    [
        "Pola Penggunaan Sepeda Berdasarkan Waktu",
        "Perbedaan Hari Kerja dan Akhir Pekan, atau Musim",
        "Faktor yang Mempengaruhi Jumlah Penggunaan Sepeda",
        "Distribusi dan Outlier",
    ]
)

# Filter tambahan
selected_season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=df['season'].unique(),
    default=df['season'].unique()
)
selected_day_type = st.sidebar.multiselect(
    "Pilih Tipe Hari (Kerja/Akhir Pekan):",
    options=df['is_weekend'].unique(),
    default=df['is_weekend'].unique()
)

# Filter data berdasarkan pilihan
filtered_df = df[df['season'].isin(selected_season) & df['is_weekend'].isin(selected_day_type)]

# Analisis berdasarkan pilihan pengguna
if selected_analysis == "Pola Penggunaan Sepeda Berdasarkan Waktu":
    st.title("Pola Penggunaan Sepeda Berdasarkan Waktu")
    
    # Penggunaan berdasarkan jam
    st.subheader("Penggunaan Sepeda per Jam")
    hour_usage = filtered_df.groupby('hour')['hour_count'].mean().reset_index()
    plot_line(hour_usage, 'hour', 'hour_count', 
              "Rata-rata Penggunaan Sepeda per Jam", "Jam", "Jumlah Penggunaan")
    
    # Penggunaan berdasarkan hari
    st.subheader("Penggunaan Sepeda per Hari")
    day_usage = filtered_df.groupby('day')['hour_count'].mean().reset_index()
    plot_bar(day_usage, 'day', 'hour_count', 
             "Rata-rata Penggunaan Sepeda per Hari", "Hari", "Jumlah Penggunaan", 
             order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

elif selected_analysis == "Perbedaan Hari Kerja dan Akhir Pekan, atau Musim":
    st.title("Perbedaan Hari Kerja dan Akhir Pekan, atau Musim")
    
    # Perbedaan antara hari kerja dan akhir pekan
    st.subheader("Perbedaan Penggunaan Sepeda: Hari Kerja vs Akhir Pekan")
    weekend_usage = filtered_df.groupby('is_weekend')['hour_count'].mean().reset_index()
    plot_bar(weekend_usage, 'is_weekend', 'hour_count', 
             "Penggunaan Sepeda: Hari Kerja vs Akhir Pekan", "Tipe Hari", "Jumlah Penggunaan")
    
    # Perbedaan antara musim
    st.subheader("Perbedaan Penggunaan Sepeda Berdasarkan Musim")
    season_usage = filtered_df.groupby('season')['hour_count'].mean().reset_index()
    plot_bar(season_usage, 'season', 'hour_count', 
             "Penggunaan Sepeda Berdasarkan Musim", "Musim", "Jumlah Penggunaan")

elif selected_analysis == "Faktor yang Mempengaruhi Jumlah Penggunaan Sepeda":
    st.title("Faktor yang Mempengaruhi Jumlah Penggunaan Sepeda")
    
    # Korelasi antara jumlah penggunaan dan faktor cuaca
    st.subheader("Korelasi antara Faktor Cuaca dan Penggunaan Sepeda")
    plot_correlation_heatmap(filtered_df[['hour_count', 'temp', 'hum', 'windspeed']], 
                             "Korelasi Faktor Cuaca dengan Penggunaan Sepeda")
    
    # Scatter plot penggunaan vs suhu
    st.subheader("Pengaruh Suhu terhadap Penggunaan Sepeda")
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x='temp', y='hour_count', ax=ax)
    ax.set_title("Penggunaan Sepeda vs Suhu")
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Jumlah Penggunaan")
    st.pyplot(fig)

elif selected_analysis == "Distribusi dan Outlier":
    st.title("Distribusi dan Outlier")
    
    # Histogram untuk distribusi jumlah penggunaan sepeda
    st.subheader("Distribusi Jumlah Penggunaan Sepeda")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['hour_count'], kde=True, ax=ax, bins=30)
    ax.set_title("Distribusi Jumlah Penggunaan Sepeda")
    ax.set_xlabel("Jumlah Penggunaan")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig)
    
    # Boxplot untuk outlier analisis
    st.subheader("Analisis Outlier pada Jumlah Penggunaan Sepeda")
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, x='hour_count', ax=ax)
    ax.set_title("Outlier pada Jumlah Penggunaan Sepeda")
    st.pyplot(fig)
