from marshmallow import ValidationError, fields, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_enum import EnumField
from .database import db

# Importa los modelos al final del archivo para evitar circularidad
from .users import User
from .habits import Habit, Frequency
from .entries import Entry

class EntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entry
        include_fk = True
        load_instance = True
    
    habit = fields.Nested(lambda: HabitSchema(exclude=('entries',)))

class HabitSchema(SQLAlchemyAutoSchema):
    frequency = EnumField(Frequency, by_value=True)
    class Meta:
        model = Habit
        include_fk = True
        load_instance = True
    
    user = fields.Nested(lambda: UserSchema(only=('id', 'name')))
    entries = fields.Nested(lambda: EntrySchema(many=True, exclude=('habit',)))

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
    
    habits = fields.Nested(lambda: HabitSchema(many=True, exclude=('user',)))

'''
from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .database import db
from marshmallow_enum import EnumField 
from .habits import Frequency
from .users import User  # Importación directa
from .habits import Habit  # Importación directa
from .entries import Entry  # Importación directa

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User  # Usa la clase directamente, no string
        load_instance = True
        sqla_session = db.session
    
    email = fields.Email(required=True)
    habits = fields.Nested(lambda: HabitSchema, many=True, exclude=('user',), dump_only=True)  # Usa lambda

class HabitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Habit  # Clase directa
        load_instance = True
        sqla_session = db.session
    
    frequency = EnumField(Frequency, by_value=True)
    user = fields.Nested(lambda: UserSchema, exclude=('habits',), dump_only=True)  # Lambda
    entries = fields.Nested(lambda: EntrySchema, many=True, exclude=('habit',), dump_only=True)  # Lambda

class EntrySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Entry  # Clase directa
        load_instance = True
        include_relationships = True
        sqla_session = db.session
    
    #habit = fields.Nested(lambda: HabitSchema, exclude=('entries',), dump_only=True)  # Lambda
    habit = fields.Nested('HabitSchema', exclude=('entries',))
    date = fields.Date(format='%Y-%m-%d')
    '''