# API Key: eb6241f96c3649a084f36500b3dd89e3
import datetime
import time

import pandas
import requests
import yagmail


class NewsFeed:
    """Representing multiple news titles and links as a single string
    """
    base_url = "http://newsapi.org/v2/everything?"
    api_key = "eb6241f96c3649a084f36500b3dd89e3"

    def __init__(self, interest, from_date, to_date, language='en'):
        self.interest = interest
        self.from_date = from_date
        self.to_date = to_date
        self.language = language

    def _build_url(self):
        url = f"{self.base_url}" \
              f"qInTitle={self.interest}&" \
              f"from={self.from_date}&" \
              f"to={self.to_date}&" \
              f"language={self.language}&" \
              f"apikey={self.api_key}"
        return url

    def _get_articles(self, url):
        response = requests.get(url)
        content = response.json()
        articles = content['articles']
        return articles

    def get(self):
        url = self._build_url()

        articles = self._get_articles(url)

        email_body = ''
        for article in articles:
            email_body = email_body + article['title'] + "\n" + article['url'] + "\n\n"

        return email_body


def send_mail():
    today = datetime.datetime.now().strftime('%Y-%m-d')
    yesterday = ((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-d'))
    news_feed = NewsFeed(interest=row['interest'], from_date=yesterday, to_date=today)
    email = yagmail.SMTP(user="YOU CAN ADD MAIL ID FROM WHOM YOU WANT TO SEND MAIL", password="ENTER PASSWORD HERE")
    email.send(to=row['email'],
               subject=f"Your {row['interest']} news for today!",
               contents=f"Hi {row['name']}\n\n\n"
                        f"See whats's on about {row['interest']} today."
                        f"\n\n\n{news_feed.get()}"
                        f"\n\nThanks & Regards,"
                        f"\n Akash Gawande")


while True:
    if datetime.datetime.now().hour == 20 and datetime.datetime.now().minute == 40:

        df = pandas.read_excel('people.xlsx')

        for index, row in df.iterrows():
            send_mail()
    time.sleep(60)
