from app import app
from flask import render_template, url_for, redirect, request, session
from app.models.tables import User, Tutor, Animal
from app.models.form import LoginForm,Cadastro

@app.route("/")
@app.route("/index/")
def index():
    tutores = Tutor.query.all()
    return render_template('index.html',tutores=tutores)

@app.route('/login/')
def login():
    login = LoginForm()
    return render_template("login.html", login=login)

@app.route('/tutor/')
def tutor():
    return render_template("tutor.html")



@app.route('/animais/')
def animais():
    animals = Animal.query.all()
    return render_template('detail.html', animals=animals)

'''@app.route('/detalhes/')
def xpace():
    animals = Animal.query.filter_by(id_tutor=5).all()
    return render_template('detail.html', animals=animals)
'''

@app.route("/cadastro/")
def cadastro():
    cadastro = Cadastro()
    return render_template('cadastro.html', cadastro=cadastro)