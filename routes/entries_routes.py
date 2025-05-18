from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from error_handler import handle_error
from models.entries import Entry
from sqlalchemy.exc import SQLAlchemyError
from models.extensions import db, entry_schema, entries_schema
from models.habits import Habit
from models.schemas import EntrySchema

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
    if not entry:
        return jsonify({'error': 'entry not found'}), 404
    return jsonify(entry_schema.dump(entry))

@entry_bp.route("/entries", methods=["POST"])
def create_entry():
    try:
        new_entry = entry_schema.load(request.json, session=db.session)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify(entry_schema.dump(new_entry)), 201
    except Exception as e:
        return handle_error(str(e), 400)

@entry_bp.route("/entries/<int:entry_id>", methods=["PUT"])
def update_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    try:
        schema = EntrySchema(session=db.session)
        updated_entry = schema.load(request.json, instance=entry)
        db.session.commit()
        return jsonify(schema.dump(updated_entry)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)

@entry_bp.route("/entries/<int:entry_id>", methods=["PATCH"])
def patch_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    try:
        schema = EntrySchema(session=db.session)
        updated_entry = schema.load(request.json, instance=entry, partial=True)
        db.session.commit()
        return jsonify(schema.dump(updated_entry)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)

@entry_bp.route("/entries/<int:entry_id>", methods=["DELETE"])
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Entry deleted successfully"}), 200