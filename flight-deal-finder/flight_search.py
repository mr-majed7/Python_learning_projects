import requests
import os
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv()
class FlightSearch:
    def __init__(self):
        self.location_endpoint = f"{os.getenv('TEQUILA_ENDPOINT')}/locations/query"
        self.headers = {"apikey": os.getenv("TEQUILA_API_KEY")}
    def get_destination_code(self,city):
        query = {"term": city, "location_types": "city"}
        response = requests.get(url=self.location_endpoint, headers=self.headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code
    
    def search_flight(self,origin,to,from_time,to_time):
        query={
            "fly_from": origin,
            "fly_to": to,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(
            url=f"https://api.tequila.kiwi.com/v2/search",
            headers=self.headers,
            params=query,
        )
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {to}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data