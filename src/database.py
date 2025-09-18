import os
import psycopg2

database_url = os.environ.get("DATABASE_URL")

conn = psycopg2.connect(database_url)
cur = conn.cursor()

def insert_in_database(data):
    for city_data in data:
        city_name = city_data["city_name"]
        measured_time = city_data["measured_at"]
        aqi_value = city_data["aqi"]
        pollutants_dict = city_data["pollutants"]

        data_source = {
        "city" : city_name,
        "measured_at" : measured_time,
        "aqi" : aqi_value,
        "pm25": pollutants_dict["pm2_5"],
        "pm10": pollutants_dict["pm10"],
        "no2": pollutants_dict["no2"],
        "o3" : pollutants_dict["o3"],
        "co" : pollutants_dict["co"],
        "so2" : pollutants_dict["so2"]
    }

        collumns  = ["city", "measured_at", "aqi", "pm25", "pm10", "no2", "o3", "co", "so2"]

        values_to_insert = [data_source[collum_name] for collum_name in collumns]

        placeholders = ', '.join(['%s' for _ in collumns])
        query = f"INSERT INTO air_quality_data ({', '.join(collumns)}) VALUES ({placeholders})"

        cur.execute(query, values_to_insert)
    
conn.commit()
conn.close()