import requests
import schedule
import time
from datetime import datetime
import pytz


with open('webhook.txt', 'r') as f:
    WEBHOOK_URL = f.read().strip()
ICON = "https://cdn.discordapp.com/attachments/1089456058507989023/1089456956281982986/images.png"
NAME = "Workout Reminder"
COLOR = 5526612
# set the timezone to Warsaw
tz = pytz.timezone('Europe/Warsaw')
# get the current time in Warsaw
now = datetime.now(tz)
# format the current time as a string
current_time = now.strftime("%H:%M:%S")
current_min = now.strftime("%M")
current_hour = now.hour
already_called = False

def update_time():  
    global now, current_time, current_hour, current_min
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M:%S")
    current_min = now.strftime("%M")
    current_hour = now.hour

def send_message(time, workout, message):
    global already_called
    if already_called == False:
        update_time()
        response = requests.post(WEBHOOK_URL, json={
        "username": "Reminder",
        "avatar_url": ICON,
        "content": "@everyone get off your ass, bum",
        "embeds": [
            {
            "author": {
                "name": NAME,
            },
            "color": COLOR,
            "fields": [
                {
                    "name": "work out",
                    "value": time,
                    "inline": True
                },
                {
                    "name": workout,
                    "value": message,
                    "inline": True
                }
            ],
            "footer": {
                "text": "You've been a bum for an entire hour, its time to get up",
                "icon_url": ICON
            }
            }
        ]})

        if response.ok:
            print(f'Message sent: {message}')
        else:
            print(f'Error sending message: {response.text}')
        already_called = True

message = "You've been a bum for an entire hour, its time to get up"
workouts = []
res = []
minute = "00"

def get_workouts():
    global workouts, res
    response = requests.get('https://api.quarza.online/api/workouts')
    if response.ok:
        workouts = response.json()
        res = response.json
        print("workouts")
        for workout in workouts:
            print("workout: ", workout['id'])
            print("hour: ", workout['time'])
            print("workout: ", workout['workout'])
            print("todo: ", workout['todo'])
        print("current time: " + current_time)
        return True
    else:
        return False

def workout_reminder():
    print("reminder called")
    global already_called, workouts, res
    already_called = False
    print("updating workouts..")
    update_time()
    update = get_workouts()
    if update == True: 
        for workout in workouts:
            workout_time = workout['time']
            if current_hour == workout_time and not already_called:
                workout_name = workout['workout']
                workout_todo = workout['todo']
                send_message(workout_time, workout_name, workout_todo)
                already_called = True
            else:
                if 10 <= current_hour < 20:
                        send_message(current_time, "stop being a bum", "do something")
                        already_called = True
    else:
        print(f'Error retrieving workouts: {res.text}')
    time.sleep(60)


def start_reminder():
    print("starting reminder")
    print("current time: " + current_time)
    get_workouts()
    while True:
        if now.hour >= 6 and now.hour < 20:
            # Schedule tasks to run every hour after 10am GMT till 8pm
            schedule.every().hour.at(":" + minute).do(workout_reminder).tag('workout_reminder')
            #schedule.every().minute.do(workout_reminder)
        else:
            # Clear any pending tasks that may have been scheduled earlier
            schedule.clear('workout_reminder')
        schedule.run_pending()
        time.sleep(30)
start_reminder()