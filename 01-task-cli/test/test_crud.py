
from fastapi.testclient import TestClient

test_user = {
    "name":"testuser",
    "age":20,
    "secret_name": "secret"
}
test_user_2 = {
    "name":"testuser_2",
    "age":21,
    "secret_name": "secret_name"
}
test_update_user = {
    "name":"testuser",
    "age":20
}
    
def test_successful_hero_creation(client: TestClient):
    response = client.post('/heroes/', json=test_user)
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == test_user["name"]
    assert data['age'] == test_user["age"]
    assert data['id'] is not None

def test_create_hero_with_missing_info(client: TestClient):
    response = client.post('/heroes/', json=test_update_user)
    assert response.status_code == 422
    
def test_update_missing(client: TestClient):
    response = client.patch('/heroes/100', json=test_user)
    assert response.status_code == 404
    
def test_successful_update(client: TestClient):
    response = client.post('/heroes/', json=test_user)
    created_id = response.json()['id']
    response = client.patch('/heroes/1', json=test_update_user)
    data = response.json()
    assert response.status_code == 200
    assert data['name'] == test_update_user["name"]
    
def test_get_all_heroes(client: TestClient):
    response = client.post('/heroes/', json=test_user)
    response = client.post('/heroes/', json=test_user_2)
    response = client.get('/heroes/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2