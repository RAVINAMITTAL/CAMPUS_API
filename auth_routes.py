from flask import Blueprint, request, jsonify
from models import db, User,TokenBlocklist
from  flask_jwt_extended import (create_access_token , jwt_required , get_jwt_identity,get_jwt,create_refresh_token)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import logging
from extensions import limiter
from schemas.user_schema import RegisterSchema
from schemas.user_schema import LoginSchema

auth_bp = Blueprint(
    "auth_bp",
    __name__
)
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User Registration
    ---
    tags:
      - Authentication


    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            username:
              type: string
              example: ravina

            password:
              type: string
              example: password123

    responses:
      201:
        description: User registered successfully

      409:
        description: Username already exists
    """

    data = request.get_json()
    if not data:
        return jsonify({
            "message": "No input data provided"
        }), 400
    schema = RegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors),400


    

    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "student")

    # if not username or not password:
    #     return jsonify({
    #         "message": "Username and password required"
    #     }), 400
   ## as marshmallow will see it
    existing = User.query.filter_by(
        username=username
    ).first()

    if existing:
        return jsonify({
            "message": "User already exists"
        }), 409

    hashed_password = generate_password_hash(password)

    user = User(
    username=username,
    password=hashed_password,
    role=role
)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully"
    }), 201

##login api
@auth_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """
User Login
---
tags:
  - Authentication

parameters:
  - in: body
    name: body
    required: true
    schema:
      properties:
        username:
          type: string
          example: admin

        password:
          type: string
          example: admin123

responses:
  200:
    description: Login successful

  401:
    description: Invalid credentials
"""

    data = request.get_json()
    if not data:
        return jsonify({
            "message": "No input data provided"
        }), 400
    schema = LoginSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors),400

    

    username = data.get("username")
    password = data.get("password")

    # if not username or not password:
    #     return jsonify({
    #         "message": "Username and password required"
    #     }), 400
    ##marshmallow will see it

    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return jsonify({
            "message": "Invalid username or password"
        }), 401

    if not check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "message": "Invalid username or password"
        }), 401

    access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "role": user.role
    }
)
    refresh_token = create_refresh_token(
    identity=str(user.id)
 )
    logging.info(
    f"User {user.username} logged in"
)
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200

##get profile 
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    User Profile
    ---
    tags:
      - Authentication

    security:
      - Bearer: []

    responses:
      200:
        description: User profile retrieved successfully

      401:
        description: Invalid or expired token
    """

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "role":user.role
    }), 200



###refresh api

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh Access Token
    ---
    tags:
      - Authentication

    security:
      - Bearer: []

    responses:
      200:
        description: New access token generated successfully

      401:
        description: Invalid refresh token
    """

    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "access_token": new_access_token
    }), 200

##logout api
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
Logout User
---
tags:
  - Authentication

security:
  - Bearer: []

responses:
  200:
    description: User logged out successfully
"""

    jti = get_jwt()["jti"]

    blocked_token = TokenBlocklist(
        jti=jti
    )

    db.session.add(blocked_token)
    db.session.commit()
    logging.info(f"User {get_jwt_identity()} logged out")

    return jsonify({
        "message": "Logged out successfully"
    }), 200


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
Change Password
---
tags:
  - Authentication

security:
  - Bearer: []

parameters:
  - in: body
    name: body
    required: true
    schema:
      properties:
        old_password:
          type: string
          example: admin123

        new_password:
          type: string
          example: newpassword123

responses:
  200:
    description: Password changed successfully

  400:
    description: Old password is incorrect

  401:
    description: Unauthorized
"""

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No input data provided"
        }), 400

    if "old_password" not in data:
        return jsonify({
            "message": "old_password is required"
        }), 400

    if "new_password" not in data:
        return jsonify({
            "message": "new_password is required"
        }), 400

    if not check_password_hash(
        user.password,
        data["old_password"]
    ):
        return jsonify({
            "message": "Old password incorrect"
        }), 400

    user.password = generate_password_hash(
        data["new_password"]
    )

    db.session.commit()
    logging.info(
    f"User {user.username} changed password"
)
    return jsonify({
        "message": "Password changed successfully"
    }), 200