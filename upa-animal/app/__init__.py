from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config.from_object('config')

# Criar instância SQLAlchemy (opcional)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from app.controllers import default
