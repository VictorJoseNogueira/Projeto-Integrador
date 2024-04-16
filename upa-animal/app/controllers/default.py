from app import app, db
from flask import render_template, url_for, redirect, request, session
from app.models.tables import User, Tutor, Animal
from app.models.form import LoginForm,Cadastro,cadastrar_animal,cadastrar_tutor

@app.route("/")
@app.route("/index/")
def index():
    tutores = Tutor.query.all()
    return render_template('index.html',tutores=tutores)

@app.route('/login/', methods=['GET','POST'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        print(login.email.data)
        print(login.senha.data)
    return render_template("login.html", login=login)

@app.route('/tutor/<info>')
@app.route('/tutor/', defaults={'info':None}, methods=['GET', 'POST'])
def tutor(info):
    form = cadastrar_tutor()
    if form.validate_on_submit():
        print(form.nome.data)
        novo_tutor = Tutor(nome=form.nome.data, cpf=form.cpf.data, tel=form.tel.data, endereco = form.endereco.data)
        db.session.add(novo_tutor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("tutor.html", tutores=form)


@app.route("/cadastro/<info>")
@app.route("/cadastro/", defaults={'info':None}, methods=['GET', 'POST'])
def cadastro(info):
    cadastro = Cadastro()
    if cadastro.validate_on_submit():
        novo_usuario = User(nome=cadastro.nome.data, email=cadastro.email.data, senha=cadastro.senha.data)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html', cadastro=cadastro)


@app.route('/animais/')
def animais():
    animals = Animal.query.all()
    return render_template('detail.html', animals=animals)




@app.route('/animal/')
def cad_animal():
    cad_animal = ''
    return render_template('animal_cadastro.html')



'''@app.route('/detalhes/')
def xpace():
    animals = Animal.query.filter_by(id_tutor=5).all()
    return render_template('detail.html', animals=animals)
'''
