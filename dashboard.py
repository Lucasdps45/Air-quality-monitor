import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_data():
    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    df = pd.read_sql_query("SELECT * FROM air_quality_data", conn)
    conn.close()
    return df

# Config
st.set_page_config(page_title="Dashboard de Qualidade do Ar", layout="wide")
st.title("🌍 Dashboard de Qualidade do Ar")

# AQI function
def get_aqi_status(aqi_value):
    aqi_map = {
        1: {"label": "Bom", "color": "#00FF00"},
        2: {"label": "Razoável", "color": "#87CEEB"},
        3: {"label": "Moderado", "color": "#FFFF00"},
        4: {"label": "Ruim", "color": "#FFA500"},
        5: {"label": "Muito ruim", "color": "#FF0000"}
    }
    return aqi_map.get(aqi_value, {"label": "N/A", "color": "#808080"})


try:
    DATABASE_URL = st.secrets["DATABASE_URL"]
except KeyError:
    
    from dotenv import load_dotenv
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to DB
@st.cache_resource
def get_db_connection():
    return psycopg2.connect(st.secrets["DATABASE_URL"])

conn = get_db_connection()
df = get_data()
conn.close()

df['measured_at'] = pd.to_datetime(df['measured_at'])

# City selection
CITIES = {
    "São Paulo": (-23.5505, -46.6333),
    "Rio de Janeiro": (-22.9068, -43.1729),
    "Brasília": (-15.7975, -47.8919),
    "Salvador": (-12.9714, -38.5014),
    "Fortaleza": (-3.7172, -38.5433),
    "Belo Horizonte": (-19.9191, -43.9386),
    "Manaus": (-3.1190, -60.0217),
    "Curitiba": (-25.4284, -49.2733),
    "Recife": (-8.0476, -34.8770),
    "Goiânia": (-16.6869, -49.2648),
    "Belém": (-1.4558, -48.4902),
    "Porto Alegre": (-30.0346, -51.2177),
    "Guarulhos": (-23.4544, -46.5333),
    "Campinas": (-22.9056, -47.0608),
    "São Luís": (-2.5307, -44.3068),
    "Maceió": (-9.6658, -35.7350),
    "João Pessoa": (-7.1195, -34.8450),
    "Natal": (-5.7793, -35.2009),
    "Teresina": (-5.0892, -42.8016),
    "Campo Grande": (-20.4697, -54.6201),
    "Cuiabá": (-15.6010, -56.0979),
    "Aracaju": (-10.9091, -37.0678),
    "Florianópolis": (-27.5954, -48.5480),
    "Porto Velho": (-8.7612, -63.9004),
    "Boa Vista": (2.8235, -60.6758),
    "Rio Branco": (-9.9747, -67.8100),
    "Vitória": (-20.3155, -40.3128),
    "Macapá": (0.0340, -51.0695),
    "Palmas": (-10.1844, -48.3336)
}

selected_city = st.sidebar.selectbox(
    "Select city:",
    options=list(CITIES.keys()),
    index=0
)

# Filter data
city_data = df[df['city'] == selected_city]

if not city_data.empty:
    latest = city_data.iloc[-1]
    aqi_info = get_aqi_status(latest['aqi'])
    
    # TOP ROW: Main AQI card
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background-color: {aqi_info['color']}; 
                    padding: 40px; 
                    border-radius: 15px; 
                    text-align: center;
                    margin: 10px 0;">
            <h1 style="color: white; margin: 0; font-size: 4em;">AQI: {latest['aqi']}</h1>
            <h2 style="color: white; margin: 0;">{aqi_info['label']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # MIDDLE ROW: Pollutants grid
    st.subheader("Pollutants Concentration (µg/m³)")
    cols = st.columns(6)
    
    pollutants = {
        "PM2.5": latest['pm25'],
        "PM10": latest['pm10'],
        "NO2": latest['no2'],
        "O3": latest['o3'],
        "CO": latest['co'],
        "SO2": latest['so2']
    }
    
    for col, (name, value) in zip(cols, pollutants.items()):
        with col:
            st.metric(name, f"{value:.2f}")
    
    # BOTTOM: Evolution chart
    st.subheader("Daily AQI Variation")
    weekly_data = city_data[city_data['measured_at'] >= (datetime.now() - timedelta(days=7))]
    
    if not weekly_data.empty:
        fig = px.line(weekly_data, 
                     x='measured_at', 
                     y='aqi',
                     title=f'AQI Evolution in {selected_city}')
        st.plotly_chart(fig)
    else:
        st.warning("Insufficient data for historical analysis")

else:
    st.warning(f"No data available for {selected_city}")

