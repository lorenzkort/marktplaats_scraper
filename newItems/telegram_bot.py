import requests

def telegram_send_text(bot_message='Hey this is a text message', chat_id = '-425371692'):
    
    bot_token = '1132455575:AAFWwpwZ-qJUdabq-WbSHoK8nh7aPwMoVo4'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)

    return response.json()

# https://api.telegram.org/bot1132455575:AAFWwpwZ-qJUdabq-WbSHoK8nh7aPwMoVo4/getUpdates
