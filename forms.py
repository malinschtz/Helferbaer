from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField("E-Mail", validators=[
        InputRequired(),
        Email()
    ])
    password = PasswordField("Passwort", validators=[InputRequired()])
    submit = SubmitField("Anmelden")

class RegisterForm(FlaskForm):
    firstName = StringField("Vorname", validators=[
        InputRequired(), 
        Length(min=2, max=50)
    ])
    name = StringField("Nachname", validators=[
        InputRequired(), 
        Length(min=2, max=50)
    ])
    birthday = DateField("Geburtsdatum", validators=[InputRequired()])
    email = StringField("E-Mail", validators=[
        InputRequired(), 
        Email(),
        Length(min=6, max=120)
    ])
    phone = StringField("Telefon", validators=[Optional()])
    password = PasswordField("Passwort", validators=[
        InputRequired(), 
        Length(min=8)
    ])
    password_confirm = PasswordField("Wiederholen", validators=[
        InputRequired(), 
        EqualTo("password")
    ])
    submit = SubmitField("Registrieren")