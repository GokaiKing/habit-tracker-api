from flask import Blueprint, jsonify, request
from error_handler import handle_error
from models.habits import Habit
from models.extensions import db, habit_schema, habits_schema

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
    return jsonify(habit_schema.dump(habit))

@habit_bp.route("/habits", methods=["POST"])
def create_habit():
    try:
        data = habit_schema.load(request.json)
        new_habit = Habit(**data)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify(habit_schema.dump(new_habit)), 201
    except Exception as e:
        return handle_error(str(e), 400)

@habit_bp.route("/habits/<int:habit_id>", methods=["PUT"])
def update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    try:
        data = habit_schema.load(request.json)
        for key, value in data.items():
            setattr(habit, key, value)
        db.session.commit()
        return jsonify(habit_schema.dump(habit))
    except Exception as e:
        return handle_error(str(e), 400)

@habit_bp.route("/habits/<int:habit_id>", methods=["PATCH"])
def partial_update_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    try:
        data = habit_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(habit, key, value)
        db.session.commit()
        return jsonify(habit_schema.dump(habit))
    except Exception as e:
        return handle_error(str(e), 400)

@habit_bp.route("/habits/<int:habit_id>", methods=["DELETE"])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted successfully"}), 200
