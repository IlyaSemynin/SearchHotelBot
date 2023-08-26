import json
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot
from states.user_data import UserInfoState
from telebot.types import Message
from telebot import types
from database.history_class import History
from datetime import datetime
from config_data import config
import requests


def city_founding(city):
    global suggestions
    url_search = "https://hotels4.p.rapidapi.com/locations/v2/search"

    querystring_search = {"query": city, "locale": "en_UK", "currency": "USD"}

    response = requests.request("GET", url_search, headers=config.headers, params=querystring_search)
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, response.text)
    if find:
        suggestions = json.loads(f"{{{find[0]}}}")

    cities = list()
    for dest_id in suggestions['entities']:
        clear = r'<.*?>|</.*?>'
        clear_destination = re.sub(clear, '', dest_id['caption'])
        cities.append({'city_name': clear_destination, 'destination_id': dest_id['destinationId']})
    return cities


def city_markup(city):
    cities = city_founding(city)
    destinations = InlineKeyboardMarkup()
    for city in cities:
        exact_location = list()
        exact_location.append(city['city_name'].split(','))
        txt = ''.join(exact_location[0][0:2])
        destinations.add(InlineKeyboardButton(text=txt, callback_data=txt))
    return destinations


def request_to_api(url, headers, querystring):
    try:
        response = requests.request("GET", url, headers=headers, params=querystring, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
    except BaseException:
        print('Ошибка поиска')


gaiaId = list()


def get_regionId(response_search: dict) -> None:
    for d in response_search['sr']:
        if d['@type'] == 'gaiaRegionResult':
            gaiaId.append(d['gaiaId'])


def cleaner(string: str) -> float:
    numbers = ''
    for i in string:
        if i == '.':
            numbers += i
        if i.isdigit():
            numbers += str(i)
    return float(numbers)


def get_address_and_rate_and_photo(hotel_id: str) -> list:
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }

    response = requests.request("POST", url, json=payload, headers=config.headers).json()

    return [response['data']['propertyInfo']['summary']['location']['address']['addressLine'], response['data'][
        'propertyInfo']['summary']['overview']['propertyRating']['rating'], response['data']['propertyInfo'][
        'propertyGallery']['images']]


def get_result_dict(entities_list, result_dict):
    for hotel in entities_list[:8]:
        res_rate_photo: list = get_address_and_rate_and_photo(hotel['id'])
        print('Hotels - ID', hotel['id'])
        result_dict.update({hotel['id']: {'name': hotel['name'], 'adress': res_rate_photo[0],
                                          'star_rating': res_rate_photo[1],
                                          'price': hotel['price']['lead']['formatted'],
                                          'centre': hotel['destinationInfo']['distanceFromDestination']['value'],
                                          'img': res_rate_photo[2]}})


def lowprice(result_dict, count, message, data) -> None:
    history_list = list()
    sort_list = sorted([(hotel, result_dict[hotel]["price"]) for hotel in result_dict], key=lambda x: x[1],
                       reverse=False)
    for hotel_price in sort_list:
        if count > 0:
            id = hotel_price[0]
            name = result_dict[id]['name']
            rating = result_dict[id]["star_rating"]
            adress = result_dict[id]["adress"]
            go_centre = result_dict[id]["centre"]
            price = result_dict[id]['price']
            link = f"https://www.hotels.com/h{id}.Hotel-Information"
            text = f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\nРасстояние до центра: {go_centre}\n" \
                   f"Цена за период: {price}\nСайт: {link}\n"
            history_list.append(f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\n"
                                f"Расстояние до центра: {go_centre}\n"
                                f"Цена за период: {price}\n")
            bot.send_message(message.from_user.id, text)

            try:
                if data['count_photo'] != 'Нет':
                    media = get_photo_link(result_dict[id]['img'], data)
                    bot.send_media_group(message.chat.id, media=media)
            except:
                bot.send_message(message.from_user.id, "Фото найти не удалось...")

            count -= 1
        else:
            lowprice_history = History('bot_history.sqlite', message.from_user.id)
            lowprice_history.fill(message.from_user.id, data["command"], datetime.now(), history_list)
            lowprice_history.close()
            break


