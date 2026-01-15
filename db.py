import click
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import orm
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///helferbaer.sqlite' 

db = SQLAlchemy()
db.init_app(app)
 
class User(db.Model):
    __tablename__ = "user"
    userId = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    role = db.Column(db.String, nullable=False)

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


@click.command("init-db")
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo("DB initialisiert (Tabellen erstellt)")

@click.command("insert-sample")
def insert_sample():
    with app.app_context():
        # Sample-Daten 
        db.session.add_all(['sample'])
        db.session.commit()
    click.echo("Sample-Daten eingefügt")

app.cli.add_command(init_db)
app.cli.add_command(insert_sample)

