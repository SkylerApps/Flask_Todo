from app import app
from forms.Login import LoginForm


def test_login_form_short_pw():
    with app.test_request_context():
        form_data = {
            'email': 'invalidemail',
            'password': '123',
            'remember': True
        }
        form = LoginForm(data=form_data)
        assert not form.validate()


def test_login_form_long_pw():
    with app.test_request_context():
        form_data = {
            'email': 'invalidemail',
            'password': '1234567891011121314151617181920',
            'remember': True
        }
        form = LoginForm(data=form_data)
        assert not form.validate()


def test_login_form_short_email():
    with app.test_request_context():
        form_data = {
            'email': 'shrtem@gmail.com',
            'password': '12345678',
            'remember': True
        }
        form = LoginForm(data=form_data)
        assert not form.validate()


def test_login_form_long_email():
    with app.test_request_context():
        form_data = {
            'email': 'longemailfortesting@gmail.com',
            'password': '12345678',
            'remember': True
        }
        form = LoginForm(data=form_data)
        assert not form.validate()
