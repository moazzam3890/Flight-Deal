import requests
import datetime as dt
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_KEY = YOUR_TEQUILA_KEY


class FlightSearch:

    def get_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {
            "apikey": TEQUILA_KEY,
        }
        params = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=location_endpoint, params=params, headers=headers)
        code = response.json()["locations"][0]["code"]
        return code

    def search(self, fly_from, fly_to):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {
            "apikey": TEQUILA_KEY,
        }
        params = {
            "fly_from": fly_from,
            "fly_to": fly_to,
            "date_from": self.date(days=1),
            "date_to":  self.date(180),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
        }
        response = requests.get(url=search_endpoint, params=params, headers=headers)
        try:
            data = response.json()["data"][0]
        except IndexError:
            params["max_stopovers"] = 1
            response = requests.get(url=search_endpoint, params=params, headers=headers)
            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f"No flights found for {fly_to}")
                return None
            else:
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["cityCodeFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["cityCodeTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"],
                )
                print(f"{flight_data.destination_city}: £{flight_data.price}")
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["cityCodeFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["cityCodeTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            print(f"{flight_data.destination_city}: £{flight_data.price}")
            return flight_data

    def date(self, days):
        datetime = dt.datetime.now() + dt.timedelta(days=days)
        formatted = datetime.strftime("%d/%m/%Y")
        return formatted

