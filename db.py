import click
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date, timedelta
from flask_bcrypt import Bcrypt
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helferbaer.sqlite' 

bcrypt = Bcrypt(app)
db = SQLAlchemy()
db.init_app(app)


class User(db.Model, UserMixin):    #Quelle UserMixin: Flask-Login, Abschnitt "Your User Class"
    __tablename__ = "user"
    userId = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    registered_date = db.Column(db.Date, default=date.today())

    jobs_created = db.relationship(
        "Job",
    foreign_keys='Job.kundeId',
        back_populates="kunde"
    )

    jobs_taken = db.relationship(
        "Job",
        foreign_keys='Job.helferId',
        back_populates="helfer"
    )

    def get_id(self):   #Quelle: KI Prompt 2
        return str(self.userId)
    
    #lädt Stunden des aktuellen Monats für Stundenkonto Kunde
    @property   #Quelle: KI Promt 3, Python property-Dekorator
    def current_month_hours_kunde(self):
        current_month = date.today().replace(day=1)
        next_month = (current_month + timedelta(days=32)).replace(day=1)        
        jobs = [job for job in self.jobs_created if current_month <= job.date < next_month]
        
        offene = sum(job.hours for job in jobs if job.statusId == 1)
        gebuchte = sum(job.hours for job in jobs if job.statusId == 2)
        erledigte = sum(job.realHours or job.hours for job in jobs if job.statusId == 3)
        
        return {
        'offene': offene,
        'gebuchte': gebuchte, 
        'erledigte': erledigte,
        'gesamt': offene + gebuchte + erledigte
    }

    #lädt Stunden des aktuellen Monats für Stundenkonto Helfer
    @property
    def current_month_hours_helfer(self):
        current_month = date.today().replace(day=1)
        next_month = (current_month + timedelta(days=32)).replace(day=1)        
        jobs = [job for job in self.jobs_taken if current_month <= job.date < next_month]
        
        gebuchte = sum(job.hours for job in jobs if job.statusId == 2)
        erledigte = sum(job.realHours or job.hours for job in jobs if job.statusId == 3)
        
        return {
        'gebuchte': gebuchte, 
        'erledigte': erledigte,
        'gesamt': gebuchte + erledigte
    }

    #angefragte und erledeigte Jobs für Kunden Dashboard
    def get_jobs_by_status_kunde(self):
        jobs = Job.query.filter(
            Job.kundeId == self.userId
        ).order_by(Job.date.desc()).all()
        
        # Trennung: angefragt (offen/gebucht) vs erledigt
        angefragte_jobs = [j for j in jobs if j.statusId in [1,2]] 
        erledigte_jobs = [j for j in jobs if j.statusId == 3] 
        
        return {
            'angefragte_jobs': angefragte_jobs,
            'erledigte_jobs': erledigte_jobs
        }
    
    #angefragte und erledeigte Jobs für Helfer Dashboard
    def get_jobs_by_status_helfer(self):
        jobs = Job.query.filter(
            Job.helferId == self.userId
        ).order_by(Job.date.desc()).all()
        
        # Trennung: gebuchte vs erledigt
        gebuchte_jobs = [j for j in jobs if j.statusId == 2]
        erledigte_jobs = [j for j in jobs if j.statusId == 3] 
        
        return {
            'gebuchte_jobs': gebuchte_jobs,
            'erledigte_jobs': erledigte_jobs
        }
    
    #Stundenkonto für Helfer Dashboard
    @property
    def gesamtArbeitsStunden(self):
        if self.role != 'helfer':
            return 0

        return sum(
            job.realHours or 0
            for job in self.jobs_taken
            if job.statusId == 3  
        )


class Category(db.Model):
    __tablename__ = "category"
    catId = db.Column(db.Integer, primary_key=True, index=True)
    catName = db.Column(db.String, nullable=False, unique=True)

class Status(db.Model):
    __tablename__ = "status"
    statusId = db.Column(db.Integer, primary_key=True, index=True)
    statusName = db.Column(db.String, nullable=False, unique=True)

class Job(db.Model):
    __tablename__ = "job"
    jobId = db.Column(db.Integer, primary_key=True, index=True)
    kundeId = db.Column(db.Integer, db.ForeignKey("user.userId"), nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    street = db.Column(db.String, nullable=False)
    plz = db.Column(db.Integer, nullable=False)
    uploaded = db.Column(db.DateTime, nullable=False, default=db.func.now())
    catId = db.Column(db.Integer, db.ForeignKey("category.catId"))
    statusId = db.Column(db.Integer, db.ForeignKey("status.statusId"))
    isTemplate = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float, nullable=False)
    helferId = db.Column(db.Integer, db.ForeignKey("user.userId"))
    realHours = db.Column(db.Float, default=None)
    
    kunde = db.relationship(
        "User",
        foreign_keys=[kundeId],
        back_populates="jobs_created"
    )

    helfer = db.relationship(
        "User",
        foreign_keys=[helferId],
        back_populates="jobs_taken"
    )

    status = db.relationship('Status', backref='jobs')

