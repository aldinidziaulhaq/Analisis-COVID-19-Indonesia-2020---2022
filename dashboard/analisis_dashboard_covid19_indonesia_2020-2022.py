import os
import base64
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ── Konfigurasi Halaman ──
st.set_page_config(
    page_title='Analisis COVID-19 Indonesia 2020-2022',
    layout='wide'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Palet warna (diambil dari gambar virus) ──
NAVY = '#06192b'
DEEP = '#0a2a45'
PANEL = '#0d3354'
BLUE = '#1c6ea4'
CYAN = '#5fd0f0'
ICE = '#d8f1fb'
MUTED = '#8fb4cc'
CORAL = '#ff7a7a'


# ── Load Data ──
@st.cache_data
def load_data():
    path = os.path.join(BASE_DIR, 'covid_indonesia_clean.csv')
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df


@st.cache_data
def load_banner():
    path = os.path.join(BASE_DIR, 'covid19.jpg')
    if not os.path.exists(path):
        return ''
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def fmt(x):
    """Format angka gaya Indonesia: 1.234.567"""
    return f"{int(x):,}".replace(',', '.')


df = load_data()
banner_b64 = load_banner()

nasional = df[df['location'] == 'Indonesia']
provinsi = df[df['location_level'] == 'Province']
latest = provinsi.sort_values('date').groupby('location').last().reset_index()

# ── CSS ──
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Inter', sans-serif;
    color: {ICE};
}}
.stApp {{
    background:
        radial-gradient(1200px 600px at 85% -10%, rgba(28,110,164,0.35), transparent 60%),
        linear-gradient(180deg, {NAVY} 0%, {DEEP} 100%);
}}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}
.block-container {{ padding-top: 1.5rem; max-width: 1280px; }}

