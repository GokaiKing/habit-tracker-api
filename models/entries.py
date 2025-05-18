from .database import db

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float)
    
    habit = db.relationship('Habit', back_populates='entries')
    
    def __repr__(self):
        return f'<Entry {self.date} - {self.value}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'date': self.date.isoformat(),
            'value': self.value
        }