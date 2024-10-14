"""import os

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
"""
DEBUG = True
# Configurações do MySQL
MYSQL_DATABASE_PORT = "25721"
MYSQL_DATABASE = "railway"
MYSQL_HOST = "junction.proxy.rlwy.net"
MYSQL_USER = "root"
MYSQL_PASSWORD = "rKhHzqnEBZCyyZoBnBLGAeXbXscJsqAw"

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rKhHzqnEBZCyyZoBnBLGAeXbXscJsqAw@junction.proxy.rlwy.net:25721/railway'

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'zjoQB"*%I>}cjpRwm(M#V/U^:f+mc%mKRkoh/XDgKF{gVupo-f}+R?f&u,ng*dd'


SESSION_TYPE = 'filesystem'
