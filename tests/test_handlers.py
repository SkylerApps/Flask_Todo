from app import app


def test_page_not_found():
    client = app.test_client()

    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404
    assert b'404' in response.data
    assert b'404 Not Found!' in response.data

