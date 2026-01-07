from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm, RegisterForm

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'pulse'
)

from db import db, User, Category, Status, Job

bootstrap = Bootstrap5(app) 

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'helfer' in request.form:
            action = request.form['helfer']
            if action == 'login':
                return redirect(url_for('helfer_anmelden'))
            elif action == 'register':
                return redirect(url_for('helfer_registrieren'))

        if 'kunde' in request.form:
            action = request.form['kunde']
            if action == 'login':
                return redirect(url_for('kunde_anmelden'))
            elif action == 'register':
                return redirect(url_for('kunde_registrieren'))
    
    return render_template('index.html')

@app.route('/helfer/', methods=['GET', 'POST'])
def helfer():
    if request.method == 'POST':
        return
    return 'Helfer Startseite'

@app.route('/helfer/anmelden', methods=['GET', 'POST'])
def helfer_anmelden():
    form = LoginForm()
    if form.validate_on_submit():
        # ToDo Login Logik
        flash('Login erfolgreich!', 'success')
        return redirect(url_for('helfer'))
    return render_template('helfer_anmelden.html', form=form)

@app.route('/helfer/registrieren', methods=['GET', 'POST'])
def helfer_registrieren():
    if request.method == 'POST':
        return
    return render_template('helfer_registrieren.html')

@app.route('/helfer/stellenangebot', methods=['GET', 'POST'])
def hlefer_stellenangebot():
    if request.method == 'POST':
        return
    return 'Helfer Stellenangebote suchen'

@app.route('/helfer/profil', methods=['GET', 'POST'])
def hlefer_profil():
    if request.method == 'POST':
        return
    return 'Helfer Profil'

@app.route('/kunde/', methods=['GET', 'POST'])
def kunde():
    if request.method == 'POST':
        return
    return 'Kunde Startseite'

@app.route('/kunde/anmelden', methods=['GET', 'POST'])
def kunde_anmelden():
    if request.method == 'POST':
        return
    return render_template('kunde_anmelden.html')

@app.route('/kunde/registrieren', methods=['GET', 'POST'])
def kunde_registrieren():
    if request.method == 'POST':
        return
    return render_template('kunde_registrieren.html')

@app.route('/kunde/stellenangebot', methods=['GET', 'POST'])
def kunde_stellenangebot():
    if request.method == 'POST':
        return
    return 'Kunde Stellenangebot aufgeben'

@app.route('/kunde/profil', methods=['GET', 'POST'])
def kunde_profil():
    if request.method == 'POST':
        return
    return 'Kunde Profil'


   

