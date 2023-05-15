import random
from socket import *
from threading import Thread

# Game choices
choices = ['rock', 'paper', 'scissors']

# Initialize scores
user_score = 0
computer_score = 0

# Game function
def play_game(client_socket):
    global user_score
    global computer_score
    while True:
        # Receive user choice
        user_choice = client_socket.recv(1024).decode()
        if not user_choice:
            break

        # Get computer choice
        computer_choice = random.choice(choices)

        # Determine winner
        if user_choice == computer_choice:
            result = f"Both players selected {user_choice}. It's a tie!"
        elif user_choice == 'rock':
            if computer_choice == 'scissors':
                user_score += 1
                result = f"Rock smashes scissors! You scored 1 point."
            else:
                computer_score += 1
                result = f"Paper covers rock! Computer scored 1 point."
        elif user_choice == 'paper':
            if computer_choice == 'rock':
                user_score += 1
                result = f"Paper covers rock! You scored 1 point."
            else:
                computer_score += 1
                result = f"Scissors cuts paper! Computer scored 1 point."
        elif user_choice == 'scissors':
            if computer_choice == 'paper':
                user_score += 1
                result = f"Scissors cuts paper! You scored 1 point."
            else:
                computer_score += 1
                result = f"Rock smashes scissors! Computer scored 1 point."

        # Send game results to client
        client_socket.send(result.encode('utf-8'))

        # Send updated scores to client
        score_string = f"Score: {user_score} - {computer_score}"
        client_socket.send(score_string.encode('utf-8'))

        # End game if either player reaches 3 points
        if user_score == 3:
            client_socket.send("You win!".encode('utf-8'))
            break
        elif computer_score == 3:
            client_socket.send("Computer wins!".encode('utf-8'))
            break

# Start server
s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 7002
s.bind((host, port))
s.listen(1)
print("Server is running...")

while True:
    # Wait for client connection
    client_socket, addr = s.accept()
    print(f"Connection from {addr} established.")

    # Start a new thread for each game
    t = Thread(target=play_game, args=(client_socket,))
    t.start()