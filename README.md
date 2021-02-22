# MAD LIBS MULTIPLAYER

## GENERAL INFORMATION
This program is written for the purpose of practicing Python skills.

---
## PROGRAM DESCRIPTION
This repository contains multiple files: server.py, multiplayer.py, singleplayer.py, and various .txt files under the /wordbank folder.
- server.py allows you to host a local server for a madlibs game.
- multiplayer.py is the client program for the local server.
- singleplayer.py allows you to play the single player version of the game and edit the blank paragraph list.
- the /wordbank folder stores the .txt files for blank paragraphs and word banks.

---
## CONFIGURATION
- These programs are only campatible with Python3.
- These programs need at least one word bank text file, only one sample paragraphs and only one recovery text file to run properly.
- Edit the "FILE_LOCATIONS" list, the "PARAGRAPH_LIST_LOCATION" string, or the "RECOVER_LIST_LOCATION" string to change the respective .txt file location.
- The multiplayer.py and server.py files are not dependent on each other. Both can run properly without the other file being in the same directory.
- Both multiplayer.py and server.py are dependent on the various .txt files under /wordbank folder and the singleplayer.py program, which stores important functions that are needed for either multiplayer.py or server.py to run properly.