from flask import Flask, request
from geo import getGeoInfo, getDistance
import logging
import json


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {'session': request.json['session'],
                'version': request.json['version'],
                'response': {'end_session': False}}
    handleDialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handleDialog(res, req):
    userId = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[userId] = {'name': None}
        return
    if sessionStorage[userId]['name'] is None:
        name = getName(req)
        if name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[userId]['name'] = name
            res['response']['text'] = f'Приятно познакомиться, {name.title()}. Я - Алиса. Я могу показать город или сказать расстояние между городами!'
    else:
        name = sessionStorage[userId]['name'].title()
        cities = getCities(req)
        if not cities:
            res['response']['text'] = name + ', ты не написал не одного города!'
        elif len(cities) == 1:
            res['response']['text'] = f'{name}, этот город в стране {getGeoInfo(cities[0], "country")}'
        elif len(cities) == 2:
            dist = getDistance(getGeoInfo(cities[0], 'coordinates'),
                               getGeoInfo(cities[1], 'coordinates'))
            res['response']['text'] = f'{name}, расстояние между этими городами: {str(round(dist))} км'
        else:
            res['response']['text'] = name + ', слишком много городов!'


def getName(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


def getCities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value'].keys():
                cities.append(entity['value']['city'])
    return cities


if __name__ == '__main__':
    app.run()
