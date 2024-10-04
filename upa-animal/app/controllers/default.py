from app import app, db, login_manager
from flask import render_template, url_for, redirect, request, session, flash, abort  # noqa E501
from app.models.tables import User, Tutor, Animal, Consulta
from app.models.form import LoginForm, Cadastro, cadastrar_animal, cadastrar_tutor, Cadastrar_Consulta  # noqa E501
from flask_login import login_user, login_required, logout_user
from werkzeug.exceptions import Unauthorized
from datetime import datetime


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
            (Tutor.nome.ilike(f'%{search}%')) | (Tutor.cpf.ilike(f'%{search}%')),  # noqa E501
            Tutor.deleted == False  # noqa
        ).all()
    else:
        tutores = Tutor.query.filter_by(deleted=False).order_by(Tutor.id.desc()).limit(10).all()  # noqa E501
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
            novo_tutor = Tutor(nome=form.nome.data, cpf=form.cpf.data, tel=form.tel.data, endereco=form.endereco.data)  # noqa E501
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
        novo_usuario = User(nome=cadastro_form.nome.data, email=cadastro_form.email.data, senha=cadastro_form.senha.data)  # noqa E501
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
    return render_template(cadastramento_animal, id_tutor=id_tutor)


@app.route('/detalhe/<int:info>', methods=['GET', 'POST'])
@login_required
def detalhamento(info):
    tutor = Tutor.query.get(info)
    animais = Animal.query.filter_by(id_tutor=info).all()

    if request.method == "POST" and "nome" in request.form:  # noqa E501
        tutor.nome = request.form['nome']
        tutor.cpf = request.form['cpf']
        tutor.tel = request.form['tel']
        tutor.endereco = request.form['endereco']
    try:
        db.session.commit()
    except Exception as e:
        print("Erro ao atualizar o Tutor:", e)
        db.session.rollback()  # Rollback caso ocorra um erro

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
    except Exception as e:  # noqa
        return render_template('erro.html')
    return render_template('animal_cadastro.html', info=tutor_id, cadastro_animal=cadastro_animal)  # noqa E501


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


@app.route('/remover-tutor/<int:info>', methods=['POST'])
@login_required
def remover_tutor(info):
    tutor = Tutor.query.get_or_404(info)
    tutor.deleted = True
    db.session.commit()
    flash('Tutor foi removido com sucesso.', 'success')
    return redirect(url_for('index'))  # Redirecione para a rota que deseja, por exemplo 'index'  # noqa E501

@app.route('/detalhe-animal/<int:info>/<int:info_animal_id>', methods=['GET', 'POST'])  # noqa E501
@login_required
def show_animal_detail(info, info_animal_id):
    tutor = Tutor.query.get(info)
    if not tutor:
        abort(404, description="Tutor não encontrado")

    # Filtrando pelo ID do animal específico
    animal = Animal.query.filter_by(id_tutor=info, animal_id=info_animal_id).first()  # noqa E501
    if not animal:
        abort(404, description="Animal não encontrado")

    # Consultas relacionadas ao animal
    consulta = Consulta.query.filter(Consulta.id_tutor == info, Consulta.id_animal == info_animal_id).all()  # noqa E501
    cad_consulta = Cadastrar_Consulta()

    # Pegando a data atual no formato correto para MySQL
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%Y-%m-%d %H:%M:%S")  # Formato compatível com MySQL  # noqa E501

    # Atribuindo manualmente os valores de id_tutor, id_animal e data
    cad_consulta.id_tutor = info
    cad_consulta.id_animal = info_animal_id
    cad_consulta.data.data = data_formatada

    try:
        if cad_consulta.validate_on_submit():
            print("Formulário validado com sucesso.")
            nova_consulta = Consulta(
                id_animal=info_animal_id,
                id_tutor=info,
                veterinario=cad_consulta.veterinario.data,
                sintomas=cad_consulta.sintomas.data,
                procedimento=cad_consulta.procedimento.data,
                medicacao=cad_consulta.medicacao.data,
                observacao=cad_consulta.observacao.data,
                data=data_formatada  # Agora no formato correto para o banco de dados  # noqa E501
            )
            db.session.add(nova_consulta)
            db.session.commit()
            return redirect(url_for('show_animal_detail', info=info, info_animal_id=info_animal_id))  # noqa E501
        else:
            print("Formulário não validado:", cad_consulta.errors)
    except Exception as e:
        print("Erro ao salvar a consulta:", e)
        return render_template('erro.html')


    if request.method == 'POST' and 'nomeAnimal' in request.form:  # noqa E501
        animal.nome = request.form['nomeAnimal']
        animal.peso_aproximado = request.form['pesoAnimal']
        animal.idade_aproximado = request.form['idadeAnimal']
        animal.especie = request.form['especieAnimal']
        animal.sexo = request.form['sexoAnimal']

        try:
            db.session.commit()
            return redirect(url_for('show_animal_detail', info=info, info_animal_id=info_animal_id))  # noqa E501
        except Exception as e:
            print("Erro ao atualizar o animal:", e)
            db.session.rollback()  # Rollback caso ocorra um erro



    return render_template('animal_detail_page.html', tutor=tutor, animal=animal, consulta=consulta, cad_consulta=cad_consulta)  # noqa E501
