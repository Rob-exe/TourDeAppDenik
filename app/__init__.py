import os
from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
#connection to api
api_commits = requests.get('https://tda.knapa.cz/commit/', headers={'x-access-token': 'cc21ac07629d323bd2c85570379cf05c','accept': 'application/json'})
api_users = requests.get('https://tda.knapa.cz/user/', headers={'x-access-token': 'cc21ac07629d323bd2c85570379cf05c','accept': 'application/json'})
api_sys = requests.get('https://tda.knapa.cz/sysinfo/', headers={'x-access-token': 'cc21ac07629d323bd2c85570379cf05c','accept': 'application/json'})
def create_app():


    app = Flask(__name__)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config['SECRET_KEY'] = 'cc21ac07629d323bd2c85570379cf05c'
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'tourdeflask.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denik.db'    
    app.config['UPLOAD_FOLDER'] = os.path.abspath("app/static/backups/") #useless command (no impact on code)
    db.init_app(app)



    # blueprint for api parts of app
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)   
    # blueprint for data managing parts of app
    from .data_manage import data as data_blueprint
    app.register_blueprint(data_blueprint)
    # blueprint for backup parts of app
    from .backup import back as backup_blueprint
    app.register_blueprint(backup_blueprint)
    # blueprint for main parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# ensure the instance folder exists
if __name__ == '__main__':
    create_app().run(debug=True)