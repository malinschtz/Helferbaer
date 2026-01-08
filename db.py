import click
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import orm
from app import app

@click.command("init-db")
def init():
    with app.app_context():
        db.drop_all()
        db.create_all()
    click.echo("Database initialized (all tables recreated).")

app.cli.add_command(init)

def insert_sample():

    user1 = User(
            name="Müller",
            firstName="Anna",
            birthday="1961-01-01",
            email="annamüller@gmail.de",
            password="test",
            role="kunde"
        )
    user2 = User(
            name="Fillon",
            firstName="Leonie",
            birthday="2002-07-31",
            email="leoniefillon@gmail.de",
            password="test",
            role="helfer"
        )
    
    category1 = Category(catName="Haushaltsnahe Dienstleistung")
    category2 = Category(catName="Begleitdienste")
    category3 = Category(catName="Betreuung und Gesellschaft")

    status1 = Status(statusName="offen")
    status2 = Status(statusName="gebucht")
    status3 = Status(statusName="erledigt")

    job1 = Job(
        kunde=user1,
        helfer=user2,
        description="Hilfe beim Staubsaugen und Boden wischen",
        date="2026-01-08",
        hours=2,
        categroy=category2,
        status=status2

    )

    db.session.add_all([user1,user2,category1,category2,status1,status2,status3,job1])
    db.session.commit()

@click.command("insert-sample")
def insert_sample_command():
    insert_sample()
    click.echo("Sample data inserted.")

app.cli.add_command(insert_sample_command)

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
        "job",
        foreign_keys="job.kundeId",
        back_populates="kunde"
    )

    jobs_taken = db.relationship(
        "job",
        foreign_keys="job.helferId",
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
    uploaded = db.Column(db.DateTime, nullable=False, default=db.func.now())
    catId = db.Column(db.Integer, db.ForeignKey("category.catId"))
    statusId = db.Column(db.Integer, db.ForeignKey("status.statusId"))
    isTemplate = db.Column(db.Boolean, default=False)
    hours = db.Column(db.Float, nullable=False)
    helferId = db.Column(db.Integer, db.ForeignKey("user.userId"))
    realHours = db.Column(db.Float, default=None)
    
    kunde = db.relationship(
        "user",
        foreign_keys=[kundeId],
        back_populates="jobs_created"
    )

    helfer = db.relationship(
        "user",
        foreign_keys=[helferId],
        back_populates="jobs_taken"
    )

with app.app_context(): db.create_all()