from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField, FloatField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Optional, NumberRange, Regexp

#Quelle: Kursmaterial 
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

class StellenangebotForm(FlaskForm):
    description = StringField('Beschreibung', validators=[InputRequired(), Length(min=10, max=500)])
    date = DateField('Datum', format='%Y-%m-%d' , validators=[InputRequired()])
    street = StringField('Straße & Hausnummer', validators=[InputRequired()])
    plz = StringField('PLZ', validators=[InputRequired(), Regexp(r'^\d+$', message='Nur Zahlen erlaubt')])
    category = SelectField('Kategorie', choices=[(1, 'Haushaltsnahe Dienstleistungen'), (2, 'Begleitdienste'), (3, 'Betreuung und Gesellschaft')])
    is_template = BooleanField('Als Vorlage speichern?', description='Speichere diese Stellenangebot als Vorlage um es später wieder zu benutzen')
    hours = FloatField('Erwartete Stunden', validators=[InputRequired(), NumberRange(min=0.5, max=10)])
    submit = SubmitField('Stellenangebot aufgeben')

class JobFilterForm(FlaskForm):
    search = StringField('Suche (Beschreibung)', validators=[Optional()])
    category = SelectField('Kategorie', choices=[(1, 'Haushaltsnahe Dienstleistungen'), (2, 'Begleitdienste'), (3, 'Betreuung und Gesellschaft')], default=0, validators=[Optional()])
    plz = StringField('PLZ filtern', validators=[Optional(), Regexp(r'^\d{5}$', message='PLZ: 5 Ziffern')])
    min_hours = FloatField('Min. Stunden', validators=[Optional(), NumberRange(min=0.5)])
    submit = SubmitField('Suchen')

class ProfileForm(FlaskForm):
    firstName = StringField("Vorname", validators=[
        InputRequired(), Length(min=2, max=50)
    ])
    name = StringField("Nachname", validators=[
        InputRequired(), Length(min=2, max=50)
    ])
    email = StringField("E-Mail", validators=[
        InputRequired(), Email(), Length(min=6, max=120)
    ])
    phone = StringField("Telefon", validators=[Optional()])
    birthday = StringField("Geburtstag", validators=[Optional()])
    submit = SubmitField("Speichern")