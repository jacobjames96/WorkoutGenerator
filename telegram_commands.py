import requests
import settings
import json
import time
import generator

token = settings.telegram['bot_key']
URL = 'https://api.telegram.org/bot{}/'.format(token)


def get_url(url):
    # Performs a get request on a url and returns the reply
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    # Turns json from a Telegram https get request into a nice usable dict
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    # Performs long polling against telegram API to monitor updates for the exercise bot
    url = URL + "getUpdates?timeout=100"
    if offset:
        # Include offset to only retrieve messages we haven't processed before
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    # Gets the ID of the latest update from 'getUpdates' request for use in long polling
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(text, chat_id):
    # Sends a message from the exercisebot to the specified chat ID
    url = URL + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    get_url(url)


def process_updates(updates):
    # Loops through all the latest updates
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # fire off the workout function if the user has requested a workout...
            if text.lower() == 'workout':
                print("User requested a workout")
                workout(chat)
        except Exception as e:
            print(e)


def workout(chat_id):
    # Run through the flow of generating a workout

    # Get points target and exercises, generate the workout
    points_target, exercises = generator.get_exercises()
    generated_workout, actual_points = generator.generate_workout(points_target, exercises)

    # Format the workout into a nice list and send the user their workout
    workout_formatted = generator.format_workout(generated_workout)
    message = 'Here is your workout worth {} points consisting of: \n{}'.format(actual_points, workout_formatted)
    send_message(message, chat_id)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            process_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
