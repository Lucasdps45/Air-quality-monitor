import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
data_base_url = os.getenv("DATA_BASE_URL")

print(data_base_url)
