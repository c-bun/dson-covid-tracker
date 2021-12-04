
# script:
# read in data
# check site
# compare data
# if different:
    # send message
    # append data
    
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup

def parse_soup(soup):
    td = soup.find_all('td')
    result = [x.get_text() for x in td]
    to_send = "Students pos/cum. pos/quarantine:" + result[2]+ '/' + result[3]+ '/' + result[4]
    to_append = [int(result[2]), int(result[3]), int(result[4])]
    return to_append, to_send

def telegram_bot_sendtext(bot_message):
    
    bot_token = '2113495995:AAE0-1MxKj6MNECSrobxt6tIcOj9wYz10OA'
    bot_chatID = '2122924009'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

try:
    data = pd.read_csv('./data.csv', index_col=0)
except FileNotFoundError:
    print("CSV does not exist. Creating new one.")
    time = datetime.datetime.now().strftime("%x %X")
    df = pd.DataFrame({'time':[time], 'pos':[0], 'cumulative':[0], 'quarantine':[0]})
    df.to_csv('./data.csv')
    data = pd.read_csv('./data.csv', index_col=0)
    
print("found data, reading site")

url = "https://www.dickinson.edu/homepage/1505/fall_2021_semester_information"
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

current_numbers, to_send = parse_soup(soup)
print("Found Current numbers:", to_send)

last_numbers = list(data.iloc[-1].values[1:])

if last_numbers != current_numbers:
    print("New numbers!")
    time = datetime.datetime.now().strftime("%x %X")
    new_numbers = pd.DataFrame({'time':[time],'pos':[current_numbers[0]], 'cumulative':[current_numbers[1]], 'quarantine':[current_numbers[2]]})
    data = data.append(new_numbers, ignore_index=True)
    print("Appended. Writing csv.")
    data.to_csv('./data.csv')
    
    # send telegram
    telegram_bot_sendtext(to_send)
    
else:
    print("No new numbers right now.")
