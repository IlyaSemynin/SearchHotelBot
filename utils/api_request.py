import requests
import json
import re
from config_data import config


city_url = "https://hotels4.p.rapidapi.com/locations/v3/search"

headers = {
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def destination_id(city):
    pattern = '<[^<]*>'
    querystring = {"q": city, "locale": "en_US", "langid": "1033", "siteid": "300000001"}
    response = requests.get(city_url, headers=headers, params=querystring)

    data = json.loads(response.text)  # десериализация JSON

    with open('find_city', 'w') as find_city:
        json.dump(data, find_city, indent=4)

    possible_cities = {}
    for id_place in data['sr']:
        try:
            possible_cities[id_place['gaiaId']] = {
                "gaiaId": id_place['gaiaId'],
                "regionNames": id_place['regionNames']['fullName']
            }
        except KeyError:
            continue
    return possible_cities

