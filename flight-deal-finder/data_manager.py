import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self):
        self.sheet_url = os.getenv("SHEET_URL")
        self.bearer_headers = {
        "Authorization": os.getenv("BEARER_TOKEN")
        }
        sheety_response = requests.get(self.sheet_url,headers=self.bearer_headers)
        self.sheety_data = sheety_response.json()["prices"]

    def update_destination_code(self,data):
        for city in data:
            new_data = {
                "price":{
                    "iataCode":city["iataCode"]
                }
            }
            response = requests.put(f"{self.sheet_url}/{city['id']}",json=new_data,headers=self.bearer_headers)