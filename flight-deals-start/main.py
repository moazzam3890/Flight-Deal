from data_manager import DataManager
from datetime import timedelta, datetime
from flight_search import FlightSearch
from notification_manager import NotificationManager

DEPARTURE_CITY_IATA = "LON"

data_manager = DataManager()
sheet_data = data_manager.get_details()
flight_search = FlightSearch()
notification_manager = NotificationManager()


for id_ in range(9):
    if sheet_data[id_]["iataCode"] == "":
        import flight_search
        flight_search = flight_search.FlightSearch()
        for row in sheet_data:
            row["iataCode"] = flight_search.get_code(row["city"])
        print(f"Sheet Data: {sheet_data}")

        data_manager.sheet_details = sheet_data
        data_manager.update_sheet_data()

tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=6*30)

for destination in sheet_data:
    flight = flight_search.search(
        DEPARTURE_CITY_IATA,
        destination["iataCode"]
    )
    try:
        if flight.price < destination["lowestPrice"]:
            link = f"https://www.google.co.uk/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"
            message = f"Low Price Alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport} from {flight.out_date} to {flight.return_date}."
            additional_message = f"Flight has {flight.stop_overs} stop overs, via {flight.via_city}."
            if flight.stop_overs > 0:
                notification_manager.notification(
                    message=message + f"Flight has {flight.stop_overs} stop overs, via {flight.via_city}.",
                )
                notification_manager.send_email(
                    message=message.encode("utf-8") + additional_message.encode("utf-8"),
                    link=link,
                )
            notification_manager.notification(
                message=message,
            )
            notification_manager.send_email(
                message=message.encode("utf-8"),
                link=link,
            )
    except AttributeError:
        continue

