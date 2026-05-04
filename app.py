# ==========================================
# 🐍 STUDENT MANAGEMENT SYSTEM - PYTHON BACKEND
# Built with Flask Framework
# Upgraded Version - Works Locally + Online (Render)
# ==========================================

# First we import the tools we need
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

# Initialize our Flask app
app = Flask(__name__)
CORS(app)  # This allows our website to talk to Python - CRITICAL!

# ✅ FIXED: This finds the exact folder no matter where it runs
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIRECTORY, 'students_database.json')

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
    print(f"📂 Database location: {DATA_FILE}")

def get_all_students():
    """Read all students from our database file"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error reading database: {str(e)}")
        return []

def save_students(students):
    """Save updated student list back to database"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(students, f, indent=4)
        return True
    except Exception as e:
        print(f"⚠️ Error saving database: {str(e)}")
        return False

# ==========================================
# 📂 SERVE WEBSITE FILES - FIXED FOR RENDER
# THIS IS WHAT SOLVES THE "NOT FOUND" ERROR!
# ==========================================

@app.route('/')
def serve_home():
    """Send your main website page"""
    try:
        index_path = os.path.join(BASE_DIRECTORY, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(BASE_DIRECTORY, 'index.html')
        else:
            return f"❌ ERROR: index.html NOT FOUND! Looking in: {BASE_DIRECTORY}", 404
    except Exception as e:
        return f"❌ ERROR loading page: {str(e)}", 500

@app.route('/<path:filename>')
def serve_files(filename):
    """Send CSS, JS, images, logo and all other files"""
    try:
        file_path = os.path.join(BASE_DIRECTORY, filename)
        if os.path.exists(file_path):
            return send_from_directory(BASE_DIRECTORY, filename)
        else:
            print(f"⚠️ File missing: {filename} | Path checked: {file_path}")
            return f"❌ File not found: {filename}", 404
    except Exception as e:
        print(f"⚠️ Error loading {filename}: {str(e)}")
        return f"❌ Error: {str(e)}", 500

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
        
        if save_students(students):
            print(f"✅ Added new student: {student_data['fullName']}")
            return jsonify({"message": "Student added successfully!", "student": student_data}), 201
        else:
            return jsonify({"error": "Failed to save to database"}), 500

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
                
                if save_students(students):
                    print(f"✅ Updated student: {updated_data['fullName']}")
                    return jsonify({"message": "Student updated successfully!"}), 200
                else:
                    return jsonify({"error": "Failed to save updates"}), 500

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
            if save_students(students):
                print(f"✅ Deleted student ID: {student_id}")
                return jsonify({"message": "Student deleted successfully!"}), 200
            else:
                return jsonify({"error": "Failed to save changes"}), 500
        else:
            return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 🚀 START THE SERVER - WORKS EVERYWHERE!
# ==========================================
if __name__ == '__main__':
    init_database()
    print("=" * 60)
    print("🎓 STUDENT MANAGEMENT SYSTEM SERVER RUNNING!")
    print(f"🌐 Working Directory: {BASE_DIRECTORY}")
    print(f"📁 Database File: {DATA_FILE}")
    print("=" * 60)
    
    # This works both on your computer AND on Render
    app.run(debug=False, host='0.0.0.0', port=5000)