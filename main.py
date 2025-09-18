from src.extract import get_air_quality_data
from src.parses import parse_air_quality_data
from src.database import insert_in_database

def main():
    print("Iniciando pipeline ETL")

    raw_data = get_air_quality_data()

    parsed_data = parse_air_quality_data(raw_data)

    insert_in_database(parsed_data)

    print("Fim do pipeline")

if __name__ == "__main__":
    main()