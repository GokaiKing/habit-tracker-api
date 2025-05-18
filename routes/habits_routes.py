from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from error_handler import handle_error
from sqlalchemy.exc import SQLAlchemyError
from models.habits import Habit
from models.extensions import db, habit_schema, habits_schema
from models.schemas import HabitSchema

habit_bp = Blueprint('habit_bp', __name__)

@habit_bp.route("/habits", methods=["GET"])
def get_habits():
    habits = Habit.query.options(
        db.joinedload(Habit.user),
        db.joinedload(Habit.entries)
    ).all()
    return jsonify(habits_schema.dump(habits))

@habit_bp.route("/habits/<int:habit_id>", methods=["GET"])
def get_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    if not habit:
        return jsonify({'error': 'Habit not found'}), 404
    return jsonify(habit_schema.dump(habit))

@habit_bp.route("/habits", methods=["POST"])
def create_habit():
    try:
        new_habit = habit_schema.load(request.json, session=db.session)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify(habit_schema.dump(new_habit)), 201
    except Exception as e:
        return handle_error(str(e), 400)
    
@habit_bp.route("/habits/<int:habit_id>", methods=["PUT"])
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    try:
        schema = HabitSchema(session=db.session)
        updated_habit = schema.load(request.json, instance=habit)
        db.session.commit()
        return jsonify(schema.dump(updated_habit)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)


@habit_bp.route("/habits/<int:habit_id>", methods=["PATCH"])
def patch_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    try:
        schema = HabitSchema(session=db.session)
        updated_habit = schema.load(request.json, instance=habit, partial=True)
        db.session.commit()
        return jsonify(schema.dump(updated_habit)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)


@habit_bp.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted successfully"}), 200
