from app import app


def test_home_page_logged_out():
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 302
    assert b'Redirect' in response.data


def test_home_page_logged_in():
    with app.test_client() as client:
        # Register a new user
        client.post('/register', data={'email': 'new_user', 'password': 'password'}, follow_redirects=True)

        # Log in with the new user's credentials and follow the redirect
        response = client.post('/login', data={'email': 'new_user', 'password': 'password'}, follow_redirects=True)

        # Check the status code and content of the redirected response
        assert response.status_code == 200
        assert b'to your to-do list!' in response.data

