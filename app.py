from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from forms import LoginForm, RegisterForm, StellenangebotForm, JobFilterForm
from sqlalchemy import select, func
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import date

app = Flask(__name__)
bcrypt = Bcrypt(app)    #Quelle: Flask-Bcrypt

app.config.from_mapping(                                    
    SECRET_KEY = 'secret_key_just_for_dev_environment',     
    BOOTSTRAP_BOOTSWATCH_THEME = 'superhero'
)

from db import db, User, Category, Job

bootstrap = Bootstrap5(app) 

login_manager = LoginManager()      #Quelle: Flask-Login, Abschnitt "Configuring your Application"
login_manager.init_app(app)

@login_manager.user_loader      #Quelle: Flask-Login, Abschnitt "How it Works"
def load_user(userId):
    return db.session.get(User, userId)     #Quelle: SQLAlchemy Session Basics, Abschnitt "Get by Primary Key"


@app.route('/', methods=['GET', 'POST'])    #Quelle: Kursmaterial Flask routing und requests, Abschnitt "5"
def index():
    if request.method == 'POST': #prüft, ob auf button geklickt wurde
        if 'helfer' in request.form:        #Quelle: Kursmaterial Flask routing und requests, Abschnit "6"
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

@app.route('/helfer/', methods=['GET'])
@login_required
def helfer():
    if current_user.role != 'helfer':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    # Stundenkonto
    hours = current_user.current_month_hours_helfer
    DE_MONTHS = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'}
    monat_name = f"{DE_MONTHS[date.today().month]} {date.today().year}"     #Quelle: Python datetime today, Abschnitt "date Objects"

    # Gebuchte und erledigte Jobs
    jobs_data = current_user.get_jobs_by_status_helfer()
    
    return render_template('helfer_startseite.html', hours=hours, monat_name=monat_name, **jobs_data)   #Quelle: Python Unpacking Operators

@app.route('/helfer/anmelden', methods=['GET', 'POST'])
def helfer_anmelden():
    form = LoginForm()      #Quelle: Kursmaterial User Interfaces, Abschnitt "2"
    if form.validate_on_submit(): # Kombiniert if request.method == 'POST' & if form.validate() Quelle: Flask-WTF, Abschnitt "Validating Forms"
        user = db.session.execute(      #Quelle: Kursmaterial SQLAlchemy, Abschnitt "7"
            select(User).filter_by(email=form.email.data) #Benutzer suchen nach E-Mail
            ).scalar_one_or_none()      
        if not user:
            flash('Email nicht gefunden. Bitte erst registrieren!', 'error')
        elif not bcrypt.check_password_hash(user.password, form.password.data):     #Quelle: Flask-Bcrypt
            flash('Passwort ungültig!', 'error')
        elif user.role != 'helfer':
            flash('Nur Alltagshelfer können sich hier anmelden. Bitte melden Sie sich als Kunde an', 'error')
        else: 
            login_user(user)        #Quelle: Flask-Login, Abschnitt "Login Example"
            flash(f'Willkommen zurück {user.firstName}!', 'success')
            return redirect(url_for('helfer'))
    return render_template('helfer_anmelden.html', form=form)

