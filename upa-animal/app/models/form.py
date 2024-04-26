from flask_wtf import FlaskForm
from wtforms import  PasswordField,BooleanField, EmailField, StringField,IntegerField, FloatField,SelectField,TextAreaField
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
    raca = SelectField('Raça', choices=[('gato'), ('cachorro')], validators=[DataRequired()])
    peso = FloatField('Peso', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('macho'), ('femea')], validators=[DataRequired()])
    id_tutor = IntegerField('ID Tutor', validators=[DataRequired()])
