import socket
import pickle
import random
import time
import singleplayer as ml
from _thread import *
from threading import Thread

# CONNECTION VARIABLES
HOSTNAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOSTNAME)
PORT = 7890
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"

# CREATES SERVER SOCKET
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# GAME VARIABLES
PLAYERS_DICT = {} # Stores player information. FORMAT - {socket:player_class_object,socket2:player2_class_object ....}
CONNECTION_LIST = [] # Stores player sockets who are in a game.
CONNECTION_LIST_ALL = [] # Stores sockets of anyone who is connected to server.
GAME_OBJECT = None # Stores game class object.

# OTHER VARIABLES
FILE_LOCATIONS = ["wordbank/nouns.txt","wordbank/verbs.txt","wordbank/adj.txt"]
NUMBER_OF_EACH_TYPE_OF_WORD_TO_SELECT = 3

class Player: #filelocation is a list that contains the locations of text files in the following order: NOUNS, VERBS, ADJ
    def __init__(self,name,ready_status,filelocation,filled_paragraph,votes,voted_for,finished):
        self.name = name
        self.filelocation = filelocation
        self.wordbank = self.word_bank_generator(filelocation)
        self.filled_paragraph = filled_paragraph
        self.votes = votes
        self.voted_for = voted_for
        self.ready_status = ready_status # this is a string rather than a bool.
        self.finished = finished
    def __repr__(self):
        return "Player {} has {} votes".format(self.name,self.votes)
    def word_bank_generator(self,filelocation): #random words are selected from text files inside the FILE_LOCATIONS list.
        word_bank = []
        for location in filelocation:
            try:
                file_object = open(location,"r")
            except FileNotFoundError:
                print("File {} cannot be found.".format(location))
            else:
                linecount = 0
                entire_word_bank = []
                for i in file_object.readlines(): #Gets entire list of words in .txt file and total number of words.
                    word = i
                    word = word.replace("\n","")
                    entire_word_bank.append(word)
                    linecount += 1
                for i in range(0,NUMBER_OF_EACH_TYPE_OF_WORD_TO_SELECT): #Randomly select words.
                    rand_num = random.randrange(0,linecount)
                    word_bank.append(entire_word_bank[rand_num]) #Append word to player wordbank
        return word_bank

class Game:
    def __init__(self):
        self.selected_para = self.select_para()
    def select_para(self):
        paragraph_number = ml.paragraph_options_user_response_controller("1")
        paragraph_selected = ml.paragraph_selector(paragraph_number)
        chosen_paragraph = paragraph_selected
        return chosen_paragraph

def broadcaster():
    while True:
        try:
            for conn in CONNECTION_LIST:
                player_object = PLAYERS_DICT[conn]
                send_info = send_info_former(player_object)
                print(f"[DATA] Sending {send_info}...")
                conn.send(pickle.dumps(send_info))
            time.sleep(1)
        except:
            True

def threaded_client(conn):
    add_new_player(conn,"FIRST_STAGE")
    game_is_in_progress = True
    while game_is_in_progress:
        game_is_in_progress = game_progress_checker()
    print("[SENDING] Sending Game Progress Information...")
    for i in range(3):
        conn.send(pickle.dumps(False))
        time.sleep(0.1)

    add_new_player(conn,"SECOND_STAGE")
    player_object = PLAYERS_DICT[conn]

    end = False
    while not end:
        try:
            while True:
                received_data = recv_data(conn)
                if received_data:
                    player_class_modifier(received_data,player_object,conn)
                    print(f"[DATA] Received {received_data} from {player_object.name}.")
        except Exception as e:
            print(e)
            end = True
    disconnect_player(conn,player_object)
    conn.close()
    print(f"[DISCONNECTION] {player_object.name} disconnected.")

def recv_data(conn):
    recv_data = conn.recv(1024)
    recv_data_decoded = recv_data.decode(FORMAT)
    return recv_data_decoded

def reset_game():
    global GAME_OBJECT, PLAYERS_DICT
    GAME_OBJECT = Game()
    for key in PLAYERS_DICT:
        PLAYERS_DICT[key].name=None
        PLAYERS_DICT[key].filelocation=FILE_LOCATIONS
        PLAYERS_DICT[key].filled_paragraph=None
        PLAYERS_DICT[key].votes=0
        PLAYERS_DICT[key].ready_status="False"
        PLAYERS_DICT[key].voted_for = None
        PLAYERS_DICT[key].finished = False
        PLAYERS_DICT[key].wordbank = PLAYERS_DICT[key].word_bank_generator(FILE_LOCATIONS)
    return GAME_OBJECT, PLAYERS_DICT

def game_is_finished():
    game_is_finished = True
    for key in PLAYERS_DICT:
        if PLAYERS_DICT[key].finished == False:
            game_is_finished = False
    return game_is_finished

def add_new_player(conn,parameter):
    global PLAYERS_DICT,CONNECTION_LIST,CONNECTION_LIST_ALL
    if parameter == "FIRST_STAGE":
        CONNECTION_LIST_ALL.append(conn)
        return CONNECTION_LIST
    elif parameter == "SECOND_STAGE":
        PLAYERS_DICT[conn] = Player(name=None,filelocation=FILE_LOCATIONS,filled_paragraph=None,votes=0,ready_status="False",voted_for = None, finished = False)
        CONNECTION_LIST.append(conn)
        return PLAYERS_DICT, CONNECTION_LIST

