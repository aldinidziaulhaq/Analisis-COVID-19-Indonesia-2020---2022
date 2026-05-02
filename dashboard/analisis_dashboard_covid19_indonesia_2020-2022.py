import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Konfigurasi Halaman ──
st.set_page_config(
    page_title='Analisis COVID-19 Indonesia 2020-2022',
    page_icon='🦠',
    layout='wide'
)

# ── Load Data ──
@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), 'covid_indonesia_clean.csv')
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
nasional = df[df['location'] == 'Indonesia']
provinsi = df[df['location_level'] == 'Province']
latest   = provinsi.sort_values('date').groupby('location').last().reset_index()

# ── Judul ──
st.title('🦠 Analisis COVID-19 Indonesia 2020-2022')
st.markdown('Sumber data: COVID-19 Indonesia Time Series Dataset — Kaggle')
st.divider()

# ── Kartu Ringkasan ──
st.subheader('📊 Ringkasan Nasional')

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label='Total Kasus',
    value=f"{nasional['total_cases'].max():,}"
)
col2.metric(
    label='Total Kematian',
    value=f"{nasional['total_deaths'].max():,}"
)
col3.metric(
    label='Total Sembuh',
    value=f"{nasional['total_recovered'].max():,}"
)
col4.metric(
    label='Puncak Kasus Harian',
    value=f"{nasional['new_cases'].max():,}"
)

st.divider()

# ── Tren Kasus & Kematian Harian ──
st.subheader('📈 Tren Harian Nasional')

col_kiri, col_kanan = st.columns(2)

with col_kiri:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(nasional['date'], nasional['new_cases'], color='steelblue')
    ax.set_title('Kasus Baru Harian — Indonesia')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Kasus Baru')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col_kanan:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(nasional['date'], nasional['new_deaths'], color='crimson')
    ax2.set_title('Kematian Baru Harian — Indonesia')
    ax2.set_xlabel('Tanggal')
    ax2.set_ylabel('Kematian Baru')
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# ── 5 Provinsi Kasus Tertinggi ──
st.subheader('🗺️ 5 Provinsi Kasus Tertinggi')

top5 = latest.nlargest(5, 'total_cases')[['location', 'total_cases']]

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.barh(top5['location'], top5['total_cases'], color='steelblue')
ax3.set_title('5 Provinsi Kasus Tertinggi')
ax3.set_xlabel('Total Kasus')
ax3.set_ylabel('Provinsi')
plt.tight_layout()
st.pyplot(fig3)

st.divider()

# ── Tabel Data Provinsi ──
st.subheader('📋 Tabel Data Provinsi')

tabel = latest[['location', 'total_cases', 'total_deaths', 'total_recovered']].sort_values(
    'total_cases', ascending=False
).reset_index(drop=True)

tabel.columns = ['Provinsi', 'Total Kasus', 'Total Kematian', 'Total Sembuh']

st.dataframe(tabel, use_container_width=True)

# ── Footer ──
st.divider()
st.caption('📌 Dashboard dibuat menggunakan Python & Streamlit')