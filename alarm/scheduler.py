import schedule
import time
import threading
from datetime import datetime
from music_executer import open_random_youtube

scheduler_running = False

def parse_and_schedule(message: str):
    message = message.lower()
    try:
        if 'wake me up at' in message:
            time_str = message.split('wake me up at')[1].strip()
            return handle_one_time_alarm(time_str)
        elif 'wake me up every day at' in message:
            time_str = message.split('wake me up every day at')[1].strip()
            return handle_daily_alarm(time_str)
        elif 'cancel alarm' in message:
            schedule.clear("alarm")
            return "Alarm cancelled", 200
        else:
            return "No alarm command found", 400
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return "Failed to parse message", 400

def handle_one_time_alarm(time_str):
    now = datetime.now()
    alarm_time = datetime.strptime(time_str, "%H:%M").replace(
        year=now.year, month=now.month, day=now.day
    )
    if alarm_time < now:
        alarm_time = alarm_time.replace(day=now.day + 1)
    delay_seconds = (alarm_time - now).total_seconds()

    print(f"Scheduling one-time alarm in {delay_seconds / 60:.2f} minutes")
    schedule_alarm(delay_seconds, repeat=False)
    return "One-time alarm scheduled", 200

def handle_daily_alarm(time_str):
    print(f"Scheduling daily alarm at {time_str}")
    schedule_alarm(time_str, repeat=True)
    return "Daily alarm scheduled", 200

def schedule_alarm(time_value, repeat=False):
    # Clear previous alarm
    schedule.clear("alarm")

    # Start scheduler thread only once
    global scheduler_running
    if not scheduler_running:
        threading.Thread(target=run_scheduler, daemon=True).start()
        scheduler_running = True

    # Schedule
    if repeat:
        schedule.every().day.at(time_value).do(open_random_youtube).tag("alarm")
    else:
        schedule.every(time_value).seconds.do(one_time_wrapper).tag("alarm")

def one_time_wrapper():
    open_random_youtube()
    return stop()

def stop():
    return schedule.CancelJob

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
