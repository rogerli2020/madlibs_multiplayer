import random

NUMBER_OF_EACH_TYPE_OF_WORD_TO_SELECT = 3
FILE_LOCATIONS = ["wordbank/nouns.txt","wordbank/verbs.txt","wordbank/adj.txt"]
PARAGRAPH_LIST_LOCATION = "wordbank/paragraphs.txt"
RECOVER_LIST = ["""He looked at her NOUN, and without hesitation, he VERBed their NOUNs.
My NOUN was acting a bit ADJ, so I decided to VERB it.
To the surprise of everyone, the NOUN happened yesterday, but it didn't VERB as expected.
When he VERBed my NOUN, I sensed a ADJ NOUN coming from my NOUN.
To VERB a NOUN, one must first VERB their NOUN.
"This is some serious gourmet!" Rick exclaimed as he took a bite of the ADJ NOUN.
The ADJ NOUN is the most popular scenic attraction of Whispering Oaks Amusement Park.
"I couldn't, I just couldn't VERB my NOUN... I am so sorry..." Jordan said as he teared up.
To lessen the pain, Helen used a ADJ NOUN to cover up her wound."""
]

class Player: #filelocation is a list that contains the locations of text files in the following order: NOUNS, VERBS, ADJ
    def __init__(self,name,filelocation,filled_paragraph,votes):
        self.name = name
        self.filelocation = filelocation
        self.wordbank = self.word_bank_generator(filelocation)
        self.filled_paragraph = filled_paragraph
        self.votes = votes
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

def name_and_wordbank_obtainer(ask_count): #This function ONLY asks for user response.
    if ask_count == 0:
        input_prompt_message = "Please enter name of one player:"
    else:
        input_prompt_message = "Please enter name of another player:"
    player_name = input(input_prompt_message)
    return player_name
def name_list_former(player_count): #This function forms a list based on the inputs of name_and_wordbank_obtainer function.
    ask_count = 0
    name_list = []
    for num in range(0,player_count):
        name_user_entered = name_and_wordbank_obtainer(ask_count)
        while name_user_entered in name_list or name_user_entered == "":
            if name_user_entered in name_list:
                print("***Sorry, players cannot share same name. Please reenter.")
            elif name_user_entered == "":
                print("***Sorry, player name cannot be blank. Please reenter.")
            name_user_entered = name_and_wordbank_obtainer(ask_count)
        name_list.append(name_user_entered)
        ask_count += 1
    return name_list
def player_objects_former(): #This function asks for number of users, gets list of name of users, and ultimately creates Player class objects based on inputs. It also returns a list or dict of player names so it can be accessed outside.
    print("=======================PLAYER=OPTIONS==========================")
    number_of_players = "string"
    while number_of_players not in "123456789" or len(number_of_players) != 1:
        number_of_players = input("Please enter number of players (MIN 1, MAX 9):")
    number_of_players = int(number_of_players)
    player_name_list = name_list_former(number_of_players)
    players_dict = {name: Player(name=name, filelocation=FILE_LOCATIONS, filled_paragraph=None, votes=0) for name in player_name_list} #Creates Players objects using a dict
    return players_dict

def user_response_viability_checker(user_response): #Checks if the user response makes sense. Returns false if not. Returns true if yes.
    parameters = ["-r","-c"]
    space_count = 0
    for char in user_response: #Checks for total spaces.
        if char == " ":
            space_count += 1
        else:
            continue
    if space_count == 1:    #PARCE the user_response into manageable form.
        user_response_list = user_response.split(" ")
    try:
        file_object = open(PARAGRAPH_LIST_LOCATION,"r")
    except FileNotFoundError:
        print("File {} cannot be found.".format(PARAGRAPH_LIST_LOCATION))
    else:
        linecount = 0
        for i in file_object.readlines(): #GETS TOTAL NUM OF PARAGRAPHS IN TXT FILE.
            linecount += 1
        if user_response == "recover" or user_response == "Recover" or user_response == "RECOVER": #Checks for different conditions.
            return True
        elif space_count == 0 and user_response != "recover":
            return False
        elif space_count > 1:
            return True
        elif user_response_list[0].isnumeric() == True:
            if int(user_response_list[0]) <= linecount and user_response_list[1] in parameters:
                return True
            else:
                return False
        else:
            return False
        file_object.close()
