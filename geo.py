import requests
import math


def getGeoInfo(city, type):
    try:
        url = 'https://geocode-maps.yandex.ru/1.x/'
        params = {
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'geocode': city,
            'format': 'json'
        }
        data = requests.get(url, params).json()
        if type == 'country':
            return data['response']['GeoObjectCollection'][
                'featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['AddressDetails']['Country']['CountryName']
        elif type == 'coordinates':
            coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            return list(map(float, coords.split()))
    except Exception as e:
        return e


def getDistance(point1, point2):
    radius = 6373.0
    lon1 = math.radians(point1[0])
    lat1 = math.radians(point1[1])
    lon2 = math.radians(point2[0])
    lat2 = math.radians(point2[1])
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
    distance = radius * c
    return distance
