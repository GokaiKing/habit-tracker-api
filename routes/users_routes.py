from flask import Blueprint, jsonify, request
from error_handler import handle_error
from models.users import User
from models.extensions import db, user_schema, users_schema

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))

@user_bp.route("/users", methods=["POST"])
def create_user():
    try:
        data = user_schema.load(request.json)
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except Exception as e:
        return handle_error(str(e), 400)

@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        data = user_schema.load(request.json)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user_schema.dump(user))
    except Exception as e:
        return handle_error(str(e), 400)

@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def partial_update_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        data = user_schema.load(request.json, partial=True)
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user_schema.dump(user))
    except Exception as e:
        return handle_error(str(e), 400)

@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200