from api_func import *
from multiprocessing import Process, Queue, Lock, Value, Manager
from os import path 
from time import sleep


def get_friends(lock, api_key, player_array, collected_count, collected_ids):
    if to_explore.empty():
        sleep(20) #TODO handl 410 errors
        if to_explore.empty():
            return
    player_id = to_explore.get()
    
    if exit_flag:
        return
    try:
        friend_list = get_player_friends(api_key, player_id)
    except Exception as e:
        if hasattr(e, 'message'):
            # User has a locked profile
            if e.message == '403':
                print(player_id)
                get_friends(lock, api_key)
        else:
            print(e)
            raise

    lock.acquire()
    print('api call complete')
    for friend in friend_list:
        steam_id = friend['steamid']
        if steam_id not in collected_ids:
            collected_ids[steam_id] = 1
            player_array.append(steam_id)
            to_explore.put(steam_id)

    if len(player_array) > 100:
        if path.exists(output_file_name):
            file_open_type = 'a'
        else:
            file_open_type = 'w'
        with open(output_file_name, file_open_type) as out_file:
            for steam_id in player_array:
                out_file.write(steam_id+'\n')
            player_array = []
        collected_count.value += len(player_array)
        print(f'Number of IDs collected: {collected_count.value}')
        if collected_count.value > 100:
            lock.release()
            return
    lock.release()
 
    get_friends(lock, api_key, player_array, collected_count, collected_ids)


if __name__ == '__main__':
    api_key = open('apiKey.txt', 'r').readline().strip()
    GRAPH_START = '76561197978184570'
    output_file_name = 'steam_ids.txt'

    total_ids_collected = Value('i', 0)
    exit_flag = False
    to_explore = Queue()
    manager = Manager()
    player_set = manager.dict()
    player_array = []
    proc_lock = Lock()    

    to_explore.put(GRAPH_START)
    num_processes = 2
    processes = []
    for i in range(num_processes):
        p = Process(target=get_friends, args=(proc_lock, api_key,
                    player_array, total_ids_collected, player_set))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
