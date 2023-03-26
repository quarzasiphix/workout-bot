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

def update_time():
    global now, current_time, current_hour
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M:%S")
    current_hour = now.hour

def send_message(time, workout, message):
    update_time()
    response = requests.post(WEBHOOK_URL, json={
    "username": "Reminder",
    "avatar_url": ICON,
    #"content": "Text message. Up to 2000 characters.",
    "embeds": [
        {
        "author": {
            "name": NAME,
            #"url": ICON,
            #"icon_url": ICON
        },
        #"title": "REMINDER",
        #"url": "https://google.com/",
        #"description": "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`",
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

message = "You've been a bum for an entire hour, its time to get up"

def workout_reminder():
    print("reminder called")
    response = requests.get('https://api.quarza.online/api/workouts')
    if response.ok:
        workouts = response.json()
        for workout in workouts:
            print("workouts")
            print(workout['time'])
            print(workout['workout'])
            print(workout['todo'])
        for workout in workouts:
            workout_time = workout['time']
            if current_hour == workout_time:
                workout_name = workout['workout']
                workout_todo = workout['todo']
                send_message(workout_time, workout_name, workout_todo)
    else:
        print(f'Error retrieving workouts: {response.text}')

# Schedule tasks to run every hour after 10am GMT
schedule.every(1).hour.do(workout_reminder)

def start_reminder():
    print("starting reminder")
    print("current time: " + current_time)
    workout_reminder()
    while True:
        update_time()
        schedule.run_pending()
        time.sleep(1)

def main():
    print("calling send message")
    send_message("PUSH UPS", '\n do 30 push ups and some sit ups.')
    
    #send_message(message + '\n now its time for burpees, \n do 3 sets of 10 burpees ')

start_reminder()