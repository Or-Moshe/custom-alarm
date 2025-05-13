from flask import Flask, request
from scheduler import parse_and_schedule, stop

app = Flask(__name__)
@app.route('/start', methods=['POST'])
def start():
    data = request.json
    message = data.get('message', '')
    print("message", message)
    parse_and_schedule(message)
    return "OK", 200

@app.route('/stop', methods=['POST'])
def stop():
    stop()
    return "OK", 200

def main():
    app.run(port=5000)
