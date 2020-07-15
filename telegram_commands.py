import requests
import settings

def telegram_bot_sendtext(bot_message):
    bot_token = settings.telegram['bot_key']
    bot_chatID = settings.telegram['archie_chat']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