def paragraph_options(): # PRINTS PARAGRAPH OPTIONS AND 
    print("=================================GAME=OPTIONS==================================")
    print("1. START GAME by randomly choosing from list of paragraphs. (RECOMMENDED)")
    print("2. START GAME by manually choosing from list of paragraphs.")
    print("     -This option also allows you to edit the list of paragraphs.")
    user_response = "abc"
    while user_response not in "12" or len(user_response) != 1:
        user_response = input(">>> PLEASE ENTER DESIRED OPTION (1, 2):")
    return user_response
def paragraph_options_user_response_controller(user_response): #User cannot get past this until paragraph number is chosen.
    try:
        file_object = open(PARAGRAPH_LIST_LOCATION,"r")
    except FileNotFoundError:
        print("File {} cannot be found.".format(PARAGRAPH_LIST_LOCATION))
    else:
        linecount = 0
        for i in file_object.readlines(): #GETS TOTAL NUM OF PARAGRAPHS IN TXT FILE.
            linecount += 1
        file_object.close()
    paragraph_number = "9999999999"
    if user_response == "1":
        paragraph_number = random.randrange(0,linecount)
    elif user_response == "2":
        while int(paragraph_number) not in range(0,linecount + 1):
            file_object = open(PARAGRAPH_LIST_LOCATION,"r")
            linecount = 0
            for i in file_object.readlines(): #GETS TOTAL NUM OF PARAGRAPHS IN TXT FILE.
                linecount += 1
            file_object.close()
            paragraph_number = paragraph_viewer()
    return paragraph_number
def paragraph_selector(paragraph_number): #Selects and return paragraph based on the input (a number that corresponds to the paragraph's line)
    paragraph_number = int(paragraph_number)
    all_paragraphs_list = []
    try:
        file_object = open(PARAGRAPH_LIST_LOCATION,"r")
    except FileNotFoundError:
        print("File {} cannot be found.".format(PARAGRAPH_LIST_LOCATION))
    else:
        for line in file_object.readlines():
            all_paragraphs_list.append(line)
    return all_paragraphs_list[paragraph_number - 1]