def ip_and_port_confirmer():
    global SERVER_IP, PORT, ADDR
    print("==========SETTINGS==========")
    print(f"SERVER_IP: {SERVER_IP}")
    print(f"PORT: {PORT}")
    print("Please confirm that the settings are correct.")
    user_input = input("Enter 'N' to change settings. Enter anything else to confirm:")
    if user_input == "N" or user_input == "n":
        SERVER_IP = input("Enter desired SERVER_IP:")
        
        PORT = "123"
        while type(PORT) != int:
            PORT = input("Enter desired PORT:")
            try:
                PORT = int(PORT)
            except:
                PORT = "123"
    ADDR = (SERVER_IP, PORT)

    return SERVER_IP, PORT, ADDR

def bind_and_listen():
    try:
        SERVER.bind(ADDR)
    except socket.error as e:
        print(str(e))
    SERVER.listen()
    print(f"[LISTENING] Server is listening on {ADDR}.")

def game_progress_checker():
    players_dict_items = PLAYERS_DICT.items()
    if len(PLAYERS_DICT) == 0:
        return False
    for items in players_dict_items:
        if items[1].ready_status == "False":
            return False
    return True

def player_class_modifier(recv_info,player_object,conn):
    if "ml::N::ml" in recv_info:
        player_name = recv_info.replace("ml::N::ml","")
        player_name_ = identical_name_handler(player_name,conn,player_object) # handles names that are not unique
        player_object.name = player_name_
    elif "ml::R::ml" in recv_info:
        player_ready_status = recv_info.replace("ml::R::ml","")
        player_object.ready_status = player_ready_status
    elif "ml::F::ml" in recv_info:
        player_filled_paragraph = recv_info.replace("ml::F::ml","")
        player_object.filled_paragraph = player_filled_paragraph
    elif "ml::V::ml" in recv_info:
        player_vote = recv_info.replace("ml::V::ml","")
        player_object.voted_for = player_vote
        for i in PLAYERS_DICT.items():
            if i[1].name == player_vote:
                i[1].votes += 1

def start_new_game():
    global GAME_OBJECT, CONNECTION_LIST, PLAYERS_DICT
    # reset joined players list
    CONNECTION_LIST = []
    # reset game object
    GAME_OBJECT = Game()
    # reset player objects
    PLAYERS_DICT = {}
    return GAME_OBJECT, PLAYERS_DICT, CONNECTION_LIST, PLAYERS_DICT

def send_info_former(player_object):
    """
    0 - player name list
    1 - game ready status
    2 - chosen blank paragraph
    3 - wordbank
    4 - is_filled
    5 - filled para dict
    6 - vote results
    """
    print("========================================================")

    send_information = [[], False, None, None, False, {}, None]
    player_dict_items = PLAYERS_DICT.items()

    # 0 - list of player names
    for i in player_dict_items:
        if i[1].name != None:
            send_information[0].append(i[1].name)
    # 1 - game ready status:
    game_is_ready = True
    for conn in CONNECTION_LIST:
        if PLAYERS_DICT[conn].ready_status != "True":
            game_is_ready = False
    send_information[1] = game_is_ready
    # 2 - chosen_blank_paragraph:
    send_information[2] = GAME_OBJECT.selected_para
    # 3 - wordbank
    send_information[3] = player_object.wordbank
    # 4 - is_filled
    is_filled = True
    for conn in CONNECTION_LIST:
        if PLAYERS_DICT[conn].filled_paragraph == None:
            is_filled = False
    send_information[4] = is_filled
    # 5 - filled_para_dict
    if is_filled:
        for conn in CONNECTION_LIST:
            send_information[5][PLAYERS_DICT[conn].name] = PLAYERS_DICT[conn].filled_paragraph
    # 6 - vote_results
    vote_is_ready = True
    for conn in CONNECTION_LIST:
        if PLAYERS_DICT[conn].voted_for == None:
            vote_is_ready = False
    if vote_is_ready:
        winner_info_list = ml.winner_determiner(PLAYERS_DICT)
        send_information[6] = winner_info_list

    if send_information[6] != None:
        player_object.finished = True

    return send_information

def disconnect_player(conn,player_object):
    global CONNECTION_LIST, CONNECTION_LIST_ALL, PLAYERS_DICT
    CONNECTION_LIST.remove(conn)
    try:
        CONNECTION_LIST_ALL.remove(conn)
        PLAYERS_DICT.pop(conn)
    except Exception as e:
        print(e)
    return CONNECTION_LIST, CONNECTION_LIST_ALL, PLAYERS_DICT

def identical_name_handler(name,conn,player_object):
    send_info = send_info_former(player_object)
    while name in send_info[0]:
        name = name + "(1)"
    return name

def game_reset_thread():
    while True:
        game_status = game_is_finished()
        if game_status:
            reset_game()
        time.sleep(1)

# MAIN
if __name__ == "__main__":
    print("========WELCOME TO THE MADLIBS MULTIPLAYER SERVER PROGRAM========")
    ip_and_port_confirmer()
    bind_and_listen()
    Thread(target = broadcaster).start()
    Thread(target = game_reset_thread).start()
    while True:
        if len((CONNECTION_LIST_ALL)) == 0:
            start_new_game()
        conn, addr = SERVER.accept() #conn is a socket object.
        print(f"[CONNECTION] {addr} connected to server.")
        start_new_thread(threaded_client, (conn,))
