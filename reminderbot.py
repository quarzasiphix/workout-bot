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
current_hour = now.hour

already_called = False

def update_time():  
    global now, current_time, current_hour
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M:%S")
    current_hour = now.hour

def send_message(time, workout, message):
    global already_called
    if already_called == False:
        update_time()
        response = requests.post(WEBHOOK_URL, json={
        "username": "Reminder",
        "avatar_url": ICON,
        "content": " get off your ass, bum",
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
        ]
        })

        if response.ok:
            print(f'Message sent: {message}')
        else:
            print(f'Error sending message: {response.text}')
        already_called = True

message = "You've been a bum for an entire hour, its time to get up"

def workout_reminder():
    print("reminder called")
    global already_called
    already_called = False
    response = requests.get('https://api.quarza.online/api/workouts')
    if response.ok:
        workouts = response.json()
        print("workouts")
        for workout in workouts:
            print("workout: ", workout['id'])
            print("hour: ", workout['time'])
            print("workout: ", workout['workout'])
            print("todo: ", workout['todo'])
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
        print(f'Error retrieving workouts: {response.text}')

# Schedule tasks to run every hour after 10am GMT
schedule.every().hour.at(":00").do(workout_reminder).tag('workout_reminder')
#schedule.every().minute.do(workout_reminder)

def start_reminder():
    print("starting reminder")
    print("current time: " + current_time)
    workout_reminder()
    while True:
        update_time()
        schedule.run_pending()
        time.sleep(1)

start_reminder()