def highprice(result_dict, count, message, data) -> None:
    history_list = list()
    sort_list = sorted([(hotel, result_dict[hotel]["price"]) for hotel in result_dict], key=lambda x: x[1],
                       reverse=True)
    for hotel_price in sort_list:
        if count > 0:
            id = hotel_price[0]
            name = result_dict[id]['name']
            rating = result_dict[id]["star_rating"]
            adress = result_dict[id]["adress"]
            go_centre = result_dict[id]["centre"]
            price = result_dict[id]['price']
            link = f"https://www.hotels.com/h{id}.Hotel-Information"
            text = f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\nРасстояние до центра: {go_centre}\n" \
                   f"Цена за период: {price}\nСайт: {link}\n"
            history_list.append(f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\n"
                                f"Расстояние до центра: {go_centre}\n"
                                f"Цена за период: {price}\n")
            bot.send_message(message.from_user.id, text)

            try:
                if data['count_photo'] != 'Нет':
                    media = get_photo_link(result_dict[id]['img'], data)
                    bot.send_media_group(message.chat.id, media=media)
            except:
                bot.send_message(message.from_user.id, "Фото найти не удалось...")

            count -= 1
        else:
            highprice_history = History('bot_history.sqlite', message.from_user.id)
            highprice_history.fill(message.from_user.id, data["command"], datetime.now(), history_list)
            highprice_history.close()
            break


def custom(result_dict, count, message, data) -> None:
    history_list = list()
    sort_price = sorted([(hotel, result_dict[hotel]["price"]) for hotel in result_dict if (
                int(data['price_min']) <= cleaner(result_dict[hotel]['price']) <= int(data['price_max']))],
                        key=lambda x: x[1], reverse=True)
    sort_range = sorted([(hotel[0], result_dict[hotel[0]]["centre"]) for hotel in sort_price if (
                int(data['distance_min']) <= result_dict[hotel[0]]['centre'] <= int(data['distance_max']))],
                        key=lambda x: x[1], reverse=False)

    for hotel in sort_range:
        if count > 0:
            id = hotel[0]
            name = result_dict[id]['name']
            rating = result_dict[id]["star_rating"]
            adress = result_dict[id]["adress"]
            go_centre = result_dict[id]["centre"]
            price = result_dict[id]['price']
            link = f"https://www.hotels.com/h{id}.Hotel-Information"
            text = f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\nРасстояние до центра: {go_centre}\n" \
                   f"Цена за период: {price}\nСайт: {link}"
            history_list.append(f"\nОтель: {name}\nРейтинг: {rating}\nАдрес: {adress}\n"
                                f"Расстояние до центра: {go_centre}\n"
                                f"Цена за период: {price}\n")
            bot.send_message(message.from_user.id, text)
            try:
                if data['count_photo'] != 'Нет':
                    media = get_photo_link(result_dict[id]['img'], data)
                    bot.send_media_group(message.chat.id, media=media)
            except:
                bot.send_message(message.from_user.id, "Фото найти не удалось...")
            count -= 1
        else:
            custom_history = History('bot_history.sqlite', message.from_user.id)
            custom_history.fill(message.from_user.id, data["command"], datetime.now(), history_list)
            custom_history.close()
            break


def get_photo_link(images: list, data) -> list:
    media = list()
    photo_link = [photo['image']['url'] for photo in images]
    count = 0
    for link in photo_link:
        count += 1
        media.append(types.InputMediaPhoto(media=link.replace('{size}', 'z')))
        if count >= int(data['count_photo']):
            return media


def search(message: Message, data) -> None:
    global data_list
    bot.set_state(message.from_user.id, UserInfoState.search, message.chat.id)
    url_search = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": data['city'], "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    response_search = request_to_api(url_search, config.headers, querystring)
    try:
        if response_search.status_code == 200:
            get_regionId(response_search.json())
    except BaseException:
        bot.send_message(message.from_user.id, "Ошибка поиска")

    url_list = "https://hotels4.p.rapidapi.com/properties/v2/list"
    result_dict = dict()

    print(f"Region - ID {gaiaId[0]}")
    payload = {
        "currency": data['currency'],
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": str(gaiaId[0])
        },
        "checkInDate": {
            "day": int(str(data['check_in']).split('-')[2]),
            "month": int(str(data['check_in']).split('-')[1]),
            "year": int(str(data['check_in']).split('-')[0])
        },
        "checkOutDate": {
            "day": int(str(data['check_out']).split('-')[2]),
            "month": int(str(data['check_out']).split('-')[1]),
            "year": int(str(data['check_out']).split('-')[0])
        },
        "rooms": [
            {
                "adults": 1,
                "children": []
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": None,
        "filters": {
            "price": {
                "max": None,
                "min": None
            }
        }
    }

    response_list = requests.request("POST", url_list, json=payload, headers=config.headers)
    try:
        data_list = response_list.json()

    except AttributeError:
        print('error')

    entities_list = data_list["data"]["propertySearch"]["properties"]
    get_result_dict(entities_list, result_dict)

    if data['command'] == '/low':
        lowprice(result_dict, int(data['count']), message, data)

    if data['command'] == '/high':
        highprice(result_dict, int(data['count']), message, data)

    if data['command'] == '/custom':
        custom(result_dict, int(data['count']), message, data)
