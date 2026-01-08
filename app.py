from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm, RegisterForm
from flask_login import LoginManager, login_required

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'superhero'
)

from db import db, User, Category, Status, Job, insert_sample

bootstrap = Bootstrap5(app) 

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

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
@login_required
def helfer():
    if request.method == 'POST':
        return
    return 'Helfer Startseite'

@app.route('/helfer/anmelden', methods=['GET', 'POST'])
def helfer_anmelden():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
        # ToDo Login Logik
            return redirect(url_for('helfer'))
        else: 
            flash('Anmeldung fehlgeschlagen', 'error')
    return render_template('helfer_anmelden.html', form=form)

@app.route('/helfer/registrieren', methods=['GET', 'POST'])
def helfer_registrieren():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
        # ToDo Register Logik
            return redirect(url_for('helfer'))
        else: 
            flash('Registrierung fehlgeschlagen', 'error')
    return render_template('helfer_registrieren.html', form=form)

@app.route('/helfer/stellenangebot', methods=['GET', 'POST'])
@login_required
def hlefer_stellenangebot():
    if request.method == 'POST':
        return
    return 'Helfer Stellenangebote suchen'

@app.route('/helfer/profil', methods=['GET', 'POST'])
@login_required
def helfer_profil():
    if request.method == 'POST':
        return
    return 'Helfer Profil'

@app.route('/kunde/', methods=['GET', 'POST'])
@login_required
def kunde():
    if request.method == 'POST':
        return
    return render_template('kunde_startseite.html')

@app.route('/kunde/anmelden', methods=['GET', 'POST'])
def kunde_anmelden():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():
        # ToDo Login Logik
            return redirect(url_for('kunde'))
        else: 
            flash('Anmeldung fehlgeschlagen', 'error')
    return render_template('kunde_anmelden.html', form=form)

@app.route('/kunde/registrieren', methods=['GET', 'POST'])
def kunde_registrieren():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate():
        # ToDo Register Logik
            return redirect(url_for('kunde'))
        else: 
            flash('Registrierung fehlgeschlagen', 'error')
    return render_template('kunde_registrieren.html', form=form)

@app.route('/kunde/stellenangebot', methods=['GET', 'POST'])
@login_required
def kunde_stellenangebot():
    if request.method == 'POST':
        return
    return 'Kunde Stellenangebot aufgeben'

@app.route('/kunde/profil', methods=['GET', 'POST'])
@login_required
def kunde_profil():
    if request.method == 'POST':
        return
    return 'Kunde Profil'

@app.route('/insert/sample')
def run_insert_sample():
    insert_sample()
    return 'Database flushed and populated with some sample data.'

   

