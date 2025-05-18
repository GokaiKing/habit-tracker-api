from .database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    registration_date = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    
    habits = db.relationship('Habit', back_populates='user')

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "registration_date": self.registration_date.isoformat()
        }