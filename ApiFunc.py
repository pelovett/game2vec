import requests as req
import sys
apiKey = open("APIKey.txt", "r").readline().strip().split("=")[1].strip('"')

#Returns json of API call for url passed in
#Default URL is mine
def api_call(start, mid, end="", userID="76561197960435530", key=apiKey):
    request_string = start+key+mid+str(userID)+end
    result = req.get(request_string)
    if result.status_code == 200:
        return result.json()
    else:
        print("Error while reaching:")
        print(request_string)
        raise Exception(result.status_code)
        return
    

#Returns json for player summaries
#key is api key, uesrID is one or list of userIDs for steam users
def get_player_sum(user="76561197978184570", api_key=apiKey):
    p_start = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key="
    p_end = "&steamids="
    return api_call(p_start, p_end, userID=user, key=api_key)['response']['players']


#Returns json for list of friends
def get_player_friends(user="76561197978184570", api_key=apiKey):
    p_start = "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key="
    p_mid = "&steamid="
    p_end = "relationship=friend"
    return api_call(p_start, p_mid, p_end, user, api_key)['friendslist']['friends']
    

#Returns json for games played in the last two weeks
def get_recent_games(user="76561197978184570", api_key=apiKey):
    p_start = "http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key="
    p_mid = "&steamid="
    p_end = "&format=json"
    return api_call(p_start, p_mid, p_end, user, api_key)['response']['games']


#Get a list of every game a user owns, and all free games they've played
def get_all_games(user="76561197978184570", api_key=apiKey):
    p_start = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key="
    p_mid   = "&steamid="
    p_end     = "&format=json"
    return api_call(p_start, p_mid, p_end, user, api_key)['response']['games']


#Return name of game based upon games Steam App ID
def get_game_name(gameID, api_key=apiKey):
    p_start = "http://api.steampowered.com/ISteamUserStats/GetSchemaForGame/v2/?key="
    p_mid = "&appid="
    return api_call(p_start, p_mid, userID=gameID, key=api_key)['game']['gameName']