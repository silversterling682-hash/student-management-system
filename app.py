# ==========================================
# 🐍 STUDENT MANAGEMENT SYSTEM - FINAL LIVE VERSION
# ✅ Works on PC ✅ Works on Render ✅ Works Mobile
# ==========================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime

# Initialize app
app = Flask(__name__)
CORS(app)

# ✅ FIXED: Always finds files correctly everywhere
BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIRECTORY, 'students_database.json')

# ==========================================
# 📂 DATABASE
# ==========================================
def init_database():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
        print("✅ Database created")

def get_all_students():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_students(students):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(students, f, indent=4)
        return True
    except:
        return False

# ==========================================
# 🌐 SERVE WEBSITE FILES — CRITICAL FOR RENDER
# ==========================================
@app.route('/')
def serve_home():
    try:
        return send_from_directory(BASE_DIRECTORY, 'index.html')
    except Exception as e:
        return f"❌ Error: {str(e)} | Looking in: {BASE_DIRECTORY}", 500

@app.route('/<path:filename>')
def serve_files(filename):
    try:
        return send_from_directory(BASE_DIRECTORY, filename)
    except Exception as e:
        return f"❌ File not found: {filename} | {str(e)}", 404

# ==========================================
# 🛣️ API ROUTES
# ==========================================
@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(get_all_students()), 200

@app.route('/api/students', methods=['POST'])
def add_student():
    try:
        data = request.get_json()
        data['id'] = str(uuid.uuid4())[:8]
        data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        students = get_all_students()
        students.append(data)
        save_students(students)
        return jsonify({"message": "Success", "student": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        updated = request.get_json()
        students = get_all_students()
        for i, s in enumerate(students):
            if s['id'] == student_id:
                updated['id'] = student_id
                updated['created_at'] = s['created_at']
                students[i] = updated
                save_students(students)
                return jsonify({"message": "Updated", "student": updated}), 200
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        students = get_all_students()
        original_len = len(students)
        students = [s for s in students if s['id'] != student_id]
        if len(students) < original_len:
            save_students(students)
            return jsonify({"message": "Deleted"}), 200
        return jsonify({"error": "Not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# 🚀 START SERVER — THE MOST IMPORTANT PART!
# ==========================================
init_database()

if __name__ == '__main__':
    # ✅ THIS IS WHAT MAKES IT WORK EVERYWHERE
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)