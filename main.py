import cloudscraper
from bs4 import BeautifulSoup
import os
from datetime import datetime   
import pytz
import requests
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

url = 'https://in.bookmyshow.com/explore/sports-vadodara'

div_class = 'sc-dv5ht7-0 XmXCP'
scraper = cloudscraper.create_scraper(
    browser='chrome'
)
def check_wpl():
    response = scraper.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div',{'class':div_class})
    for div in divs:
        title = div.find('h3')
        if "wpl" in title.text.lower():
            print(title.text)
            return True
    return False

def send_telegram_message(data):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data=data)

def main():
    try:
        indian_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        data = {
            'chat_id': chat_id,
        }
        if check_wpl():
            data['text'] = f"WPL is available at {indian_time.strftime('%Y-%m-%d %H:%M:%S')}"
            send_telegram_message(data)
        else:
            data['text'] = f"WPL is not available.\n\nChecked at {indian_time.strftime('%Y-%m-%d %H:%M:%S')}"
            data['disable_notification'] = True
            send_telegram_message(data)
    except Exception as e:
        data['text'] = f"Error: {e}\n\nChecked at {indian_time.strftime('%Y-%m-%d %H:%M:%S')}"
        send_telegram_message(data)

if __name__ == "__main__":
    main()