def paragraph_viewer(): #Allows the user to see all paragraphs, accepts user-entered parameter for choosing/editing/adding paragraphs, executes given edits.
    print("*******************LIST*OF*PARAGRAPHS************************")
    print("The following paragraphs are included:")
    try:
        file_object = open(PARAGRAPH_LIST_LOCATION,"r")
    except FileNotFoundError:
        print("File {} cannot be found.".format(PARAGRAPH_LIST_LOCATION))
    else:
        file_lines = file_object.readlines()
        linecount = 0
        for i in file_lines: #GETS TOTAL NUM OF PARAGRAPHS IN TXT FILE.
            linecount += 1
            print("{}. {}".format(linecount,i.replace("\n","")))
        file_object.close()
        print("======EDIT=INSTRUCTION=======")
        print("● To remove a paragraph, type ' -r' following the paragraph number")
        print("     For example, typing in '2 -r' will remove the second paragraph from list.")
        print("● To manually choose a paragraph, type ' -c' following the paragraph number")
        print("     For example, typing in '2 -c' will start the game with the second paragraph from list")
        print("● To add a paragraph, simply type in your desired paragraph.")
        print("     For example, typing in 'He was not willing to VERB his ADJ NOUN.' will add this sentence to the list.")
        print("     Please only use VERB, ADJ, and NOUN as placeholders!")
        print("● To recover default list, type in 'recover' (Try this if you messed up the list)")
        print(">>>To continue with the game, you MUST select a paragraph by entering a '[paragraph number] -c' command.<<<")
        print("=============================")
        user_input = "abc -c"
        while user_response_viability_checker(user_input) == False:       #Asks for user response
            user_input = input(">>>> PLEASE ENTER DESIRED OPTION:")
        user_input_list = user_input.split(" ")
        if len(user_input_list) > 1 and user_input_list[1] == "-c":                      #Returns line number if user enters -c
            return user_input_list[0]
        elif len(user_input_list) > 1 and user_input_list[1] == "-r":                    #delete selected line if user enters -r
            writable_file = open(PARAGRAPH_LIST_LOCATION,"w")
            for line in file_lines:
                if line != file_lines[int(user_input_list[0])-1]:
                    writable_file.write(line)
            writable_file.close()
            return "9999999999"
        elif len(user_input_list) > 2:             #Add new paragraph to txt file. 
            if blank_counter(user_input) == 0:
                input("***Sorry, your paragraph must contain at least 1 placeholder word. Press Enter to continue...")
                return "99999999"
            else:
                user_defined_paragraph = " ".join(user_input_list)
                writable_file = open(PARAGRAPH_LIST_LOCATION,"w")
                for line in file_lines:
                    writable_file.write(line)
                writable_file.write("\n" + user_defined_paragraph)
                writable_file.close()
                return "999999999"
        elif user_input == "recover" or user_input == "RECOVER" or user_input == "Recover":
            user_input_2 = input("""***CONFIRMATION: Recovering the default list will eliminate all user changes to the 
            list permanently. Are you sure you want to do this? (Y/N):""")
            if user_input_2 in "Yy" and len(user_input_2) == 1:
                recover_list()
                return "9999999999"
            else:
                return "9999999999"
def recover_list():                                       #RECOVERS para list
    writable_file = open(PARAGRAPH_LIST_LOCATION,"w")
    for item in RECOVER_LIST:
        writable_file.write(item)
    writable_file.close()
def blank_counter(paragraph_chosen): #Counts the total number of items that the user needs to enter. Returns a number.
    paragraph_word_list = paragraph_chosen.split(" ")
    return_value = 0
    for word in paragraph_word_list:
        if "NOUN" in word or "VERB" in word or "ADJ" in word:
            return_value += 1
    return return_value
def filled_paragraph_generator(paragraph_chosen,chosen_words): #returns filled para.
    chosen_word_list = chosen_words.split(" ")
    paragraph_chosen_list = paragraph_chosen.split(" ")
    chosen_word_index = 0
    new_list = []
    for word in paragraph_chosen_list:
        if "NOUN" in word or "ADJ" in word or "VERB" in word:
            replacement_string = "[" + chosen_word_list[chosen_word_index] + "]"
            word = word.replace("NOUN",replacement_string)
            word = word.replace("VERB",replacement_string)
            word = word.replace("ADJ",replacement_string)
            chosen_word_index += 1
            new_list.append(word)
        else:
            new_list.append(word)
    return_string = " ".join(new_list)
    return_string = return_string.replace("\n","")
    return return_string
def game_board(paragraph_chosen,players_dict,blank_numbers): #Prints game message. Allows users to see the chosen paragraph and enter their responses.
    print("==================================================================")
    print("GAME STARTS! The paragraph chosen is...")
    print(paragraph_chosen.replace("\n",""))
    print("==================================================================")
    for i in players_dict.items():
        prompt_statement = "● {}, your word bank is {}. Please enter your word choices in desired order.".format(i[1].name,i[1].wordbank)
        print(prompt_statement)
        eligibility = False
        while eligibility == False:
            user_input = input(">>> Please separate your words using spaces:")
            eligibility_tuple = player_word_input_eligibility_checker(i[1].wordbank,user_input,blank_numbers)
            false_message = eligibility_tuple[1]
            if false_message != None:
                print(false_message)
            eligibility = eligibility_tuple[0]
        i[1].filled_paragraph = filled_paragraph_generator(paragraph_chosen,user_input) #Determines the .filled_paragraph attribute of each Player class object.
