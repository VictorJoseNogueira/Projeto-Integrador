from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# Criar instância SQLAlchemy (opcional)
db = SQLAlchemy(app)

from app.controllers import default
