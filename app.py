from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default-key-change-me")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User, Poll, Option, Vote

with app.app_context():
    db.create_all()


@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}


from routes import auth_routes, poll_routes, history_routes

app.register_blueprint(auth_routes)
app.register_blueprint(poll_routes)
app.register_blueprint(history_routes)


@app.route('/')
def root():
    return redirect(url_for('polls.index'))


if __name__ == '__main__':
    app.run(debug=True)
