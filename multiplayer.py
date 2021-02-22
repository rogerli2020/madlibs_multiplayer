import sys
import socket
import pickle
import time
import singleplayer as ml
from threading import Thread

"""
    0 - player name list
    1 - game ready status
    2 - chosen blank paragraph
    3 - wordbank
    4 - is_filled
    5 - filled para dict
    6 - vote results
"""

# Connection global variables.
SERVER_IP = "192.168.0.107"
PORT = 7890
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"

# Information received from server.
SERVER_INFO = [[], False, None, None, False, {}, None]

# Creates socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def connection():
    ip_address = input(">>> Please enter server IP address:")
    if ip_address == "-q":
        sys.exit()
    port_num = "123"
    while type(port_num) != int:
        port_num = input(">>> Please enter server port number:")
        if port_num == "-q":
            sys.exit()
        try:
            port_num = int(port_num)
        except:
            continue
    address = (ip_address,port_num)
    try:
        print(f"[CONNECTION] Connecting to {ip_address}:{port_num}...")
        client.connect(address)
    except Exception as e:
        print(e)
        print(f"[CONNECTION] Failed to connect to {address}. The server might be down or you've entered the wrong server address.")
        return False
    else:
        print("[CONNECTION] Successfully connected to targeted server!")
        return True

def server_info_updater_loop():
    while True:
        server_info_updater()
        time.sleep(0.1)

def server_info_updater():
    global SERVER_INFO
    recved_info = recv_info()
    if type(recved_info) == list:
        SERVER_INFO = recved_info
        return SERVER_INFO

def check_game_progress():
    print("[SERVER] Waiting for a joinable game...")
    recved_info = True
    while recved_info != False:
        recved_info = recv_info()
    print("[SERVER] You've joined a joinable game.")

def get_name():
    name = ""
    while len(name) == 0 or len(name) > 10 or " " in name:
        name = input(">>> Please enter your name:")
        if name == "-q":
            sys.exit()
        if len(name) == 0:
            print("[CLIENT] Name cannot be blank. Please re-enter.")
        elif len(name) > 10:
            print("[CLIENT] Length of name cannot exceed 10 characters. Please re-enter.")
        elif " " in name:
            print("[CLIENT] Using spaces in your name is not allowed. Please re-enter.")
        else:
            return name

def get_ready():
    response = ""
    while response not in "Yy" or len(response) != 1:
        response = input(">>> Please enter Y when you think everyone is ready:")
        if response == "-q":
            sys.exit()
    print("[CLIENT] You're Ready!")
    return "True"

def ready_status_checker():
    print("[SERVER] Waiting for everyone to get ready...")
    while SERVER_INFO[1] == False:
        continue
    print(f"[SERVER] Game will start soon! Players participating are {SERVER_INFO[0]}.")
    time_index = 3
    while time_index != 0:
        print(f"[SERVER] Game starting in {time_index}...")
        time.sleep(1)
        time_index -= 1

def print_prompt():
    blank_para = SERVER_INFO[2]
    wordbank = SERVER_INFO[3]

    print("============================================================")
    print("=================   GAME STARTS   ==========================")
    print("============================================================")
    print("The chosen blank paragraph is...")
    print("============================================================")
    print(blank_para.replace("\n",""))
    print("============================================================")
    print(f"Your word bank is {wordbank}.")

def get_filled():
    blank_para = SERVER_INFO[2]
    wordbank = SERVER_INFO[3]

    blank_count = ml.blank_counter(blank_para)
    user_response_is_ok = False
    print("[SERVER] Please enter your word choices in desired order")
    while not user_response_is_ok:
        user_response = input(">>> Please separate your words using spaces:")
        if user_response == "-q":
            sys.exit()
        reply = ml.player_word_input_eligibility_checker(wordbank,user_response,blank_count)
        user_response_is_ok = reply[0]
        if not user_response_is_ok:
            print(reply[1])
    return ml.filled_paragraph_generator(blank_para,user_response)

def filled_status_checker():
    print("[SERVER] Waiting for everyone to fill their paragraphs...")
    while SERVER_INFO[4] == False:
        continue
    print("[SERVER] Everyone has filled their paragraphs. Time to vote!")

def get_player_vote():
    print("[SERVER] Whose sentence is your favorite? Please enter your response...")
    vote_is_good = False
    while not vote_is_good:
        print(f"[SERVER] List of players participating: {SERVER_INFO[0]}.")
        player_vote = input(">>> Please cast your vote:")
        if player_vote == "-q":
            sys.exit()
        if player_vote in SERVER_INFO[0]:
            vote_is_good = True
            return player_vote
        else:
            continue

def print_filled():
    filled_dict = SERVER_INFO[5]
    print("================================================")
    print("[SERVER] Time to vote!")
    for item in filled_dict.items():
        print(f"{item[0]}: {item[1]}.")
    print("================================================")

def vote_status_checker():
    print("[SERVER] Waiting for everyone to vote.")
    while SERVER_INFO[6] == None:
        continue

def winner_message_displayer():
    winner_info = SERVER_INFO[6]
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                  >>>>>>>>Player(s) {} WON!!<<<<<<<<<<".format(winner_info[0]))
    print("               They have accumulated the most number of votes ({})!".format(winner_info[1]))
    print("                               CONGRATULATIONS!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def game():
    while True:
        print("[SERVER] A new game is ready...")
        name = get_name() # gets a valid user name
        send_info("ml::N::ml" + str(name)) # sends name to server
        print("[CLIENT] Your name is sent to the server!")
        ready_status = get_ready() # 
        send_info("ml::R::ml" + str(ready_status)) # sends ready.
    
        ready_status_checker() # Blocks program until game is ready...

        print_prompt() # Prints game prompt.
        player_filled_para = get_filled() # Gets legal filled paragraph.
        send_info("ml::F::ml" + str(player_filled_para)) # Sends filled paragraph to server.

        filled_status_checker() # Blocks program until everyone has filled.

        print_filled() # Prints all filled para.
        vote = get_player_vote() # gets legal vote choice.
        send_info("ml::V::ml" + str(vote)) # send vote choice to server.

        vote_status_checker() # Blocks program until everyone has voted.

        winner_message_displayer()
        print("[SERVER] Starting new game...")



def send_info(info):
    try:
        info_bytes = info.encode(FORMAT)
        client.send(info_bytes)
    except Exception as e:
        input("\n[ERROR] Lost connection to the server. Please exit this program by entering anything:")
        sys.exit()

def recv_info():
    try:
        recved_info = pickle.loads(client.recv(4096))
        time.sleep(0.5)
    except Exception as e:
        input("\n[ERROR] Lost connection to the server. Please exit this program by entering anything:")
        sys.exit()
    else:
        return recved_info

if __name__ == "__main__":
    print("============MADLIBS:MULTIPLAYER============")
    print("Tip: Enter '-q' anywhere to quit.")
    connected = False
    while not connected:
        connected = connection()
    check_game_progress()
    # Create two threads, one for constant receipt of server information, one for sending info and controlling game progress.
    Thread(target = server_info_updater_loop).start()
    Thread(target = game).start()
