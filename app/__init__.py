from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
csrf = CSRFProtect(app)

def fetch_updates_job():
    with app.app_context():
        from app.update_fetcher import fetch_all_updates
        fetch_all_updates()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job(
    id='fetch_updates_job',
    func=fetch_updates_job,
    trigger='interval',
    hours=24
)
scheduler.start()

from app import routes, models