def player_word_input_eligibility_checker(player_wordbank,player_inputs,blank_numbers):
    """
    Checks to see if...
        blank_numbers = len(player_inputs)
        all of the words in player_input list is in player's wordbank
    Returns...
        True or false.
        If false, why is it false?
    """
    player_input_list = player_inputs.split(" ")    
    if len(player_input_list) != blank_numbers:
        return (False, "***Sorry, you did not enter the correct amount of words.")
    for i in player_input_list:
        if i not in player_wordbank:
            return (False, "***Sorry, please only enter the words that appeared in your wordlist.")
            break
        else:
            continue
    return (True, None)
def voting_process(players_dict):
    print("==================================================================================")
    print("TIME TO VOTE! Whose paragraph is your favorite?")
    for i in players_dict.items():
        print("● {}'s paragraph is:\n{}".format(i[1].name,i[1].filled_paragraph))
    print("==================================================================================")
    for i in players_dict.items():
        vote_elig = False
        while vote_elig == False:
            player_vote = input("● {}, Please cast your vote by entering player's name:".format(i[1].name))
            if player_vote in players_dict:
                vote_elig = True
            else:
                print("Sorry, player {} does not exist. Please reenter".format(player_vote))
        players_dict[player_vote].votes += 1
def winner_determiner(players_dict):
    votes = 0
    winner = []
    for i in players_dict.items():
        if i[1].votes >= votes:
            votes = i[1].votes
        else:
            continue
    for i in players_dict.items():
        if i[1].votes == votes:
            winner.append(i[1].name)
    return [winner,votes]
def winner_message_displayer(winner_info,players_dict):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("                  >>>>>>>>Player(s) {} WON!!<<<<<<<<<<".format(winner_info[0]))
    print("               They have accumulated the most number of votes ({})!".format(winner_info[1]))
    print("                               CONGRATULATIONS!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for i in players_dict.items():
        if i[1].name in winner_info[0]:
            print(i[1].filled_paragraph + "   ---" + i[1].name)
        else:
            continue
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

def one_game(players_dict):
    user_response = paragraph_options()
    paragraph_number = paragraph_options_user_response_controller(user_response)
    paragraph_chosen = paragraph_selector(paragraph_number)
    blank_numbers = blank_counter(paragraph_chosen)
    game_board(paragraph_chosen,players_dict,blank_numbers)
    voting_process(players_dict)
    print(players_dict)
    winner_determiner(players_dict)
    winner_info = winner_determiner(players_dict)
    winner_message_displayer(winner_info,players_dict)

def main():
    print("=====================WELCOME=TO=MAD=LIBS======================")
    print("Enter player information in the section below to start game.")
    players_dict = player_objects_former()
    play_again_response = "RandomString"
    while play_again_response not in "Nn":
        one_game(players_dict)
        play_again_response = input("Play again? (Y/N):")
        while play_again_response not in "YyNn" or len(play_again_response) != 1:
            play_again_response = input("Play again? (Y/N):")
        if play_again_response in "Nn":
            break
        else:
            user_input_2 = "RandomString"
            possible_response = "YyNn"
            while user_input_2 not in possible_response or len(user_input_2) != 1:
                user_input_2 = input("Play with the same people? (Y/N):")
            if user_input_2 in "Yy": #Clear all information but Player.name
                for i in players_dict.items():
                    i[1].votes = 0
                    i[1].filled_paragraph = None
                    i[1].wordbank = i[1].word_bank_generator(FILE_LOCATIONS)
            elif user_input_2 in "Nn": #Clear all information of players.
                for i in players_dict.items():
                    i[1].name = None
                    i[1].votes = 0
                    i[1].filled_paragraph = None
                    i[1].wordbank = i[1].word_bank_generator(FILE_LOCATIONS)
                players_dict = player_objects_former()
    print("Goodbye!")

if __name__ == "__main__":
    main()
