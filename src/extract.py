import requests
from config.settings import api_key
cities = {
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

def get_air_quality_data():
    
    all_city_datas = []
    
    for city_name, coordinates in cities.items():
        lat, lon = coordinates
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        
        
        response = requests.get(url)
        city_data = response.json()
        all_city_datas.append((city_name, city_data))
        
    return all_city_datas

get_air_quality_data()


