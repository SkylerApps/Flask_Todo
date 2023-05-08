import os

from flask import Flask
from flask_login import LoginManager

from extensions import db
from models.User import User
from views.auth import auth_bp
from views.handlers import page_not_found
from views.todo import todo_bp

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(os.getcwd(), 'todo.db'))
app.secret_key = 'your-secret-key'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(todo_bp)
app.register_error_handler(404, page_not_found)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)
