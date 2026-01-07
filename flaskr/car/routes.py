from . import bp
import psycopg2
from flaskr.db import get_db
from flask import request, jsonify, session

@bp.route("register", methods=["POST"])
def register_car():
    data = request.get_json()

    make = data.get("make")
    model = data.get("model")
    manufacture_year = data.get("manufacture_year")
    vin = data.get("vin")
    license_plate = data.get("license_plate")
    vehicle_type_id = data.get("vehicle_type_id")

    user_id = session.get("user_id")

    if not model or not license_plate:
        return jsonify({"message":"missing required field"}),
    
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO vehicles (user_id,model,make,manufacture_year,vin,license_plate,vehicle_type_id)
            values(%s,%s,%s,%s,%s,%s,%s)
            RETURNING ID
            """,
            (user_id,model,make,manufacture_year,vin,license_plate,vehicle_type_id)
        )
        vehicle_id = cursor.fetchone()[0]
        db.commit()
    except psycopg2.errors.UniqueViolation:
        db.rollback()
        return jsonify({"message":"license or vin may already exist"}), 409
    
    return jsonify({
        "message": "car registered sucessfully",
        "vehicle_id": vehicle_id,
        "status":"padding"
    })
    
    


    