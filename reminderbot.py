import requests
import schedule
import time
from datetime import datetime

#WEBHOOK_URL = 'https://discord.com/api/webhooks/1089448366582284298/Ye1uZbFI-J6YxLSqmIHNqHbv9yadudbWHvaNfk_EEN8tpyFyrUIeRdMB7tS-3-aCaMzI'
WEBHOOK_URL = "https://discord.com/api/webhooks/1089454889089904690/kWg_Ef03R9ddL2U9hPBbcR9U10OOy2vTxldIXe_gXqMueQbaqJQZcsrCWdNyvOHh5Za6"
ICON = "https://cdn.discordapp.com/attachments/1089456058507989023/1089456956281982986/images.png"
NAME = "Workout Reminder"
COLOR = 11119017
#BODY = 

def send_message(workout, message):
    response = requests.post(WEBHOOK_URL, json={
    "username": "Webhook",
    "avatar_url": "https://i.imgur.com/4M34hi2.png",
    #"content": "Text message. Up to 2000 characters.",
    "embeds": [
        {
        "author": {
            "name": NAME,
            "url": ICON,
            "icon_url": ICON
        },
        "title": "REMINDER",
        #"url": "https://google.com/",
        #"description": "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`",
        "color": COLOR,
        "fields": [
            {
                "name": workout,
                "value": message,
                "inline": True
            }
        ],
        #"thumbnail": {
        #    "url": "https://upload.wikimedia.org/wikipedia/commons/3/38/4-Nature-Wallpapers-2014-1_ukaavUI.jpg"
        #},
        #"image": {
        #    "url": "https://upload.wikimedia.org/wikipedia/commons/5/5a/A_picture_from_China_every_day_108.jpg"
        #},
        "footer": {
            "text": "No one else is doing shit with their life, doing this will put you ahead 90%",
            "icon_url": "https://i.imgur.com/fKL31aD.jpg"
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
    now = datetime.now()
    current_hour = now.hour
    if current_hour == 10:
        send_message('Time for a workout!')
    elif current_hour == 11:
        send_message(message + '\n do 30 push ups and some sit ups.')
    elif current_hour == 12:
        send_message(message + '\n now its time for burpees, \n do 3 sets of 10 burpees ')
    else:
        send_message('Time for a workout!')

# Schedule tasks to run every hour after 10am GMT
schedule.every().day.at('10:00').do(workout_reminder)
schedule.every().day.at('11:00').do(workout_reminder)
schedule.every().day.at('12:00').do(workout_reminder)

def start_reminder():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    print("calling send message")
    send_message(message, '\n do 30 push ups and some sit ups.')
    
    #send_message(message + '\n now its time for burpees, \n do 3 sets of 10 burpees ')

main()