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
# client 1 --Connection Request-->>  server
#
#          server <<---Connection Request-- client 2
#
# client 1 <<--- OK -- server --OK-->> client 2
#
# client 1  --sends player 1 data (r, p, or s)-->> server
#
#          server <<-- sends player 2 data (r, p, or s) ---- client 2
#
# client 1  <<--sends player 1 results (win, lose, or draw)-- server
#
#          server --sends player 2 results (win, lose, or draw)-->> client 2
#
# Client side commands/communication sent: 'r', 'p', or 's'
# Server side commands/communication sent:
# "You chose (answer) and your opponent chose (answer). " + (one of the following:)
#    "It's a draw!"
#    "You lose. Better luck next time!"
#    "You Win!! Congratulations!"
#
# When one player disconnects, the program notifies the other player,
# closes both connections, and then terminates.
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


def convertToWord(letter):
    if letter == 'r':
        return 'rock'
    elif letter == 'p':
        return 'paper'
    else:
        return 'scissors'


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
    response1 = "OK"
except:
    print("Error receiving from client 1")
    response1 = "ERR"

try:
    print("Server waiting for another client to connect ...")  # Get second client
    connectionSocket2, addr2 = serverSocket.accept()
    req2 = connectionSocket2.recv(1024).decode()
    response2 = "OK"
except:
    print("Error receiving from client 2")
    response2 = "ERR"

connectionSocket.send(response1.encode())
connectionSocket2.send(response2.encode())


# Now, using existing connections, begin gameplay loop. Terminate when
# input 'q' is received from both clients. Things get wacky if only one
# 'q' is received.
while True:
    try:
        rps1 = connectionSocket.recv(1024).decode('ascii')
        print("Received from client1:", rps1)

        rps2 = connectionSocket2.recv(1024).decode('ascii')
        print("Received from client2:", rps2)

        # Check if a player has disconnected
        if rps1 == "":
            raise Exception("1")
        if rps2 == "":
            raise Exception("2")

        rps1word = convertToWord(rps1)
        rps2word = convertToWord(rps2)
        # Set and return responses
        results = RPS(rps1, rps2)
        res1 = "You chose "+rps1word + \
            ", and your opponent chose "+rps2word+". "+results[0]
        res2 = "You chose "+rps2word + \
            ", and your opponent chose "+rps1word+". "+results[1]
        connectionSocket.send(res1.encode('ascii'))
        connectionSocket2.send(res2.encode('ascii'))

    except KeyboardInterrupt:
        print("\nClosing Server")
        serverSocket.close()

    except Exception as e:
        print("Player " + str(e) + " has disconnected. Notifying other player.")
        if int(str(e)) == 2:
            connectionSocket.send(
                'ERR'.encode('ascii'))
        else:
            connectionSocket2.send(
                'ERR'.encode('ascii'))

        connectionSocket.close()
        connectionSocket2.close()
        sys.exit(11)
