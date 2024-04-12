DEBUG = True

# Configurações do MySQL
MYSQL_DATABASE_PORT = "3306"
MYSQL_DATABASE = "centro_de_protecao_animal"
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "admin"

SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost/centro_de_protecao_animal'

SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'CPAUNIVESP'