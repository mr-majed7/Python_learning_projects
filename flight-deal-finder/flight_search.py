import requests
import os
from dotenv import load_dotenv

load_dotenv()
class FlightSearch:
    def get_destination_code(self,city):
        location_endpoint = f"{os.getenv('TEQUILA_ENDPOINT')}/locations/query"
        headers = {"apikey": os.getenv("TEQUILA_API_KEY")}
        query = {"term": city, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code