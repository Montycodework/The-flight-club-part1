import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_ENPOINT = "https://api.sheety.co/9ce394120eb102f3de248273b474c732/flightDeals/prices"
AUTH_TOKEN = "Basic TW9udHk6TW9udHlAMTk5Mw=="

HEADERS = {
    "Authorization": AUTH_TOKEN
}

class DataManager:
    def __init__(self):
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.prices_endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint = os.environ["SHEETY_USERS_ENDPOINT"]
        self.authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self.prices_endpoint, headers=HEADERS)
        self.destination_data = response.json()["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    'iataCode':city['iataCode']
                }
            }
            response = requests.put(url=f"{self.prices_endpoint}/{city['id']}", json=new_data, headers=HEADERS)
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.users_endpoint)
        data = response.json()
        # See how Sheet data is formatted so that you use the correct column name!
        # pprint(data)
        # Name of spreadsheet 'tab' with the customer emails should be "users".
        self.customer_data = data["users"]
        return self.customer_data
