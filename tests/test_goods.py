import json
from http.client import BAD_REQUEST, OK, NOT_FOUND, CREATED


def test_health(app, client):
    res = client.get('/health')
    assert res.status_code == OK
    expected = {"status": "OK"}
    assert expected == json.loads(res.get_data(as_text=True))


def test_get_invalid_id(app, client):
    res = client.get('/api/v1/goods/invalid_id_value')
    assert res.status_code == BAD_REQUEST
    expected = {'response': 'invalid id: invalid_id_value'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_delete_invalid_id(app, client):
    res = client.delete('/api/v1/goods/invalid_id_value')
    assert res.status_code == BAD_REQUEST
    expected = {'response': 'invalid id: invalid_id_value'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_put_invalid_id(app, client):
    res = client.put('/api/v1/goods/invalid_id_value')
    assert res.status_code == BAD_REQUEST
    expected = {'response': 'invalid id: invalid_id_value'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_get_not_found(app, client):
    res = client.get('/api/v1/goods/183e3d23-47ee-4eda-bb3e-758eacb91149')
    assert res.status_code == NOT_FOUND


def test_add_goods(app, client):
    # given
    product = {
        "name": "product #1",
        "description": "description #1",
        "stock": 30,
        "price": 510
    }

    # then
    res = client.post('/api/v1/goods', data=json.dumps(product), content_type='application/json')

    # assert
    assert res.status_code == CREATED
    assert json.loads(res.get_data(as_text=True))["id"] is not None


def test_get_goods(app, client):
    # given
    created_id = create_sample_product(client)

    # get by id
    res = client.get(f'/api/v1/goods/{created_id}')
    assert res.status_code == OK
    expected = {
        "id": created_id,
        "name": "product #1",
        "description": "description #1",
        "stock": 30.0,
        "price": "$510.00"
    }
    assert expected == json.loads(res.get_data(as_text=True))


def test_delete_goods(app, client):
    # given
    created_id = create_sample_product(client)

    # get by id
    res = client.delete(f'/api/v1/goods/{created_id}')
    assert res.status_code == OK


def test_update_goods(app, client):
    # given
    created_id = create_sample_product(client)

    # update merchandise
    product = {
        "name": "product #1 - updated",
        "description": "description #1 - updated",
        "stock": 120,
        "price": 987
    }

    res = client.put(f'/api/v1/goods/{created_id}', data=json.dumps(product), content_type='application/json')
    assert res.status_code == OK


def create_sample_product(client):
    product = {
        "name": "product #1",
        "description": "description #1",
        "stock": 30,
        "price": 510
    }

    # then add new goods
    res = client.post('/api/v1/goods', data=json.dumps(product), content_type='application/json')

    # assert
    assert res.status_code == CREATED

    created_id = json.loads(res.get_data(as_text=True))["id"]
    assert created_id is not None
    return created_id
