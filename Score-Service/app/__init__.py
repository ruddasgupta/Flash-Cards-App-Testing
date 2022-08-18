from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
swaggerui_blueprint = get_swaggerui_blueprint(
    Config.SWAGGER_URL,
    Config.API_URL,
    config={
        'app_name': 'Flash-Card-App'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=Config.SWAGGER_URL)

health = HealthCheck()
envdump = EnvironmentDump()

def health_database_status():
    is_database_working = True
    output = 'database is ok'

    try:
        # to check database we will execute raw query
        session = db.session()
        session.execute('SELECT * FROM SCORE')
    except Exception as e:
        output = str(e)
        is_database_working = False

    return is_database_working, output

health.add_check(health_database_status)

# add your Git data to the environment dump
def application_data():
    return {"maintainer": "Rudraraj Dasgupta",
            "git_repo": "https://github.com/ruddasgupta/Flash-Cards-App-Testing"}

envdump.add_section("application", application_data)

# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())

migrate = Migrate(app, db)

from app import routes, models