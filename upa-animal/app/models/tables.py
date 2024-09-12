from app import db
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, DateTime  # noqa E501
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class User(db.Model, UserMixin):
    __tablename__ = "administradores"

    id = db.Column(Integer, primary_key=True)
    nome = db.Column(String(255))
    email = db.Column(String(255), unique=True)
    senha = db.Column(String(255))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def is_active(self):
        print("Método is_active foi chamado.")
        return True

    def __repr__(self):
        return f"<USER {self.nome_de_usuario}>"


class Tutor(db.Model):
    __tablename__ = "tutor"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    cpf = db.Column(db.String(14), unique=True)
    tel = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    deleted = db.Column(db.Boolean, default=False)
    deleted_by = db.Column(db.Integer)

    def __init__(self, nome, cpf, tel, endereco, deleted=False, deleted_by=None):  # noqa E501
        self.nome = nome
        self.cpf = cpf
        self.tel = tel
        self.endereco = endereco
        self.deleted = deleted
        self.deleted_by = deleted_by

    def __repr__(self):
        return f'<tutor {self.id}>'


class Animal(db.Model):
    __tablename__ = "animal"
    animal_id = db.Column(Integer, primary_key=True)
    nome = db.Column(String(255))
    peso_aproximado = db.Column(Float)
    idade_aproximado = db.Column(Integer)
    sexo = db.Column(String(10))
    especie = db.Column(String(50))

    # chave estrangeira
    id_tutor = db.Column(Integer, ForeignKey("tutor.id"))
    # relacionamento
    tutor = relationship("Tutor", backref="animais")

    @validates('sexo')
    def validate_sexo(self, key, value):
        if value.lower() not in ['macho', 'femea']:
            raise ValueError('O sexo deve ser "macho" ou "femea"')
        return value

    @validates('especie')
    def validate_especie(self, key, value):
        if value.lower() not in ["cachorro", "gato"]:
            raise ValueError("A especie só pode ser cachorro ou gato")
        return value

    def __init__(self, nome, peso_aproximado, sexo, idade_aproximado, id_tutor, especie):  # noqa E501
        self.nome = nome
        self.peso_aproximado = peso_aproximado
        self.idade_aproximado = idade_aproximado
        self.sexo = sexo
        self.id_tutor = id_tutor
        self.especie = especie

    def __repr__(self):
        return f"<Animal {self.nome}>"


class Consulta(db.Model):
    __tablename__ = "consulta"
    id_consulta = db.Column(Integer, primary_key=True)
    id_animal = db.Column(Integer, ForeignKey("animal.animal_id"))
    id_tutor = db.Column(Integer, ForeignKey("tutor.id"))
    veterinario = db.Column(String(155))
    sintomas = db.Column(Text)
    procedimento = db.Column(Text)
    medicacao = db.Column(Text)
    observacao = db.Column(Text)
    data = db.Column(DateTime)

    # Relacionamentos
    animal = relationship("Animal", backref="consultas")
    tutor = relationship("Tutor", backref="consultas")

    def __init__(self, id_animal, id_tutor, veterinario, sintomas,
                 procedimento, medicacao=None, observacao=None, data=None):

        self.id_animal = id_animal
        self.id_tutor = id_tutor
        self.veterinario = veterinario
        self.sintomas = sintomas
        self.procedimento = procedimento
        self.medicacao = medicacao
        self.observacao = observacao
        self.data = data

    def __repr__(self):
        return f"<Consulta {self.id_consulta}>"
