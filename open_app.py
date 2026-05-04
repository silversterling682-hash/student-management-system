import time
import webbrowser
import subprocess

# Start the server
subprocess.Popen(["python", "app.py"])

# Wait a bit
time.sleep(3)

# Open the website
webbrowser.open("http://localhost:5000")