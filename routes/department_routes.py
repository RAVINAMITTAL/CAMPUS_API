from flask import Blueprint, request, jsonify
from models import db, Department
from flask_jwt_extended import jwt_required , get_jwt

department_bp = Blueprint(
    'department_bp',
    __name__,
    url_prefix='/api/v1'
)
###for department make a seperate apis 

@department_bp.route('/departments/bulk', methods=['POST'])
@jwt_required()
def add_departments():
    claims = get_jwt()

    if claims["role"] != "admin":
      return jsonify({
        "message": "Admin access required"
    }), 403

    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    if not isinstance(data, list):
        return jsonify({"message": "Input must be a list"}), 400

    departments = []

    for item in data:

        if "name" not in item or not item["name"]:
            return jsonify({"message": "Department name is required"}), 400

        # duplicate check inside DB
        existing = Department.query.filter_by(name=item["name"]).first()
        if existing:
            return jsonify({
                "message": f"Department already exists: {item['name']}"
            }), 409

        dept = Department(name=item["name"])
        departments.append(dept)

    db.session.add_all(departments)
    db.session.commit()

    return jsonify({
        "message": f"{len(departments)} departments created successfully"
    }), 201

@department_bp.route('/departments/fills', methods=['GET'])
def get_departments():
    """
    Get Departments
    ---
    tags:
      - Departments

    responses:
      200:
        description: List of departments
    """
    departments = Department.query.all()

    result = []

    for d in departments:
        result.append({
            "id": d.id,
            "name": d.name
        })

    return jsonify(result)

@department_bp.route('/departments/<int:id>/students', methods=['GET'])
def get_department_students(id):
    """
    Get Students Of Department
    ---
    tags:
      - Departments

    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Students in department

      404:
        description: Department not found
    """
    department = Department.query.get(id)

    if not department:
        return jsonify({"message": "Department not found"}), 404

    students_list = []

    for student in department.students:
        students_list.append({
            "id": student.id,
            "name": student.name,
            "email": student.email
        })

    return jsonify({
        "department": department.name,
        "students": students_list
    })