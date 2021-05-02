import os
from pymongo import MongoClient
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


# Replace <password> with the password for the menghsin user. Replace myFirstDatabase with the name of the database that connections will use by default. Ensure any option params are URL encoded.
class DBWrapper:
    def __init__(self):
        self.client = MongoClient(API_KEY) 
        # 沒給參數就是到 localhost
        self.db = self.client.air

    def insert_data(self, tvoc_tgs, pm25, pm10):
        at = datetime.now(timezone.utc)  # 顯示現在時區
        d = {
            'VOC-TGS': tvoc_tgs, 
            'PM25': pm25,
            'PM10': pm10,
            'at': at,
        }

        self.db.air.insert_one(d)

    def insert_data_minute(self, tvoc_tgs_min, pm25_min, pm10_min):
        at = datetime.now(timezone.utc)  # 顯示現在時區
        d_min = {
            'VOC-TGS': tvoc_tgs_min, 
            'PM25': pm25_min,
            'PM10': pm10_min,
            'at': at,
        }

        self.db.air_minute.insert_one(d_min)