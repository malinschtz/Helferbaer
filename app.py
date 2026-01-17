from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm, RegisterForm
from sqlalchemy import select
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)
bcrypt = Bcrypt(app) #für Password Hashing

app.config.from_mapping(
    SECRET_KEY = 'secret_key_just_for_dev_environment',
    BOOTSTRAP_BOOTSWATCH_THEME = 'superhero'
)

from db import db, User, Category, Status, Job

bootstrap = Bootstrap5(app) 

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userId):
    return db.session.get(User, userId)


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

@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])  # Sicherer mit ID!
def delete(user_id):
    user = db.session.execute(
        select(User).filter_by(userId=user_id)  # Primärschlüssel!
    ).scalar_one_or_none()
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return 'User gelöscht'
    else:
        return 'user nicht gefunden'
        

@app.route('/helfer/', methods=['GET', 'POST'])
@login_required
def helfer():
    if request.method == 'POST':
        return
    return 'Helfer Startseite'

@app.route('/helfer/anmelden', methods=['GET', 'POST'])
def helfer_anmelden():
    form = LoginForm()
    if form.validate_on_submit(): # Kombiniert if request.method == 'POST': & if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Email nicht gefunden. Bitte erst registrieren!', 'error')
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Passwort ungültig!', 'error')
        elif user.role != 'helfer':
            flash('Nur Alltagshelfer können sich hier anmelden.', 'error')
        else: 
            login_user(user)
            flash('Willkommen zurück!', 'success')
            return redirect(url_for('helfer'))
    return render_template('helfer_anmelden.html', form=form)

@app.route('/helfer/registrieren', methods=['GET', 'POST'])
def helfer_registrieren():
    form = RegisterForm()
    if form.validate_on_submit():
        #prüfen, ob email bereits vorhanden
        if User.query.filter_by(email=form.email.data).first():
            flash('Email breits registriert', 'error')
            return render_template('helfer_registrieren.html', form=form)
            
        user = User(
            firstName = form.firstName.data,
            name = form.name.data,
            birthday = form.birthday.data,
            email = form.email.data,
            phone = form.phone.data or None,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            role = 'helfer'
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registrierung erfolgreich!', 'success')
        return redirect(url_for('helfer'))
    return render_template('helfer_registrieren.html', form=form)

@app.route('/helfer/stellenangebot', methods=['GET', 'POST'])
@login_required
def helfer_stellenangebot():
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
    else:
        #Stundenkonto
        hours = current_user.current_month_hours
        DE_MONTHS = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'}
        monat_name = f"{DE_MONTHS[date.today().month]} {date.today().year}"

        #Anfragen und Erledigte Jobs
        jobs_data = current_user.get_jobs_by_status()
        return render_template('kunde_startseite.html', hours=hours, monat_name=monat_name, **jobs_data)

@app.route('/kunde/anmelden', methods=['GET', 'POST'])
def kunde_anmelden():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Email nicht gefunden. Bitte erst registrieren!', 'error')
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Passwort ungültig!', 'error')
        elif user.role != 'kunde':
            flash('Nur AKunden können sich hier anmelden.', 'error')
        else: 
            login_user(user)
            flash('Willkommen zurück!', 'success')
            return redirect(url_for('kunde'))
    return render_template('kunde_anmelden.html', form=form)

@app.route('/kunde/registrieren', methods=['GET', 'POST'])
def kunde_registrieren():
    form = RegisterForm()
    if form.validate_on_submit():
        #prüfen, ob email bereits vorhanden
        if User.query.filter_by(email=form.email.data).first():
            flash('Email breits registriert', 'error')
            return render_template('kunde_registrieren.html', form=form)
            
        user = User(
            firstName = form.firstName.data,
            name = form.name.data,
            birthday = form.birthday.data,
            email = form.email.data,
            phone = form.phone.data or None,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
            role = 'kunde'
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registrierung erfolgreich!', 'success')
        return redirect(url_for('kunde'))
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

@app.route('/kunde/helfer_anzeigen', methods=['GET', 'POST'])
@login_required
def kunde_helfer_anzeigen():
    if request.method == 'POST':
        return
    return render_template('kunde_helfer_anzeigen.html')


   

