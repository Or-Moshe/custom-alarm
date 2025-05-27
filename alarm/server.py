# app.py
from flask import Flask, request
import atexit
from scheduler_service import scheduler, start_scheduler, stop_scheduler, allow_sleep
import re
app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    message = data.get('message', '')
    matches = re.findall(r'\b(?:[01]?\d|2[0-3]):[0-5]\d\b', message)

    hour = matches[0].split(":")[0]
    minute = matches[0].split(":")[1]
    start_scheduler(hour, minute)
    return "Scheduler started.", 200

@app.route('/stop', methods=['POST'])
def stop():
    stop_scheduler()
    return "Scheduler stopped", 200

# Shutdown logic
atexit.register(lambda: (allow_sleep(), scheduler.shutdown()))

if __name__ == "__main__":
    app.run(port=5000)
