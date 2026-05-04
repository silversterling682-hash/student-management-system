

# ==========================================
# 🎓 STUDENT MANAGEMENT SYSTEM - BACKEND
# Built by: silversterling682-hash
# ==========================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

# Initialize app
app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

# ✅ IMPORTANT: This tells Flask where your files are
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIRECTORY, "students_database.json")

# --------------------------
# 📂 SERVE WEBSITE FILES
# --------------------------
@app.route('/')
def serve_home():
    """Send your main website page"""
    return send_from_directory(BASE_DIRECTORY, 'index.html')

@app.route('/<path:filename>')
def serve_files(filename):
    """Send CSS, JS, images and other files"""
    return send_from_directory(BASE_DIRECTORY, filename)

# --------------------------
# 📊 DATABASE FUNCTIONS
# --------------------------
def load_database():
    """Load all student records from JSON file"""
    if not os.path.exists(DATABASE_FILE):
        # Create empty file if it doesn't exist
        with open(DATABASE_FILE, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_database(data):
    """Save student records to JSON file"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# --------------------------
# 📡 API ENDPOINTS
# --------------------------
@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    students = load_database()
    return jsonify({
        "status": "success",
        "count": len(students),
        "data": students
    })

@app.route('/api/students', methods=['POST'])
def add_student():
    """Add new student"""
    try:
        student_data = request.get_json()
        
        # Add unique ID and timestamp
        student_data['id'] = str(uuid.uuid4())[:8]
        student_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to database
        students = load_database()
        students.append(student_data)
        save_database(students)
        
        return jsonify({
            "status": "success",
            "message": "Student saved successfully!",
            "data": student_data
        }), 201
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to save: {str(e)}"
        }), 500

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    """Update existing student"""
    try:
        updated_data = request.get_json()
        students = load_database()
        
        # Find and update
        for index, student in enumerate(students):
            if student['id'] == student_id:
                # Keep original ID and creation date
                updated_data['id'] = student_id
                updated_data['created_at'] = student['created_at']
                students[index] = updated_data
                save_database(students)
                
                return jsonify({
                    "status": "success",
                    "message": "Student updated successfully!",
                    "data": updated_data
                })
        
        return jsonify({
            "status": "error",
            "message": "Student not found!"
        }), 404
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Update failed: {str(e)}"
        }), 500

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete student record"""
    try:
        students = load_database()
        original_count = len(students)
        
        # Remove student
        students = [s for s in students if s['id'] != student_id]
        
        if len(students) == original_count:
            return jsonify({
                "status": "error",
                "message": "Student not found!"
            }), 404
        
        save_database(students)
        
        return jsonify({
            "status": "success",
            "message": "Student deleted successfully!"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Delete failed: {str(e)}"
        }), 500

# --------------------------
# 🚀 RUN SERVER
# --------------------------
if __name__ == '__main__':
    print("=" * 60)
    print("🎓 STUDENT MANAGEMENT SYSTEM SERVER RUNNING!")
    print(f"🌐 Server Address: http://localhost:5000")
    print(f"📂 Database File: {DATABASE_FILE}")
    print("=" * 60)
    
    # ⚠️ TURN OFF DEBUG MODE FOR PRODUCTION
    app.run(debug=False, port=5000, host='0.0.0.0')