# ==========================================
# 🐍 STUDENT MANAGEMENT SYSTEM - PYTHON BACKEND
# Built with Flask Framework
# ==========================================

# First we import the tools we need
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

# Initialize our Flask app
app = Flask(__name__)
CORS(app)  # This allows our website to talk to Python

# This is where we save all data permanently
DATA_FILE = 'students_database.json'

# ==========================================
# 📂 DATABASE FUNCTIONS
# These functions handle reading and writing data
# ==========================================

def init_database():
    """Create empty database file if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        print("✅ Database file created successfully!")

def get_all_students():
    """Read all students from our database file"""
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_students(students):
    """Save updated student list back to database"""
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=4)

# ==========================================
# 🛣️ API ROUTES (CONNECTS WEBSITE TO PYTHON)
# ==========================================

@app.route('/api/students', methods=['GET'])
def get_students():
    """📤 Send all students to the website"""
    try:
        students = get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """📥 Receive new student data and save it"""
    try:
        # Get data sent from JavaScript
        student_data = request.get_json()
        
        # Create unique ID for the student
        student_data['id'] = str(uuid.uuid4())[:8]
        student_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add to database
        students = get_all_students()
        students.append(student_data)
        save_students(students)

        print(f"✅ Added new student: {student_data['fullName']}")
        return jsonify({"message": "Student added successfully!", "student": student_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/students/<student_id>', methods=['GET'])
def get_single_student(student_id):
    """📤 Send data for ONE specific student"""
    try:
        students = get_all_students()
        student = next((s for s in students if s['id'] == student_id), None)
        
        if student:
            return jsonify(student), 200
        else:
            return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """✏️ Update existing student information"""
    try:
        updated_data = request.get_json()
        students = get_all_students()

        # Find and update the student
        for index, student in enumerate(students):
            if student['id'] == student_id:
                # Keep the original ID and creation date
                updated_data['id'] = student_id
                updated_data['created_at'] = student['created_at']
                students[index] = updated_data
                save_students(students)
                
                print(f"✅ Updated student: {updated_data['fullName']}")
                return jsonify({"message": "Student updated successfully!"}), 200

        return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """❌ Remove student from database"""
    try:
        students = get_all_students()
        original_count = len(students)

        # Keep all students EXCEPT the one to delete
        students = [s for s in students if s['id'] != student_id]
        
        if len(students) < original_count:
            save_students(students)
            print(f"✅ Deleted student ID: {student_id}")
            return jsonify({"message": "Student deleted successfully!"}), 200
        else:
            return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 🚀 START THE SERVER
# ==========================================
if __name__ == '__main__':
    init_database()
    print("=" * 60)
    print("🎓 STUDENT MANAGEMENT SYSTEM SERVER RUNNING!")
    print("🌐 Server Address: http://localhost:5000")
    print("📁 Database File: students_database.json")
    print("=" * 60)
    app.run(debug=True, port=5000)