@app.route('/helfer/registrieren', methods=['GET', 'POST'])
def helfer_registrieren():
    form = RegisterForm()
    if form.validate_on_submit():
        #prüfen, ob email bereits vorhanden
        user = db.session.execute(
            select(User).filter_by(email=form.email.data)
            ).scalars().first()
        if user:
            flash('Email breits registriert', 'error')
            return render_template('helfer_registrieren.html', form=form)
            
        user = User(
            firstName = form.firstName.data,
            name = form.name.data,
            birthday = form.birthday.data,
            email = form.email.data,
            phone = form.phone.data or None,
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8'),       #Quelle: Flask-Bcrypt, Abschnitt "Usage"
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
    if current_user.role != 'helfer':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    form = JobFilterForm()

    categories = db.session.execute(select(Category)).scalars()
    form.category.choices = [(0, 'Alle')] + [(c.catId, c.catName) for c in categories]
    
    #db.session.execute(select(Model)) führt zu Problem wegen Rückgabe Objekt, Quelle: KI Prompt 1
    stmt = select(Job).where(Job.statusId == 1).order_by(Job.date.asc())

    if form.validate_on_submit():
        if form.search.data:
            stmt = stmt.where(Job.description.ilike(f'%{form.search.data}%'))
        if form.category.data != '0':
            stmt = stmt.where(Job.catId == form.category.data)
        if form.plz.data:
            stmt = stmt.where(Job.plz == int(form.plz.data))
        if form.min_hours.data:
            stmt = stmt.where(Job.hours >= form.min_hours.data)
        
    jobs = db.paginate(stmt, page=request.args.get('page', 1, type=int), per_page=10) #zeigt nur 10 Jobs pro Seite;Seitenwechsel möglich
    
    return render_template('helfer_stellenangebot.html', form=form, jobs=jobs)

@app.route('/helfer/profil', methods=['GET', 'POST'])
@login_required
def helfer_profil():
    if request.method == 'POST':
        return
    return 'Helfer Profil'

@app.route('/helfer/kunde_profil/<int:kunde_id>', methods=['GET'])
@login_required
def helfer_kunde_profil(kunde_id):
    if current_user.role != 'helfer':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    kunde = db.session.get(User, kunde_id)
    # Alle gemeinsamen Jobs
    kunde_jobs = db.session.execute(select(Job).filter_by(
        helferId=current_user.userId,
        kundeId=kunde.userId,
        statusId=3
        ).order_by(Job.date.desc())
        ).scalars()

    return render_template('helfer_kunde_profil.html', kunde=kunde, kunde_jobs=kunde_jobs)

@app.route('/helfer/job_buchen/<int:job_id>', methods=['POST'])
@login_required
def helfer_job_buchen(job_id):
    if current_user.role != 'helfer':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 

    job = db.session.get(Job, job_id)
    job.helferId = current_user.userId
    job.statusId = 2 
    db.session.commit()
    flash(f'"{job.description[:30]}..." gebucht! Details im Dashboard.', 'success')
    return redirect(url_for('helfer_stellenangebot'))

@app.route('/kunde/', methods=['GET'])
@login_required
def kunde():
    if current_user.role != 'kunde':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    #Stundenkonto
    hours = current_user.current_month_hours_kunde
    DE_MONTHS = {1: 'Januar', 2: 'Februar', 3: 'März', 4: 'April',5: 'Mai', 6: 'Juni', 7: 'Juli', 8: 'August',9: 'September', 10: 'Oktober', 11: 'November', 12: 'Dezember'}
    monat_name = f"{DE_MONTHS[date.today().month]} {date.today().year}"

    #Anfragen und Erledigte Jobs
    jobs_data = current_user.get_jobs_by_status_kunde()
    return render_template('kunde_startseite.html', hours=hours, monat_name=monat_name, **jobs_data)

@app.route('/kunde/anmelden', methods=['GET', 'POST'])
def kunde_anmelden():
    form = LoginForm()   
    if form.validate_on_submit():
        user = db.session.execute(   
            select(User).filter_by(email=form.email.data)
            ).scalar_one_or_none()      
        if not user:
            flash('Email nicht gefunden. Bitte erst registrieren!', 'error')
        elif not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Passwort ungültig!', 'error')
        elif user.role != 'kunde':
            flash('Nur Kunden können sich hier anmelden. Bitte melden Sie sich als Helfer an.', 'error')
        else: 
            login_user(user)
            flash(f'Willkommen zurück {user.firstName}!', 'success')
            return redirect(url_for('kunde'))
    return render_template('kunde_anmelden.html', form=form)

@app.route('/kunde/registrieren', methods=['GET', 'POST'])
def kunde_registrieren():
    form = RegisterForm()
    if form.validate_on_submit():
        #prüfen, ob email bereits vorhanden
        user = db.session.execute(
            select(User).filter_by(email=form.email.data)
            ).scalars().first()
        if user:
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
    if current_user.role != 'kunde':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 

    form = StellenangebotForm()

    if form.validate_on_submit():
        job = Job(
            kundeId = current_user.userId,
            description = form.description.data,
            date = form.date.data,
            street = form.street.data,
            plz = form.plz.data,
            catId = form.category.data,
            statusId = 1,
            hours = form.hours.data,
            isTemplate = form.is_template.data,
        )
        db.session.add(job)
        db.session.commit()
        if form.is_template.data:
            flash('Vorlage gespeichert! Wird in "Meine Vorlagen" angezeigt.', 'info')
        flash('Stellenangebot aufgegeben! Helfer werden benachrichtigt.')
        return redirect(url_for('kunde'))
    
    return render_template('kunde_stellenangebot.html', form=form)

@app.route('/kunde/profil', methods=['GET', 'POST'])
@login_required
def kunde_profil():
    if request.method == 'POST':
        return
    return 'Kunde Profil'

@app.route('/kunde/helfer_profil/<int:helfer_id>', methods=['GET'])
@login_required
def kunde_helfer_profil(helfer_id):
    if current_user.role != 'kunde':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    helfer = db.session.get(User, helfer_id)
    # Alle gemeinsamen Jobs
    helfer_jobs = db.session.execute(select(Job).filter_by(
        kundeId=current_user.userId,
        helferId=helfer.userId,
        statusId=3
    ).order_by(Job.date.desc())
    ).scalars()

    # Alle Jobs des Helfers 
    total_jobs = db.session.execute(select(func.count(Job.jobId)).filter_by(    #Quelle: SQLAlchemy SQL and Generic Functions, Abschnitt "Selected “Known” Functions"
        helferId=helfer.userId,
        statusId=3
    )).scalar()
    
    return render_template('kunde_helfer_profil.html', helfer=helfer, helfer_jobs=helfer_jobs, total_jobs=total_jobs)

@app.route('/kunde/job/<int:job_id>/done', methods=['POST'])
@login_required
def kunde_job_erledigt(job_id):
    if current_user.role != 'kunde':
        logout()
        flash('Zugriff verweigert', 'error')
        return render_template('index.html') 
    
    job = job = db.session.get(Job, job_id)
    real_hours = request.form.get('real_hours')
    
    job.realHours = float(real_hours)
    job.statusId = 3
    db.session.commit()
    flash('Job als erledigt markiert!', 'success')
    return redirect(url_for('kunde'))

@app.route('/logout')
@login_required
def logout():
    logout_user()   #Quelle: Flask-Login, Abschnitt "Login Example"
    flash('Erfolgreich ausgeloggt.', 'info')
    return redirect(url_for('index'))
   

