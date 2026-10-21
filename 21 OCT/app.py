from flask import Flask,request
from flask import jsonify

app = Flask(__name__)
students=[
                {
                "id": 1,
                "name": "Rhea Kapoor",
                "course": "Python",
                "score": 82
                },
                {
                "id": 2,
                "name": "Zain Malik",
                "course": "SQL",
                "score": 76
                },
                {
                "id": 3,
                "name": "Devika Rao",
                "course": "Cloud",
                "score": 91
                }
            ]

@app.route("/students")
def get_students():

    return jsonify(students)
@app.route("/students/<int:student_id>")
def get_student(student_id):
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)
    return(jsonify({"message": "Student not found"})),404

@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.get_json()

    if not new_student:
        return jsonify({
            "message": "Invalid JSON data"
        }), 400

    # Prevent duplicate student IDs
    if any(s['id'] == new_student.get('id') for s in students):
        return jsonify({
            "message": "Student ID already exists"
        }), 409

    students.append(new_student)

    return jsonify({
        "message": "Student added successfully"
    }), 201
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid JSON data"}), 404
    if any(s['id'] == data['id'] for s in students):
        return jsonify({
            "message": "Student ID already exists"
        })
    students.append(data)
    return jsonify({"message": "Student updated successfully"}), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    for student in students:
        if student['id'] == id:
            students.remove(student)
            return jsonify({
                "message": "Student deleted successfully"
            }), 200

    return jsonify({
        "message": "Student not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
