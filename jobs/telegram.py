import requests

def send_text(msg='Hey this is a test message', chatId = '-999999999'):
    bot_token = '1123409823:abcd'
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chatId}&parse_mode=Markdown&text={msg}"
    response = requests.get(send_text)
    return response.json()

# https://api.telegram.org/bot1132455575:AAFWwpwZ-qJUdabq-WbSHoK8nh7aPwMoVo4/getUpdates

if __name__ == "__main__":
    print(send_text())
