from email.policy import default
from pprint import pprint
import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_cities_data():
    with open('cities_data.json') as f:
        cities = json.loads(f.read())
        return {city["id"]: city for city in cities}


cities = _load_cities_data()

VALID_COUNTRIES = set([city["country"] for city in cities.values()])
CITY_NOT_FOUND = 'City not found'

class City(types.Type):
    id = validators.Integer(allow_null=True)
    country = validators.String(enum=list(VALID_COUNTRIES))
    city = validators.String(max_length=100)
    country_code = validators.String(max_length=2)
    time_zone = validators.String(max_length=200, default='')
    
def list_cities() -> List[City]:
    return [City(city[1]) for city in sorted(cities.items())]

def create_city(city: City) -> JSONResponse:
    city_id = max(cities.keys())+1
    city.id = city_id
    cities[city_id] = city
    return JSONResponse(City(city), status_code=201)

def get_city(city_id: int) -> JSONResponse:
    city = cities.get(city_id)
    if not city:
        error = {'error' : CITY_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    
    return JSONResponse(City(city), status_code=200)
        

def update_city(city_id: int, city: City) -> JSONResponse:
    if not cities.get(city_id):
        error = {'error': CITY_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    
    city.id = city_id
    cities[city_id] = city
    return JSONResponse(City(city), status_code=200)
        

def delete_city(city_id: int) -> JSONResponse:
    if not cities.get(city_id):
        error = {'error': CITY_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    
    del cities[city_id]
    return JSONResponse({}, status_code=204)



routes = [
    Route('/', method='GET', handler=list_cities),
    Route('/', method='POST', handler=create_city),
    Route('/{city_id}/', method='GET', handler=get_city),
    Route('/{city_id}/', method='PUT', handler=update_city),
    Route('/{city_id}/', method='DELETE', handler=delete_city),
]

app = App(routes = routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)