# tests/test_tools.py

def test_get_tools(client):
    response = client.get('/tools')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2  # As per populate_test_db
    assert data[0]['name'] == 'Test Tool 1'

def test_create_tool(client):
    new_tool = {'name': 'New Tool', 'category': 'New Category'}
    response = client.post('/tools', json=new_tool)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'New Tool'
    assert data['category'] == 'New Category'

def test_get_single_tool(client):
    response = client.get('/tools/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Tool 1'

def test_update_tool(client):
    update_data = {'name': 'Updated Tool', 'category': 'Updated Category'}
    response = client.put('/tools/1', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Updated Tool'
    assert data['category'] == 'Updated Category'

def test_delete_tool(client):
    response = client.delete('/tools/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Tool deleted successfully.'

    # Verify deletion
    get_response = client.get('/tools/1')
    assert get_response.status_code == 404
