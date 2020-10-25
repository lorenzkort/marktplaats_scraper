import pandas as pd
from telethon.sync import TelegramClient

# credentials for getting messages from Telegram
session_name = 'Session 1'
api_id = '1934142'
api_hash = '360ee7aa959093395e2aa565fca01f3c'
chat = 'https://t.me/joinchat/O_y2oxlaqCwZVwEqK46wXg'

# get messages in Json
client = TelegramClient(session_name, api_id, api_hash)
client.start()
messages = client.get_messages(chat, limit=1000, from_user=1132455575)
client.disconnect()

# parse to dataframe
messages_out = []
for msg in messages:
    try:
        text = msg.text.split('\n')
        attributes = text[1].split('|')

        title = text[0].strip()
        price = attributes[0].replace('€','').strip()
        distance = attributes[1].replace('KM','').strip()
        city = attributes[2].strip()
        date = msg.date
        msg_content = {
            'title': title,
            'price': price,
            'distance': distance,
            'city': city,
            'date': date
        }
        messages_out.append(msg_content)
    except:
        print(f'Message at {msg.date} not parsable')

df = pd.DataFrame(messages_out).drop_duplicates()
df.to_csv('messages.csv')