from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

sheet = DataManager()
sheet_data = sheet.sheety_data
flight_search = FlightSearch()
notification_manager = NotificationManager()
ORIGIN_CITY_IATA = "LON"

for data in sheet_data:
    flight_search = FlightSearch()
    if data["iataCode"] == "":
        data["iataCode"] = flight_search.get_destination_code(data["city"])
sheet.update_destination_code(sheet_data)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


for destination in sheet_data:
    flight = flight_search.search_flight(ORIGIN_CITY_IATA,destination["iataCode"],tomorrow,six_month_from_today)
    if flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message=f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
        )
