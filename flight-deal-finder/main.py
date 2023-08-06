from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta

sheet = DataManager()
sheet_data = sheet.sheety_data
flight_search = FlightSearch()
ORIGIN_CITY_IATA = "LON"

# for data in sheet_data:
#     flight_search = FlightSearch()
#     if data["iataCode"] == "":
#         data["iataCode"] = flight_search.get_destination_code(data["city"])
# sheet.update_destination_code(sheet_data)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


for destination in sheet_data:
    flight = flight_search.search_flight(ORIGIN_CITY_IATA,destination["iataCode"],tomorrow,six_month_from_today)
