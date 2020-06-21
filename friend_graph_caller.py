from api_func import *
from multiprocessing import Process, Queue, Lock, Value, Manager
from os import path
from time import sleep


def get_friends(to_explore, api_key, player_array,
                collected_count, collected_ids):
    if len(to_explore) == 0:
        print('To explore is empty')
        return
    else:
        player_id = to_explore.pop(0)
    sleep(69/60)
    try:
        friend_list = get_player_friends(api_key, player_id)
    except Exception as e:
        # User has a locked profile
        if e.args[0] == 401 or e.args[0] == 403:
            print(f'Player: {player_id} has a private profile')
            get_friends(to_explore, api_key, player_array,
                        collected_count, collected_ids)
            return
        else:
            print(e)
            raise

    print('api call complete')
    for friend in friend_list:
        steam_id = friend['steamid']
        if steam_id not in collected_ids:
            collected_ids.add(steam_id)
            player_array.append(steam_id)
            to_explore.append(steam_id)

    if len(player_array) > 100:
        if path.exists(output_file_name):
            file_open_type = 'a'
        else:
            file_open_type = 'w'
        with open(output_file_name, file_open_type) as out_file:
            for steam_id in player_array:
                out_file.write(steam_id+'\n')
        collected_count += len(player_array)
        print(f'Number of IDs collected: {collected_count}')
        if collected_count > 100000:
            return
    get_friends(to_explore, api_key, player_array, collected_count,
                collected_ids)
    return


if __name__ == '__main__':
    api_key = open('apiKey.txt', 'r').readline().strip()
    GRAPH_START = '76561197978184570'
    output_file_name = 'steam_ids.txt'

    total_ids_collected = 0
    exit_flag = False
    to_explore = []
    player_set = set()
    player_array = []

    to_explore.append(GRAPH_START)

    get_friends(to_explore, api_key, player_array, total_ids_collected,
                player_set)
