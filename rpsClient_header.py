#############################################################################
# Program:
#    Lab PythonRPS_Client, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Isaac Dunn
# Summary:
#    This is the client for a Rock, Paper, Scissors game. It sends a simple input
# representing rock, paper, or scissors, and receives a victory, defeat or
# draw message. It takes a header and a port number as program arguments.
#############################################################################

import sys
from socket import *

if len(sys.argv) != 3:
    print('Usage: rpsClient_header.py hostname port')
    sys.exit(1)

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # Do an initial connect. This isn't necessary, but makes sense in my head.
    clientSocket.send("CON".encode('ascii'))
    print("Waiting for a another player to connect...")
    if clientSocket.recv(1024).decode('ascii') != "OK":
        raise Exception("The server didn't acknowledge the request.")
    print("Connection established!")
    # Get user input. There's probably a more elegant way to do this than
    # doing it twice. Too bad!
    rps = "lol"

    while not rps in ['r', 'p', 's', 'q']:
        rps = input('Input (r)ock, (p)aper, (s)cissors, or (q)uit: ')

    while rps != 'q':
        clientSocket.send(rps.encode('ascii'))
        print("Waiting for the other player to choose...")

        # Wait for response
        response = clientSocket.recv(1024).decode('ascii')
        if response == 'ERR':
            print('The other player has disconnected.')
            break
        print(response)
        rps = "lol"
        while not rps in ['r', 'p', 's', 'q']:
            rps = input('Input (r)ock, (p)aper, (s)cissors, or (q)uit: ')

    # Gameplay loop is complete. Send quit message and exit.
    print("Thanks for playing!")
    clientSocket.close()
    sys.exit(2)

# All the below code is stolen from the client in lab 1.
except KeyboardInterrupt:
    print('\nClosing Client')
    clientSocket.close()

except gaierror as e:
    print('Bad hostname: ', e)
    sys.exit(10)

except ConnectionRefusedError as e:
    # This is most likely, a bad port number
    print('Bad port number: ', e)

# The following could be used to figure out which type of exception occurred
# in order to put in specific error handling for it.  Thanks:
# https://stackoverflow.com/questions/19192891/how-to-handle-connectionerror-in-python
except Exception as e:
    print('Exception: ', type(e), type(e).__qualname__, e)
    sys.exit(11)
