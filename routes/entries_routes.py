from flask import Blueprint, jsonify, request
from error_handler import handle_error
from models.entries import Entry
from models.extensions import db, entry_schema, entries_schema
from models.habits import Habit

entry_bp = Blueprint('entry_bp', __name__)

@entry_bp.route("/entries", methods=["GET"])
def get_entries():
    entries = Entry.query.options(
        db.joinedload(Entry.habit).joinedload(Habit.user)
    ).all()
    return jsonify(entries_schema.dump(entries))

@entry_bp.route("/entries/<int:entry_id>", methods=["GET"])
def get_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    return jsonify(entry_schema.dump(entry))

@entry_bp.route("/entries", methods=["POST"])
def create_entry():
    try:
        data = entry_schema.load(request.json)
        new_entry = Entry(**data)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(entry_schema.dump(new_entry)), 201
    except Exception as e:
        return handle_error(str(e), 400)

@entry_bp.route("/entries/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    try:
        data = entry_schema.load(request.json)
        for key, value in data.items():
            setattr(entry, key, value)
        db.session.commit()
        return jsonify(entry_schema.dump(entry))
    except Exception as e:
        return handle_error(str(e), 400)

@entry_bp.route("/entries/<int:entry_id>", methods=["PATCH"])
def partial_update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    try:
        data = entry_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(entry, key, value)
        db.session.commit()
        return jsonify(entry_schema.dump(entry))
    except Exception as e:
        return handle_error(str(e), 400)

@entry_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Entry deleted successfully"}), 200