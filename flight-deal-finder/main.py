from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

sheet = DataManager()
sheet_data = sheet.sheety_data

for data in sheet_data:
    flight_search = FlightSearch()
    if data["iataCode"] == "":
        data["iataCode"] = flight_search.get_destination_code(data["city"])
sheet.update_destination_code(sheet_data)