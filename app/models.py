from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    organization = db.Column(db.String(128))  # Association ou RPE
    training_preference = db.Column(db.String(20))  # presentiel, distance, e-learning
    schedule_preference = db.Column(db.String(20))  # semaine, samedi, both
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Formation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iperia_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)  # en heures
    trainers = db.Column(db.String(500))  # Liste des formateurs séparés par des virgules
    program_link = db.Column(db.String(500))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(200))

class TrainingAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formation_id = db.Column(db.Integer, db.ForeignKey('formation.id'), nullable=False)
    location = db.Column(db.String(200))
    trainers = db.Column(db.String(500))
    start_date = db.Column(db.DateTime)
    formation = db.relationship('Formation', backref='actions')

class TrainingWish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    formation_id = db.Column(db.Integer, db.ForeignKey('formation.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='training_wishes')
    formation = db.relationship('Formation')

class CompletedTraining(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    formation_id = db.Column(db.Integer, db.ForeignKey('formation.id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='completed_trainings')
    formation = db.relationship('Formation')

class TrainingParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training_action_id = db.Column(db.Integer, db.ForeignKey('training_action.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    training_action = db.relationship('TrainingAction', backref='participants')
    user = db.relationship('User')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
