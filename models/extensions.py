from .database import db
from .schemas import UserSchema, HabitSchema, EntrySchema

# Inicializar esquemas después de que todos los modelos estén cargados
user_schema = UserSchema()
users_schema = UserSchema(many=True)
habit_schema = HabitSchema()
habits_schema = HabitSchema(many=True)
entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)