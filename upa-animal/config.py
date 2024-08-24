import os

DEBUG = os.environ.get("DEBUG")
# Configurações do MySQL
MYSQL_DATABASE_PORT = os.environ.get("MYSQL_DATABASE_PORT")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")  # noqa E501

SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")  # noqa E501

SECRET_KEY = os.environ.get("SECRET_KEY")


SESSION_TYPE = os.environ.get("SESSION_TYPE")
