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
minute = "07"
wait = 3600
till = current_hour
start = 6
stop = 20

def get_workouts():
    global workouts, res, till
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
        till = current_hour + 1
        print("waiting till: ", till, ":", minute)
        return True
    else:
        return False
    
def workout_time():
    update_time()
    if now.hour >= start and now.hour < stop:
        print("init workout")
        return True
    else:
        print("not workout out time")
        return False


def workout_reminder():
    while True:
        global already_called, workouts, res
        print("updating workouts..")
        update_time()
        update = get_workouts()
        already_called = False  # Reset the flag at the beginning of the function
        if update == True: 
            for workout in workouts:
                workout_time = workout['time']
                if current_hour == workout_time and already_called == False:
                    workout_name = workout['workout']
                    workout_todo = workout['todo']
                    send_message(workout_time, workout_name, workout_todo)
                    already_called = True
                
            if workout_time() == True and already_called == False:
                    send_message(current_time, "stop being a bum", "do something")
                    already_called = True
            if workout_time() == True:
                print("waiting for: ", wait, "s till next message")
                time.sleep(wait) # sleep for hour and loop
            else:
                print("going back to scheduler to reset loop")
        else:
            print(f'Error retrieving workouts: {res.text}')
            quit()


def start_reminder():
    global already_called
    print("starting reminder")
    print("current time: " + current_time)
    get_workouts()
    while True:
        if now.hour >= start and now.hour < stop:
            # Schedule tasks to run every hour after 10am GMT till 8pm
            schedule.every().hour.at(":" + minute).do(workout_reminder).tag('workout_reminder')
            #schedule.every().minute.do(workout_reminder)
        else:
            # Clear any pending tasks that may have been scheduled earlier
            schedule.clear('workout_reminder')
        schedule.run_pending()
        time.sleep(10)
start_reminder()