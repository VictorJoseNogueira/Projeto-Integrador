from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, EmailField, StringField, IntegerField, FloatField, SelectField, TextAreaField, DateTimeField  # noqa E501
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class Cadastro(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])


class cadastrar_tutor(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    tel = StringField('tel', validators=[DataRequired()])
    endereco = StringField('endereco', validators=[DataRequired()])


class cadastrar_animal(FlaskForm):
    nome_animal = StringField('nome', validators=[DataRequired()])
    raca = SelectField('Raça', choices=[('gato'), ('cachorro')], validators=[DataRequired()])  # noqa E501
    peso = FloatField('Peso', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('macho'), ('femea')], validators=[DataRequired()])  # noqa E501
    id_tutor = IntegerField('ID Tutor', validators=[DataRequired()], render_kw={'style': 'display:none;'})  # noqa E501


class Cadastrar_Consulta(FlaskForm):

    veterinario = StringField('Veterinário', validators=[DataRequired()])
    sintomas = TextAreaField('Sintomas', validators=[DataRequired()])
    procedimento = TextAreaField('Procedimento', validators=[DataRequired()])
    medicacao = TextAreaField('Medicação')
    observacao = TextAreaField('Observação')
    data = DateTimeField('Data', validators=[DataRequired()])
