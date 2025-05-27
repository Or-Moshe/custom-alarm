import ctypes
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from alarm.music_executer import open_random_youtube

# Windows API flags
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

def prevent_sleep():
    print("Preventing system sleep...")
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

def allow_sleep():
    print("Allowing system to sleep again...")
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

# Scheduler instance
scheduler = BackgroundScheduler()
job_added = False

def doSomething():
    print("Doing scheduled work at", datetime.now())
    open_random_youtube()

def start_scheduler(hour, minute):
    global job_added
    if not job_added:
        scheduler.add_job(doSomething, 'cron', hour=hour, minute=minute, id='daily_job')
        job_added = True
    if not scheduler.running:
        prevent_sleep()
        scheduler.start()

def stop_scheduler():
    global job_added
    if scheduler.running:
        scheduler.shutdown()
        allow_sleep()
        print("Scheduler stopped.")
    job_added = False
