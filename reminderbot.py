import requests
import schedule
import time
from datetime import datetime
import pytz
import json

with open('webhook.txt', 'r') as f:
    WEBHOOK_URL = f.read().strip()

with open('api.link', 'r') as f:
    API_URL = f.read().strip()

data = []


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

# Load JSON data from file
with open('post.json', 'r') as f:
    data = json.load(f)
#modify the json
data['embeds'][0]['color'] = COLOR
data['embeds'][0]['author']['name'] = NAME
data['content'] = "@everyone time to work out!"
data['avatar_url'] = ICON
data['embeds'][0]['footer']['icon_url'] = ICON

message = "You've been a bum for an entire hour, its time to get up"
workouts = []
#res = []
minute = "00"
#wait = 3600
till = current_hour
start = 6
stop = 22
        
def update_time():  
    global now, current_time, current_hour, current_min
    now = datetime.now(tz)
    current_time = now.strftime("%H:%M:%S")
    current_min = now.strftime("%M")
    current_hour = now.hour

def send_message(time, workout, message):
    global already_called, data
    if already_called == False:
        update_time()
        # add the workout to the json
        #data['embeds'][0][0]['fields'][0]['name'] = "new workout name"
        data['embeds'][0]['fields'][0]['value'] = str(time)
        data['embeds'][0]['fields'][1]['name'] = workout
        data['embeds'][0]['fields'][1]['value'] = message
        # print json
        #print(data)
        headers = {'Content-Type': 'application/json'}
        data_str = json.dumps(data)
        response = requests.post(WEBHOOK_URL, data_str, headers=headers)
        if response.ok:
            print(f'Message sent: {message}')
        else:
            print(f'Error sending message: {response.text}')
        already_called = True

def get_workouts():
    global workouts, till
    response = requests.get(API_URL)
    if response.ok:
        workouts = response.json()
        #res = response.json
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
    
def get_workout_time():
    update_time()
    if now.hour >= start and now.hour < stop:
        return True
    else:
        print("not workout time")
        return False

def workout_reminder():
    if get_workout_time() == True:
        global already_called, workouts
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
            if get_workout_time() == True and already_called == False:
                    send_message(current_time, "stop being a bum", "do something")
                    till = current_hour + 1
                    print("waiting till: ", till, ":", minute)
            #time.sleep(wait) # sleep for hour and loop
        else:
            print(f'Error retrieving workouts')
            quit()
    print(current_time)
    print("going back to scheduler to reset loop")
    print("starting reminder")
    print("current time: " + current_time)

#schedule.every().minute.do(workout_reminder).tag('workout_reminder')
schedule.every().hour.at(":" + minute).do(workout_reminder).tag('workout_reminder')
                

def start_reminder():
    global already_called
    print("starting reminder")
    print("current time: " + current_time)
    get_workouts()
    while True:
        if get_workout_time() == True:
            # Schedule tasks to run every hour after 10am GMT till 8pm
            if already_called == True:
                time.sleep(60)
            schedule.run_pending()
        else:
            # Clear any pending tasks that may have been scheduled earlier
            schedule.clear('workout_reminder')
            print("not workout time yet, waiting till its time to workout")
            while get_workout_time() == False:
                time.sleep(60)
        time.sleep(10)
start_reminder()