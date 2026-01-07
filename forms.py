from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField("E-Mail", validators=[
        InputRequired(message="Email erforderlich"),
        Email(message="Bitte eine korrekte Email eingeben")
    ])
    password = PasswordField("Passwort", validators=[InputRequired(message="Passwort erforderlich")])
    submit = SubmitField("Anmelden")

class RegisterForm(FlaskForm):
    firstName = StringField("Vorname", validators=[
        InputRequired(message="Name erforderlich"), 
        Length(min=2, max=50)
    ])
    name = StringField("Nachname", validators=[
        InputRequired(message="Name erforderlich"), 
        Length(min=2, max=50)
    ])
    birthday = DateField("Geburtsdatum", validators=[InputRequired(message="Geburtsdatum erforderlich")])
    email = StringField("E-Mail", validators=[
        InputRequired(message="Email erforderlich"), 
        Email(message="Bitte eine korrekte Email eingeben"),
        Length(min=6, max=120)
    ])
    phone = StringField("Telefon", validators=[Optional()])
    password = PasswordField("Passwort", validators=[
        InputRequired(message="Passwort erforderlich"), 
        Length(min=8)
    ])
    password_confirm = PasswordField("Wiederholen", validators=[
        InputRequired(message="Passwort bestätigen"), 
        EqualTo("password", message="Passwörter stimmen nicht überein")
    ])
    submit = SubmitField("Registrieren")