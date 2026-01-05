from flask import request, jsonify, session
from werkzeug.security import generate_password_hash,check_password_hash
from . import bp
from flaskr.db import get_db
import psycopg2


@bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    if not full_name or not email or not password:
        return jsonify({"error":"missing required fields."}), 400
    
    db = get_db()

    cursor=db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (full_name,email,phone, password)
            values(%s,%s,%s,%s)
            RETURNING id,role
            """,
            (full_name,email,phone,generate_password_hash(password))
        )
        user_id,role=cursor.fetchone()
        db.commit()
    except psycopg2.errors.UniqueViolation:
        db.rollback()
        return jsonify({"error": "Email already exists."})
    
    session["user_id"]= user_id
    session["role"]= role

    return jsonify({"message":"user register successfully.","user_id":user_id}), 201

@bp.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing required fields."}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT id, password, role
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    if user is None:
        return jsonify({"error": "Invalid email or password."}), 401

    user_id, hashed_password, role = user

    if not check_password_hash(hashed_password, password):
        return jsonify({"error": "Invalid email or password."}), 401

    # login success
    session["user_id"] = user_id
    session["role"] = role

    return jsonify({
        "message": "Logged in successfully.",
        "user_id": user_id,
        "role": role
    }), 200
