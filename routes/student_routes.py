from flask import Blueprint, request, jsonify
from models import db, Student, Department
from flask_jwt_extended import jwt_required , get_jwt
from utils.decorators import admin_required
from schemas.student_schema import StudentSchema

student_bp = Blueprint(
    'student_bp',
    __name__,
    url_prefix='/api/v1'
)

# ---------------------------
# BULK ADD STUDENTS
# ---------------------------
@student_bp.route('/students/fill', methods=['POST'])
@jwt_required()
def add_students():
    """
    Add Students
    ---
    tags:
      - Students

    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: array
          items:
            properties:
              name:
                type: string
                example: Rahul

              email:
                type: string
                example: rahul@gmail.com

              department_id:
                type: integer
                example: 1

    responses:
      201:
        description: Students added successfully
    """

    data = request.get_json()
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    if not isinstance(data, list):
        return jsonify({"message": "Input must be a list of students"}), 400

    schema = StudentSchema(many=True)
    errors = schema.validate(data)
    if errors:
        return jsonify(errors),400

    

    
    students = []
    emails_seen = set()

    # required_fields = ["name", "email", "department_id"]

    for item in data:

        if not isinstance(item, dict):
            return jsonify({"message": "Each student must be a JSON object"}), 400

        # for field in required_fields:
        #     if field not in item or not item[field]:
        #         return jsonify({
        #             "message": f"{field} is required for one of the students"
        #         }), 400
        ## done by marshmallow

        if item["email"] in emails_seen:
            return jsonify({
                "message": f"Duplicate email in request: {item['email']}"
            }), 400

        emails_seen.add(item["email"])

        existing = Student.query.filter_by(email=item["email"]).first()

        if existing:
            return jsonify({
                "message": f"Email already exists in database: {item['email']}"
            }), 409

        department = Department.query.get(item["department_id"])

        if not department:
            return jsonify({
                "message": f"Department not found: {item['department_id']}"
            }), 404

        student = Student(
            name=item["name"],
            email=item["email"],
            department_id=item["department_id"]
        )

        students.append(student)

    db.session.add_all(students)
    db.session.commit()

    return jsonify({
        "message": f"{len(students)} students added successfully"
    }), 201


# ---------------------------
# GET ALL STUDENTS
# ---------------------------
@student_bp.route('/students/detail')
@jwt_required()
def student_detail():
    """
    Get Students
    ---
    tags:
      - Students

    parameters:
      - name: page
        in: query
        type: integer
        example: 1

      - name: limit
        in: query
        type: integer
        example: 5

      - name: department
        in: query
        type: string
        example: IT

      - name: sort
        in: query
        type: string
        example: name

    responses:
      200:
        description: List of students
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)
    ##sorting parameter
    sort = request.args.get('sort')
    ##filtering parameter
    department = request.args.get('department')
    
    ## start query
    query = Student.query
    ## Department filter
    if department:
     query = query.join(Department).filter(
        Department.name.ilike(f'%{department}%')
    )
    ##sorting
    if sort == "name":
        query = query.order_by(Student.name)

    elif sort == "id":
        query = query.order_by(Student.id)    

    students = query.paginate(
        page=page,
        per_page=limit,
        error_out=False
    )
##here students is a pagination objexct  also return the fillowing properties
##students.page        # current page number
##students.total       # total records
##students.per_page    # records per page
##students.pages       # total pages
##students.items       # records of current page
##students.has_next    # True/False
##students.has_prev    # True/False
##students.next_num    # next page number
##students.prev_num    # previous page number
    result = []

    for student in students.items:

        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "department": {
                "id": student.department.id,
                "name": student.department.name
            }
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total_students": students.total,
        "total_pages": students.pages,
        "students": result
    })
##http://127.0.0.1:5000/api/v1/students/detail?page=1&limit=2
# ---------------------------
# SEARCH BY NAME
# ---------------------------
@student_bp.route('/students/search', methods=['GET'])
@jwt_required()
def search_student_name():
    """
    Search Student By Name
    ---
    tags:
      - Students

    parameters:
      - name: name
        in: query
        type: string
        example: Rahul

    responses:
      200:
        description: Matching students
    """

    name = request.args.get('name')

    students = Student.query.filter(
        Student.name.ilike(f'%{name}%')
    ).all()

    result = []

    for student in students:
        result.append({
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "department": {
                "id": student.department.id,
                "name": student.department.name
            }
        })

    return jsonify(result)


# ---------------------------
# SEARCH BY ID
# ---------------------------
@student_bp.route('/students/search/ids', methods=['GET'])
@jwt_required()
def search_student():
    """
    Search Student By ID
    ---
    tags:
      - Students

    parameters:
      - name: id
        in: query
        type: integer
        example: 1

    responses:
      200:
        description: Student found

      404:
        description: Student not found
    """

    student_id = request.args.get('id')

    student = Student.query.filter_by(id=student_id).first()

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "department": {
            "id": student.department.id,
            "name": student.department.name
        }
    }), 200


# ---------------------------
# DELETE STUDENT
# ---------------------------
@student_bp.route('/students/delete/<int:id>', methods=['DELETE'])
@admin_required
def delete_student(id):
    """
    Delete Student
    ---
    tags:
      - Students

    parameters:
      - name: id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Student deleted

      404:
        description: Student not found
    """
    claims = get_jwt()

    if claims["role"] != "admin":
       return jsonify({
        "message": "Admin access required"
    }), 403

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "message": "Student Not Found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student Deleted Successfully"
    })


# ---------------------------
# UPDATE STUDENT
# ---------------------------
@student_bp.route('/students/<int:id>', methods=['PUT'])
@jwt_required()
def update_student(id):
    """
    Update Student
    ---
    tags:
      - Students

    parameters:
      - name: id
        in: path
        type: integer
        required: true

      - in: body
        name: body
        schema:
          properties:
            name:
              type: string

            email:
              type: string

            department_id:
              type: integer

    responses:
      200:
        description: Student updated
    """

    student = Student.query.get(id)

    if not student:
        return jsonify({
            "message": "Student Not Found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No input data provided"
        }), 400

    if "name" in data:
        student.name = data["name"]

    if "department_id" in data:

        department = Department.query.get(data["department_id"])

        if not department:
            return jsonify({
                "message": "Department not found"
            }), 404

        student.department_id = data["department_id"]

    if "email" in data:

        existing = Student.query.filter_by(
            email=data["email"]
        ).first()

        if existing and existing.id != id:
            return jsonify({
                "message": "Email already exists"
            }), 409

        student.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "Student Updated Successfully"
    })