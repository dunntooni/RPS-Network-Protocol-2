#############################################################################
# Program:
#    Lab PythonRPS_Server, Computer Networking
#    Brother Jones, CSE 354
# Author:
#    Isaac Dunn
# Summary:
#    This is the server for a Rock, Paper, Scissors game. It takes a simple input
# representing rock, paper, or scissors, and returns a victory, defeat or
# draw message. It runs on a port specified as a program argument.
# *****************************************************************************
#
# RPS (rock/paper/scissors) Protocol Description
# ----------------------------------------------
# client 1 <<--TCP connection-->>  server
#
#          server <<---TCP connection-->> client 2
#
# client 1  --sends player 1 data (r, p, s, or q)-->> server
#
#          server <<-- sends player 2 data (r, p, s, or q) ---- client 2
#
# client 1  <<--sends player 1 results (win, lose, or draw)-- server
#
#          server --sends player 2 results (win, lose, or draw)-->> client 2
#
# Client side commands/communication sent: 'r', 'p', 's', or 'q'
# Server side commands/communication sent:
# "You chose (answer) and your opponent chose (answer). " + (one of the following:)
#    "It's a draw!"
#    "You lose. Better luck next time!"
#    "You Win!! Congratulations!"
#############################################################################
#
# Changes made to my code for the Lab 3 Take-2:
#   I spaced out my code for increased readability. Added a few comments.
#   Moved a print statement from line 135 to line 130 so it displays even if
#   one of the users decides to quit.
#
#############################################################################


import sys
from socket import *

DEFAULT_VALUE = 6789

if len(sys.argv) != 2:
    print('Usage: rpsServer_header.py port')
    sys.exit(1)

# Returns a list of length 2. The first is the result for client 1, and the
# second for client 2. Again, not very elegant, but it'll do.


def RPS(client1RPS, client2RPS):

    draw = "It's a draw!"
    lose = "You lose. Better luck next time!"
    win = "You Win!! Congratulations!"

    if client1RPS == client2RPS:
        return [draw, draw]
    if client1RPS == 'r':
        if client2RPS == 'p':
            return [lose, win]
        else:
            return [win, lose]
    elif client1RPS == 'p':
        if client2RPS == 'r':
            return [win, lose]
        else:
            return [lose, win]
    elif client1RPS == 's':
        if client2RPS == 'r':
            return [lose, win]
        else:
            return [win, lose]
    return [draw, draw]


serverPort = int(sys.argv[1])
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
print('The Server is ready to receive')

try:
    # Do an initial connect. This isn't necessary, but makes sense in my head.
    print('Server waiting for two clients to connect ...')  # Get first client
    connectionSocket, addr = serverSocket.accept()
    req1 = connectionSocket.recv(1024).decode()

    if req1 != "CON":
        print("ERROR: Data sent from client is bad. Value rps1: ", req1)
        response = "ERR"
    else:
        response = "ACK"

    connectionSocket.send(response.encode())
except:
    print("Error interacting with client 1")

try:
    print("Server waiting for another client to connect ...")  # Get second client
    connectionSocket2, addr2 = serverSocket.accept()
    req2 = connectionSocket2.recv(1024).decode()

    if req2 != "CON":
        print("ERROR: Data sent from client is bad. Value rps2: ", req2)
        response2 = "ERR"
    else:
        response2 = "ACK"

    connectionSocket2.send(response2.encode())
except:
    print("Error interacting with client 2")


# Now, using existing connections, begin gameplay loop. Terminate when
# input 'q' is received from both clients. Things get wacky if only one
# 'q' is received.
while True:
    try:
        rps1 = connectionSocket.recv(1024).decode('ascii')
        print("Received from client1: ", rps1)
        # Check if they want to quit
        if rps1 == 'q':
            connectionSocket.close()

        rps2 = connectionSocket2.recv(1024).decode('ascii')
        print("Received from client2: ", rps2)
        # Check if they want to quit
        if rps2 == 'q':
            connectionSocket2.close()
            print("Server shutting down...")
            break

        # Set and return responses
        results = RPS(rps1, rps2)
        res1 = "You chose "+rps1 + \
            " and your opponent chose "+rps2+". "+results[0]
        res2 = "You chose "+rps2 + \
            " and your opponent chose "+rps1+". "+results[1]
        connectionSocket.send(res1.encode('ascii'))
        connectionSocket2.send(res2.encode('ascii'))

    except KeyboardInterrupt:
        print("\nClosing Server")
        serverSocket.close()
