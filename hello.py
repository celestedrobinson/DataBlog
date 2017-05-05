import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import urllib.parse
import urllib.request


BIASED_FEEDS = {
    'conservative': {
    #"gatewaypundit": "http://www.thegatewaypundit.com/feed/",
    #"dailycaller": "http://feeds.feedburner.com/dailycaller?format=xml",
    'westernjournalism': "http://www.westernjournalism.com/feed/",
    'breitbart': "http://feeds.feedburner.com/breitbart?format=xml"
    },
    'liberal': {
    #    'dk1': "http://www.dailykos.com/user/Hunter/rss.xml",
    #    'dk2': "http://www.dailykos.com/user/Doctor%20RJ/rss.xml",
        'dk3': "http://www.dailykos.com/user/Jeff%20Singer/rss.xml",
        'cal': "http://feeds.crooksandliars.com/crooksandliars/YaCP?format=xml"
    }
}

DEFAULTS = {
    'currency_from': 'GBP',
    'currency_to': 'USD'
}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=cb932829eacb6a0e9ee4f38bfbf112ed"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=5b75b2ffd32c437ea871f1ce17937477"


app = Flask(__name__)


def get_rates(frm, to):
    all_currency = str(requests.get(CURRENCY_URL).content, 'utf-8')
    parsed = json.loads(all_currency).get("rates")
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate, parsed.keys()


def get_weather(query):
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query)
    data = requests.get(url).content
    data_str = str(data, 'utf-8')
    parsed = json.loads(data_str)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            "country": parsed["sys"]["country"]
        }
    return weather


def get_news(query):
    if not query or query.lower() not in BIASED_FEEDS:
        bias = 'liberal'
    else:
        bias = query.lower()
    current_bias = BIASED_FEEDS[bias]
    current_article_feeds = {page: feedparser.parse(feed) for page, feed in current_bias.items()}
    return current_article_feeds


@app.route("/")
def home():
    # get bias
    bias = request.args.get("bias")
    if not bias:
        bias = 'liberal'
    articles = get_news(bias)
    # get weather
    city = request.args.get('city')
    if not city:
        city = "Logan,UT"
    weather = get_weather(city)
    # get currency
    currency_from = request.args.get("currency_from")
    currency_to = request.args.get("currency_to")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rates(currency_from, currency_to)
    return render_template("home.html",
                           articles=articles,
                           weather=weather,
                           rate=rate,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           currencies=currencies)


if __name__ == '__main__':
    app.run(port=5000, debug=True)