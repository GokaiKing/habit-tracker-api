from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from error_handler import handle_error
from models.schemas import UserSchema
from models.users import User
from sqlalchemy.exc import SQLAlchemyError
from models.extensions import db, user_schema, users_schema

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_schema.dump(user))

@user_bp.route("/users", methods=["POST"])
def create_user():
    try:
        new_user = user_schema.load(request.json, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except Exception as e:
        return handle_error(str(e), 400)
    
@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        schema = UserSchema(session=db.session)
        updated_user = schema.load(request.json, instance=user)
        db.session.commit()
        return jsonify(schema.dump(updated_user)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)

@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        schema = UserSchema(session=db.session)
        updated_user = schema.load(request.json, instance=user, partial=True)
        db.session.commit()
        return jsonify(schema.dump(updated_user)), 200
    except ValidationError as ve:
        return handle_error(ve.messages, 400)
    except SQLAlchemyError as se:
        db.session.rollback()
        return handle_error("Database error: " + str(se), 500)
    except Exception as e:
        db.session.rollback()
        return handle_error("Unexpected error: " + str(e), 500)

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200