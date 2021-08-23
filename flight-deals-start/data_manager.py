import requests

SHEETY_PRICES_ENDPOINT = YOUR_PRICES_SHEETY_ENDPOINT


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_details = {}
        self.get_details()

    def get_details(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.sheet_details = data["prices"]
        return self.sheet_details

    def update_sheet_data(self):
        for city in self.sheet_details:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

