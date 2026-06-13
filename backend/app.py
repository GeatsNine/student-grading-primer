from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

# Helper function:
def error_response(message):
    return jsonify({"error": message}), 404


def parse_mark(mark, default=0):
    """
    Convert mark to int and validate it.
    Missing mark defaults to 0.
    Valid mark range: 0 to 100.
    """
    if mark is None:
        return default

    try:
        mark = int(mark)
    except (TypeError, ValueError):
        return None

    if mark < 0 or mark > 100:
        return None

    return mark


# Main function:
@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200



@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    student_data = request.get_json(silent=True)

    if not isinstance(student_data, dict):
        return error_response("Invalid JSON body")

    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark", 0)

    if not isinstance(name, str) or name.strip() == "":
        return error_response("Name is required")

    if not isinstance(course, str) or course.strip() == "":
        return error_response("Course is required")

    parsed_mark = parse_mark(mark)

    if parsed_mark is None:
        return error_response("Mark must be an integer between 0 and 100")

    created_student = db.insert_student(name.strip(), course.strip(), parsed_mark)
    return jsonify(created_student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    existing_student = db.get_student_by_id(student_id)

    if existing_student is None:
        return error_response("Student not found")

    student_data = request.get_json(silent=True)

    if not isinstance(student_data, dict):
        return error_response("Invalid JSON body")

    name = student_data.get("name", None)
    course = student_data.get("course", None)
    mark = student_data.get("mark", None)

    if name is not None:
        if not isinstance(name, str) or name.strip() == "":
            return error_response("Name cannot be empty")
        name = name.strip()

    if course is not None:
        if not isinstance(course, str) or course.strip() == "":
            return error_response("Course cannot be empty")
        course = course.strip()

    if mark is not None:
        mark = parse_mark(mark)
        if mark is None:
            return error_response("Mark must be an integer between 0 and 100")

    updated_student = db.update_student(
        student_id,
        name=name,
        course=course,
        mark=mark,
    )

    if updated_student is None:
        return error_response("Student not found")

    return jsonify(updated_student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted_student = db.delete_student(student_id)

    if deleted_student is None:
        return error_response("Student not found")

    return jsonify(deleted_student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [student["mark"] for student in students if student["mark"] is not None]

    if len(marks) == 0:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None,
        }), 200

    stats = {
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }

    return jsonify(stats), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
