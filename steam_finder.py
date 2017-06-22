"""
Helps look for the steam game you want and keeps trying in case you get an error
"""
import json
import random
import requests
from hidden_keys import STEAM_KEY
from bs4 import BeautifulSoup


def scrape_name(appid):
    pass


def find_real_name(appid):
    """Called to find the name of the game using Steam's main page
    """
    response = requests.get('http://store.steampowered.com/app/{}/This_War_of_Mine/'.format(appid))
    # TODO: check the response code
    soup = BeautifulSoup(response.content)
    title = soup.title.text
    return title.split("on Steam")[0]


def get_real_game(apps):
    """Tries to find a real game in the list of choices

    Steam sometimes returns junk, and so we have to check
    to make sure it is something that someone would play.
    Otherwise, we try again. If we have no luck, eventually
    we just let the user know that we couldn't get it working.
    """
    for _ in range(20):
        appid = str(random.choice(apps)['appid'])
        params = {'key': STEAM_KEY, 'appid': appid}
        try:
            result = requests.get("http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/",
                                  params=params)
            game_content = result.json()
            return appid, find_real_name(appid)
        except:
            pass
    return 0, "Unable to find a game. Please try again."


def get_random_game(steamid, number_of_suggestions=5):
    """Using a steamid, finds a random game to play
    """
    params = {'key': STEAM_KEY, 'steamid': steamid}
    result = None
    # Attempts to get the given steamid 10 times before giving up
    for _ in range(10):
        try:
            result = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/",
                                  params=params)
            if result.status_code == 200:
                break
            else:
                result = None
        except:
            pass
    if result:
        content = result.json()
        apps = content['response']['games']
        games = {}
        while len(games) < number_of_suggestions:
            game_id, game_name = get_real_game(apps)
            games[game_name] = "http://cdn.akamai.steamstatic.com/steam/apps/{}/header_292x136.jpg?t=1492697491".format(game_id)
        return games
    else:
        return "There was an error with your request. \
                Check to make sure you have your correct \
                SteamID"