/* Hero */
.hero {{
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    min-height: 320px;
    display: flex;
    align-items: flex-end;
    background-color: {DEEP};
    background-image:
        linear-gradient(90deg, rgba(6,25,43,0.92) 0%, rgba(6,25,43,0.55) 55%, rgba(6,25,43,0.15) 100%),
        url("data:image/jpeg;base64,{banner_b64}");
    background-size: cover;
    background-position: center;
    border: 1px solid rgba(95,208,240,0.25);
}}
.hero-inner {{ padding: 2.6rem 2.8rem; max-width: 720px; }}
.hero h1 {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 2.7rem;
    line-height: 1.12;
    color: #ffffff;
    margin: 0 0 0.8rem 0;
    padding: 0;
}}
.hero p {{
    font-size: 1.02rem;
    color: {ICE};
    margin: 0 0 0.35rem 0;
    line-height: 1.55;
}}
.hero a {{ color: {CYAN}; text-decoration: none; border-bottom: 1px solid rgba(95,208,240,0.5); }}
.hero a:hover {{ color: #ffffff; border-bottom-color: #ffffff; }}

/* Judul seksi */
.sec-title {{
    font-family: 'Sora', sans-serif;
    font-weight: 600;
    font-size: 1.35rem;
    color: #ffffff;
    margin: 2.4rem 0 1rem 0;
    padding-left: 0.9rem;
    border-left: 4px solid {CYAN};
}}

/* Kartu ringkasan */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}}
.kpi {{
    background: linear-gradient(160deg, {PANEL} 0%, {DEEP} 100%);
    border: 1px solid rgba(95,208,240,0.2);
    border-radius: 16px;
    padding: 1.3rem 1.4rem;
}}
.kpi .label {{ font-size: 0.88rem; color: {MUTED}; margin-bottom: 0.5rem; }}
.kpi .value {{
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 1.9rem;
    color: #ffffff;
    line-height: 1.1;
}}
.kpi.cases {{ border-top: 4px solid {CYAN}; }}
.kpi.deaths {{ border-top: 4px solid {CORAL}; }}
.kpi.recovered {{ border-top: 4px solid #6fe0a8; }}
.kpi.peak {{ border-top: 4px solid {BLUE}; }}

/* Tabel */
.table-wrap {{
    max-height: 520px;
    overflow: auto;
    border-radius: 14px;
    border: 1px solid rgba(95,208,240,0.2);
    background: {DEEP};
}}
table.data {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.93rem;
}}
table.data thead th {{
    position: sticky;
    top: 0;
    background: {BLUE};
    color: #ffffff;
    text-align: left;
    padding: 0.8rem 1rem;
    font-weight: 600;
}}
table.data th.num, table.data td.num {{ text-align: right; }}
table.data td {{
    padding: 0.65rem 1rem;
    border-bottom: 1px solid rgba(95,208,240,0.1);
    color: {ICE};
}}
table.data tbody tr:nth-child(even) td {{ background: rgba(13,51,84,0.55); }}
table.data tbody tr:hover td {{ background: rgba(95,208,240,0.12); }}

/* Footer */
.foot {{
    margin-top: 2.6rem;
    padding-top: 1.1rem;
    border-top: 1px solid rgba(95,208,240,0.2);
    color: {MUTED};
    font-size: 0.88rem;
    text-align: center;
}}

@media (max-width: 900px) {{
    .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .hero h1 {{ font-size: 2rem; }}
    .hero-inner {{ padding: 1.8rem 1.4rem; }}
}}
@media (max-width: 520px) {{
    .kpi-grid {{ grid-template-columns: 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Gaya grafik matplotlib agar serasi dengan tema ──
plt.rcParams.update({
    'figure.facecolor': DEEP,
    'axes.facecolor': DEEP,
    'savefig.facecolor': DEEP,
    'axes.edgecolor': BLUE,
    'axes.labelcolor': ICE,
    'axes.titlecolor': '#ffffff',
    'axes.titleweight': 'bold',
    'axes.titlesize': 13,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'grid.color': BLUE,
    'grid.alpha': 0.25,
    'text.color': ICE,
})


def rapikan(ax):
    ax.grid(True, axis='y')
    ax.set_axisbelow(True)
    for sisi in ('top', 'right'):
        ax.spines[sisi].set_visible(False)


# ── Hero ──
st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <h1>Analisis COVID-19 Indonesia 2020-2022</h1>
    <p>Sumber data: COVID-19 Indonesia Time Series Dataset, Kaggle</p>
    <p>Author: <a href="https://github.com/aldinidziaulhaq" target="_blank">github.com/aldinidziaulhaq</a></p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Kartu Ringkasan ──
st.markdown('<div class="sec-title">Ringkasan Nasional</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi cases">
    <div class="label">Total Kasus</div>
    <div class="value">{fmt(nasional['total_cases'].max())}</div>
  </div>
  <div class="kpi deaths">
    <div class="label">Total Kematian</div>
    <div class="value">{fmt(nasional['total_deaths'].max())}</div>
  </div>
  <div class="kpi recovered">
    <div class="label">Total Sembuh</div>
    <div class="value">{fmt(nasional['total_recovered'].max())}</div>
  </div>
  <div class="kpi peak">
    <div class="label">Puncak Kasus Harian</div>
    <div class="value">{fmt(nasional['new_cases'].max())}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tren Kasus & Kematian Harian ──
st.markdown('<div class="sec-title">Tren Harian Nasional</div>', unsafe_allow_html=True)

col_kiri, col_kanan = st.columns(2)

with col_kiri:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(nasional['date'], nasional['new_cases'], color=CYAN, linewidth=1.8)
    ax.fill_between(nasional['date'], nasional['new_cases'], color=CYAN, alpha=0.15)
    ax.set_title('Kasus Baru Harian — Indonesia')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Kasus Baru')
    ax.tick_params(axis='x', rotation=45)
    rapikan(ax)
    plt.tight_layout()
    st.pyplot(fig)

with col_kanan:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(nasional['date'], nasional['new_deaths'], color=CORAL, linewidth=1.8)
    ax2.fill_between(nasional['date'], nasional['new_deaths'], color=CORAL, alpha=0.15)
    ax2.set_title('Kematian Baru Harian — Indonesia')
    ax2.set_xlabel('Tanggal')
    ax2.set_ylabel('Kematian Baru')
    ax2.tick_params(axis='x', rotation=45)
    rapikan(ax2)
    plt.tight_layout()
    st.pyplot(fig2)

# ── 5 Provinsi Kasus Tertinggi ──
st.markdown('<div class="sec-title">5 Provinsi Kasus Tertinggi</div>', unsafe_allow_html=True)

top5 = latest.nlargest(5, 'total_cases')[['location', 'total_cases']]

fig3, ax3 = plt.subplots(figsize=(8, 4))
ax3.barh(top5['location'], top5['total_cases'], color=CYAN, height=0.6)
ax3.invert_yaxis()
ax3.set_title('5 Provinsi Kasus Tertinggi')
ax3.set_xlabel('Total Kasus')
ax3.set_ylabel('Provinsi')
ax3.grid(True, axis='x')
ax3.set_axisbelow(True)
for sisi in ('top', 'right'):
    ax3.spines[sisi].set_visible(False)
plt.tight_layout()

_, tengah, _ = st.columns([1, 3, 1])
with tengah:
    st.pyplot(fig3)

# ── Tabel Data Provinsi ──
st.markdown('<div class="sec-title">Tabel Data Provinsi</div>', unsafe_allow_html=True)

tabel = latest[['location', 'total_cases', 'total_deaths', 'total_recovered']].sort_values(
    'total_cases', ascending=False
).reset_index(drop=True)

baris = ''
for _, r in tabel.iterrows():
    baris += (
        f"<tr><td>{r['location']}</td>"
        f"<td class='num'>{fmt(r['total_cases'])}</td>"
        f"<td class='num'>{fmt(r['total_deaths'])}</td>"
        f"<td class='num'>{fmt(r['total_recovered'])}</td></tr>"
    )

st.markdown(f"""
<div class="table-wrap">
  <table class="data">
    <thead>
      <tr>
        <th>Provinsi</th>
        <th class="num">Total Kasus</th>
        <th class="num">Total Kematian</th>
        <th class="num">Total Sembuh</th>
      </tr>
    </thead>
    <tbody>{baris}</tbody>
  </table>
</div>
""", unsafe_allow_html=True)

# ── Footer ──
st.markdown(
    '<div class="foot">Dashboard dibuat menggunakan Python dan Streamlit</div>',
    unsafe_allow_html=True
)