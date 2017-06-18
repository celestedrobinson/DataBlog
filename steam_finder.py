"""
Helps look for the steam game you want and keeps trying in case you get an error
"""
import json
import random
import requests
from hidden_keys import STEAM_KEY


def is_real_game(game_name):
    """Makes sure that the given game is real

    For now we assume it is, since it turns out that not all
    games have been named properly. So this should be replaced
    so that we get the actual name of the game, rather than the
    one exposed by steam.
    """
    """
    if 'valvetest' in game_name.lower() or game_name == 'Capy_Test':
        return False
    elif len(game_name) < 2:
        return False
    else:
        return True
        """
    return True


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
            try:
                game_result = game_content['game']['gameName']
                if is_real_game(game_result):
                    return appid, game_result
            except KeyError:
                pass
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

