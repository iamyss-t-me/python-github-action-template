import os
import requests
from bs4 import BeautifulSoup

TOKEN = '5481103194:AAG4QwvLnZ7k1_7NeLXxLh4226bFFHVqhiw'
CHAT_IDS = [1276109349]
def check():
    url = 'https://ww2.5movierulz.mx/telugu-movie/'
    req = requests.get(url).content
    soup = BeautifulSoup(req,'html.parser')
    divs = soup.find_all("div",class_="cont_display")
    f = open("data.txt", "r").read()
    title = divs[2].find("a")['title'].replace(" Watch Online Free",'')
    image =  divs[2].find("img")['src']
    link = divs[2].find("a")['href']
    if title == f:
        pass
    else:
        caption = "**New Movie**\n`{}`\n\n{}".format(title,link)
        for CHAT_ID in CHAT_IDS:
            send_message(CHAT_ID,caption,image)
        os.remove("data.txt")
        f = open("data.txt", "a")
        f.write(title)
        f.close()


def send_message(CHAT_ID,caption,img):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}&photo={img}&caption={caption}&parse_mode=MARKDOWN"
    requests.post(url)

if __name__ == "__main__":
    check()