@click.command("init-db")
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo("DB initialisiert (Tabellen erstellt)")

@click.command("insert-sample")
def insert_sample():
    with app.app_context():
        cat1 = Category(
            catName = 'Haushaltsnahe Dienstleistungen'
        )
        cat2 = Category(
            catName = 'Begleitdienste'
        )
        cat3 = Category(
            catName = 'Betreuung und Gesellschaft'
        )
        
        stat1 = Status(
            statusName = 'offen'
        )
        stat2 = Status(
            statusName = 'gebucht'
        )
        stat3 = Status(
            statusName = 'erledigt'
        )

        helfer1 = User(
            name = 'Fillon',
            firstName = 'Leonie',
            birthday = date.fromisoformat('2002-08-31'),
            email = 'leoniefillon@gmail.com',
            password = bcrypt.generate_password_hash('12345678').decode('utf-8'),
            phone = '0179 456 762 37',
            role = 'helfer'
        )

        helfer2 = User(
            name = 'Schröder',
            firstName = 'Dennis',
            birthday = date.fromisoformat('2003-09-15'),
            email = 'dennisschröder@gmail.com',
            password = bcrypt.generate_password_hash('12345678').decode('utf-8'),
            phone = '0177 123 456 78',
            role = 'helfer'
        )

        kunde1 = User(
            name = 'Steini',
            firstName = 'Silvia',
            birthday = date.fromisoformat('1948-12-12'),
            email = 'silviasteini@gmail.com',
            password = bcrypt.generate_password_hash('12345678').decode('utf-8'),
            phone = '0177 987 654 32',
            role = 'kunde'
        )

        kunde2 = User(
            name = 'Henne',
            firstName = 'Hilda',
            birthday = date.fromisoformat('1946-06-01'),
            email = 'hildahenne@gmail.com',
            password = bcrypt.generate_password_hash('12345678').decode('utf-8'),
            phone = '0152 456 321 87',
            role = 'kunde'
        ) 

        job1 = Job(
            kundeId = 3,
            description = 'Autofahrt/Begleitung zum Arzttermin um 14 Uhr',
            date = date.fromisoformat('2026-01-29'),
            street = 'Musterstr. 123',
            plz = 14195,
            catId = 2,
            statusId = 1,
            hours = 2
        )

        job2 = Job(
            kundeId = 3,
            description = 'Wäsche waschen und aufhängen + Einkaufen',
            date = date.fromisoformat('2026-01-14'),
            street = 'Musterstr. 123',
            plz = 14195,
            catId = 1,
            statusId = 3,
            hours = 2.5,
            helferId = 1,
            realHours = 2.5
        )

        job3 = Job(
            kundeId = 3,
            description = 'Gartenarbeiten',
            date = date.fromisoformat('2026-01-23'),
            street = 'Musterstr. 123',
            plz = 14195,
            catId = 1,
            statusId = 2,
            hours = 2,
            helferId = 2
        )

        job4 = Job(
            kundeId = 4,
            description = 'Kochen helfen + gemeinsam Abendessen',
            date = date.fromisoformat('2026-01-23'),
            street = 'Beispielstr. 321',
            plz = 14195,
            catId = 3,
            statusId = 2,
            hours = 2,
            helferId = 1
        )

        job5 = Job(
            kundeId = 4,
            description = 'Neuen Schrank aufbauen',
            date = date.fromisoformat('2026-01-24'),
            street = 'Beispielstr. 321',
            plz = 14195,
            catId = 1,
            statusId = 1,
            hours = 2
        )       

        job6 = Job(
            kundeId = 3,
            description = 'Keller entrümpeln',
            date = date.fromisoformat('2026-01-25'),
            street = 'Musterstr. 123',
            plz = 14195,
            catId = 1,
            statusId = 2,
            hours = 2,
            helferId = 2
        )

        db.session.add_all([cat1, cat2, cat3, stat1, stat2, stat3, helfer1, helfer2, kunde1, kunde2, job1, job2, job3, job4, job5, job6])
        db.session.commit()
    click.echo("Sample-Daten eingefügt")

@click.command("delete-job")
def delete():
    with app.app_context():
        job = Job.query.get(7)
        db.session.delete(job)
        db.session.commit()
    click.echo("Daten gelöscht")

app.cli.add_command(init_db)
app.cli.add_command(insert_sample)
app.cli.add_command(delete)


