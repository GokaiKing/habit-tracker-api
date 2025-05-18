from .database import db
from enum import Enum

class Frequency(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    name = db.Column(db.String(200), nullable = False)
    frequency = db.Column(db.Enum(Frequency, values_callable=lambda x: [e.value for e in Frequency]), nullable=False)
    target = db.Column(db.String(100))

    user = db.relationship('User', back_populates='habits')
    entries = db.relationship('Entry', back_populates='habit', cascade='all, delete-orphan') 

    def __repr__(self):
        return f'<Habit {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'frequency': self.frequency.value,
            'target': self.target
        }
