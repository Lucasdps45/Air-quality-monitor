from datetime import datetime
import json
def parse_air_quality_data(data):
    
    all_cities_parsed_data = []
    
    

    for city_name, raw_data in data:
       

        print(json.dumps(raw_data, indent=2))
        aqi = raw_data["list"][0]["main"]["aqi"]
        timestamp = raw_data["list"][0]["dt"]
        readable_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        main_pollutants = {
        "pm2_5": raw_data["list"][0]["components"]["pm2_5"],
        "pm10": raw_data["list"][0]["components"]["pm10"],
        "no2": raw_data["list"][0]["components"]["no2"],
        "o3": raw_data["list"][0]["components"]["o3"],
        "co": raw_data["list"][0]["components"]["co"],
        "so2": raw_data["list"][0]["components"]["so2"]
    }
        
        parsed_data = {
        "city_name": city_name, 
        "measured_at": readable_time,
        "aqi": aqi,
        "pollutants": main_pollutants
        }
        all_cities_parsed_data.append(parsed_data)


    return all_cities_parsed_data
