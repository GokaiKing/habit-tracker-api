from flask import Flask
from datetime import datetime
from sqlalchemy import inspect
from models.database import db
from models.habits import Frequency
from routes.users_routes import user_bp
from routes.habits_routes import habit_bp
from routes.entries_routes import entry_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(habit_bp, url_prefix='/api')
app.register_blueprint(entry_bp, url_prefix='/api')


# def needs_frequency_migration():
#     print('EJECUTADO NFM')
#     """Verifica si es necesaria la migración"""
#     from sqlalchemy import inspect
#     inspector = inspect(db.engine)
    
#     # Verificar si la columna frequency existe y su tipo
#     if 'habits' in inspector.get_table_names():
#         columns = inspector.get_columns('habits')
#         for col in columns:
#             if col['name'] == 'frequency':
#                 return isinstance(col['type'], db.String)  # True si es string
    
#     return False

# def migrate_frequency_values():
#     print('EJECUTADO MFV')
#     """Migración segura de valores de frecuencia"""
#     if not needs_frequency_migration():
#         return  # No necesita migración
        
#     from models.habits import Habit
#     from sqlalchemy import text
    
#     try:
#         # 1. Crear tabla temporal con la nueva estructura
#         with db.engine.connect() as connection:
#             # Verificar si old_habits ya existe
#             inspector = inspect(db.engine)
#             if 'old_habits' in inspector.get_table_names():
#                 connection.execute(text("DROP TABLE old_habits"))
                
#             connection.execute(text("PRAGMA foreign_keys=OFF"))
#             connection.execute(text("ALTER TABLE habits RENAME TO old_habits"))
#             connection.execute(text("""
#                 CREATE TABLE habits (
#                     id INTEGER PRIMARY KEY,
#                     user_id INTEGER,
#                     name TEXT,
#                     frequency TEXT CHECK(frequency IN ('daily', 'weekly', 'monthly')),
#                     target TEXT,
#                     FOREIGN KEY(user_id) REFERENCES users(id)
#                 )
#             """))
#             connection.execute(text("""
#                 INSERT INTO habits (id, user_id, name, frequency, target)
#                 SELECT id, user_id, name, frequency, target FROM old_habits
#             """))
#             connection.execute(text("DROP TABLE old_habits"))
#             connection.execute(text("PRAGMA foreign_keys=ON"))
        
#         # 2. Actualizar a valores Enum
#         habits = Habit.query.all()
#         for habit in habits:
#             if isinstance(habit.frequency, str):
#                 if habit.frequency == 'daily':
#                     habit.frequency = Frequency.DAILY
#                 elif habit.frequency == 'weekly':
#                     habit.frequency = Frequency.WEEKLY
#                 elif habit.frequency == 'monthly':
#                     habit.frequency = Frequency.MONTHLY
#         db.session.commit()
        
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error durante migración: {e}")
#         raise

@app.before_request
def initialize_data():
    with app.app_context():
        db.create_all()
        
        # Solo ejecutar migración si es necesario
        # if needs_frequency_migration():
        #    migrate_frequency_values()
        
        from models.users import User
        from models.habits import Habit
        from models.entries import Entry
        
        if User.query.count() == 0:
            sample_user = User(
                name="Abelardo Flores",
                email="aflooSWE@gmail.com"
            )
            db.session.add(sample_user)
            db.session.commit()
            
            sample_habit = Habit(
                user_id=sample_user.id,
                name="leetcode practice",
                frequency=Frequency.DAILY,
                target="1 hour"
            )
            db.session.add(sample_habit)
            db.session.commit()
            
            sample_entry = Entry(
                habit_id=sample_habit.id,
                date=datetime.today(),
                value=1.0  
            )
            db.session.add(sample_entry)
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)