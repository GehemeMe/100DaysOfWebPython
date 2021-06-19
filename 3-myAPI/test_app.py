
from urllib import response
from apistar import test
from requests import status_codes

from app import app, cities, CITY_NOT_FOUND

client = test.TestClient(app)


def test_list_cities():
    response = client.get('/')
    assert response.status_code == 200

    json_resp = response.json()
    city_count = len(cities)
    assert len(json_resp) == city_count

    expected = {'id': 1,
                'city': 'Pobé',
                'country': 'Benin',
                'country_code': 'BJ',
                'time_zone': 'Africa/Porto-Novo'}
    assert json_resp[0] == expected


def test_create_city():
    city_count = len(cities)
    data = {'city': 'Perpignan',
            'country': 'France',
            'country_code': 'FR',
            'time_zone': 'Europe/Paris'}

    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(cities) == city_count + 1

    response = client.get('/1001/')
    expected = {'id': 1001,
                'city': 'Perpignan',
                'country': 'France',
                'country_code': 'FR',
                'time_zone': 'Europe/Paris'}
    assert response.json() == expected


def test_create_city_missing_fields():
    data = {'key': 1}
    response = client.post('/', data=data)
    assert response.status_code == 400
    
    errors = response.json()
    assert errors['country'] == 'The "country" field is required.'
    assert errors['city'] == 'The "city" field is required.'
    assert errors['country_code'] == 'The "country_code" field is required.'


def test_get_city():
    response = client.get('/100/')
    assert response.status_code == 200
    
    expected = {"id":100,
                "city":"Chimanimani",
                "country":"Zimbabwe",
                "country_code":"ZW",
                "time_zone":"Africa/Harare"}
    assert response.json() == expected
    

def test_city_notfound():
    response = client.get('/999999/')
    assert response.status_code == 404
    assert response.json() == {'error' : CITY_NOT_FOUND}


def test_update_city():
    data = {"city":"some_city",
             "country":"Zimbabwe",
             "country_code":"ZW",
             "time_zone":"Africa/Harare"}
    response = client.put('/100/', data = data)
    assert response.status_code == 200
    
    expected = {"id":100,
                 "city":"some_city",
                 "country":"Zimbabwe",
                 "country_code":"ZW",
                 "time_zone":"Africa/Harare"}
    assert response.json() == expected
    

def test_delete_city():
    city_count = len(cities)
    for i in (11, 22, 33):
        response = client.delete(f'/{i}/')
        assert response.status_code == 204
        
        response = client.get(f'/{i}/')
        assert response.status_code == 404
    
    assert len(cities) == city_count - 3