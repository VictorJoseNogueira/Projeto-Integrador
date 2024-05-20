from app import app, db, login_manager
from flask import render_template, url_for, redirect, request, session
from app.models.tables import User, Tutor, Animal
from app.models.form import LoginForm, Cadastro, cadastrar_animal, cadastrar_tutor
from flask_login import login_user, login_required, logout_user
from werkzeug.exceptions import Unauthorized


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
@app.route("/index/")
@login_required
def index():
    search = request.args.get('search')
    if search:
        tutores = Tutor.query.filter(
            (Tutor.nome.ilike(f'%{search}%')) | (Tutor.cpf.ilike(f'%{search}%'))
        ).all()
    else:
        tutores = Tutor.query.order_by(Tutor.id.desc()).limit(10).all()
    return render_template('index.html', tutores=tutores)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        user = User.query.filter_by(email=login.email.data).first()
        if user and user.senha == login.senha.data:
            login_user(user)
            session['logged_in'] = True  # Adicionado
            print("User logged in:", user.id)

            return redirect(url_for('index'))
    return render_template("login.html", login=login)


@app.route('/tutor/<info>')
@app.route('/tutor/', defaults={'info': None}, methods=['GET', 'POST'])
@login_required
def tutor(info):
    form = cadastrar_tutor()
    try:
        if form.validate_on_submit():
            novo_tutor = Tutor(nome=form.nome.data, cpf=form.cpf.data, tel=form.tel.data, endereco=form.endereco.data)
            db.session.add(novo_tutor)
            db.session.commit()
            id_tutor = novo_tutor.id
            return redirect(url_for('cadastramento_animal', info=id_tutor))
    except Exception as e:
        return f"Erro ao cadastrar: {e}"
    return render_template('tutor.html', tutores=form)


@app.route("/cadastro/<info>")
@app.route("/cadastro/", defaults={'info': None}, methods=['GET', 'POST'])
@login_required
def cadastro(info):
    cadastro_form = Cadastro()
    if cadastro_form.validate_on_submit():
        novo_usuario = User(nome=cadastro_form.nome.data, email=cadastro_form.email.data, senha=cadastro_form.senha.data)
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastro.html', cadastro=cadastro_form)


@app.route('/animais/')
@login_required
def animais():
    animals = Animal.query.all()
    return render_template('info_animal.html', animals=animals)


@app.route('/animal/<int:id_tutor>', methods=['GET', 'POST'])
@login_required
def cad_animal(id_tutor):
    id_tutor = request.form.get('id_tutor')
    return render_template(cadastramento_animal)


@app.route('/detalhe/<int:info>')
@login_required
def detalhamento(info):
    tutor = Tutor.query.get(info)
    animais = Animal.query.filter_by(id_tutor=info).all()
    return render_template('detalhamento.html', tutor=tutor, animais=animais)


@app.route('/detalhe/cadastro/<int:info>', methods=['GET', 'POST'])
@login_required
def cadastramento_animal(info):
    tutor_id = info
    cadastro_animal = cadastrar_animal()
    try:
        if cadastro_animal.validate_on_submit():
            novo_animal = Animal(nome=cadastro_animal.nome_animal.data.strip(),
                                 peso_aproximado=cadastro_animal.peso.data,
                                 idade_aproximado=cadastro_animal.idade.data,
                                 sexo=cadastro_animal.sexo.data,
                                 especie=cadastro_animal.raca.data,
                                 id_tutor=tutor_id)
            db.session.add(novo_animal)
            db.session.commit()
            return redirect(url_for('index'))
    except Exception as e:
        return render_template('erro.html')
    return render_template('animal_cadastro.html', info=tutor_id, cadastro_animal=cadastro_animal)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('erro.html', e='Página não encontrada'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', e='Erro interno do servidor'), 500


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Adicionado
    print("Session after logout:", session)  # Adicionado para verificar sessão
    return redirect(url_for('login'))