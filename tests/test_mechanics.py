# tests/test_mechanics.py

def test_get_mechanics(client):
    response = client.get('/mechanics')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2  # As per populate_test_db
    assert data[0]['name'] == 'Test Mechanic 1'


def test_create_mechanic(client):
    new_mechanic = {'name': 'New Mechanic'}
    response = client.post('/mechanics', json=new_mechanic)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'New Mechanic'


def test_get_single_mechanic(client):
    response = client.get('/mechanics/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Mechanic 1'


def test_update_mechanic(client):
    update_data = {'name': 'Updated Mechanic'}
    response = client.put('/mechanics/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Mechanic'


def test_delete_mechanic(client):
    response = client.delete('/mechanics/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Mechanic deleted successfully.'

    # Verify deletion
    get_response = client.get('/mechanics/1')
    assert get_response.status_code == 404
