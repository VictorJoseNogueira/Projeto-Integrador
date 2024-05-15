from app import app, db
from flask import render_template, url_for, redirect, request, session
from app.models.tables import User, Tutor, Animal
from app.models.form import LoginForm,Cadastro,cadastrar_animal,cadastrar_tutor


#pagina inicial 
@app.route("/")
@app.route("/index/")
def index():
    tutores = Tutor.query.order_by(Tutor.id.desc()).limit(10).all()
    return render_template('index.html',tutores=tutores)



# pagina login
@app.route('/login/', methods=['GET','POST'])
def login():
    login = LoginForm()
    if login.validate_on_submit():
        print(login.email.data)
        print(login.senha.data)
    return render_template("login.html", login=login)



# pagina de cadastro para tutores 
@app.route('/tutor/<info>')
@app.route('/tutor/', defaults={'info':None}, methods=['GET', 'POST'])
def tutor(info):
    form = cadastrar_tutor()
    try:
        if form.validate_on_submit():
            print(form.nome.data)
            novo_tutor = Tutor(nome=form.nome.data, cpf=form.cpf.data, tel=form.tel.data, endereco=form.endereco.data)
            db.session.add(novo_tutor)
            db.session.commit()
            id_tutor = novo_tutor.id

            return redirect(url_for('cadastramento_animal', info=id_tutor))
    except Exception as e:
        return f"Erro ao cadastrar: {e}"
    return render_template("tutor.html", tutores=form)




# pagina de cadastro de novos funcionarios
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



#pagina de exibição dos animais no db
@app.route('/animais/')
def animais():
    animals = Animal.query.all()
    return render_template('info_animal.html', animals=animals)



# pagina de cadastro de animais no db
@app.route('/animal/<int:id_tutor>', methods=['GET', 'POST'])
def cad_animal(id_tutor):
    id_tutor = request.form.get('id_tutor')
    return render_template(cadastramento_animal)





@app.route('/detalhe/<int:info>')
def detalhamento(info):
    tutor = Tutor.query.get(info)
    animais = Animal.query.filter_by(id_tutor=info).all()
    return render_template('detalhamento.html', tutor=tutor, animais=animais)
 

@app.route('/detalhe/cadastro/<int:info>', methods=['GET', 'POST'])
def cadastramento_animal(info):
    tutor_id = info
    cadastro_animal = cadastrar_animal()
    hide_id_tutor = True
    try:
        if cadastro_animal.validate_on_submit():
            novo_animal=Animal(nome=cadastro_animal.nome_animal.data.strip(),
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
    
    return render_template('animal_cadastro.html', info=tutor_id, cadastro_animal=cadastro_animal,hide_id_tutor=hide_id_tutor)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('erro.html', e='Página não encontrada'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', e='Erro interno do servidor'), 500
