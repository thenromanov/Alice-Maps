from flask import Flask, request
from geo import getCoords, getCountry, getDist
import logging
import json


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


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
    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу показать город или сказать расстояние между городами!'
        return
    cities = getCities(req)
    if not cities:
        res['response']['text'] = 'Ты не написал не одного города!'
    elif len(cities) == 1:
        res['response']['text'] = f'Этот город в стране {getCountry(cities[0])}'
    elif len(cities) == 2:
        dist = getDist(getCoords(cities[0]), getCoords(cities[1]))
        res['response']['text'] = f'Расстояние между этими городами: {str(round(dist))} км'
    else:
        res['response']['text'] = 'Слишком много городов!'


def getCities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO':
            if 'city' in entity['value'].keys():
                cities.append(entity['value']['city'])
    return cities


if __name__ == '__main__':
    app.run()
