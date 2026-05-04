# ==========================================
# 🖥️  STUDENT MANAGEMENT SYSTEM - SERVER
# Runs the backend silently in background
# ==========================================

import os
import sys

# Make sure we can find our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our main app
from app import app

if __name__ == "__main__":
    # Run the server silently
    app.run(debug=False, port=5000, host='127.0.0.1')