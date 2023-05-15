import tkinter as tk
import time
from socket import *
from threading import Thread

# Create a new window
window = tk.Tk()
window.title("Rock Paper Scissors")

# Create labels
title_label = tk.Label(window, text="Rock Paper Scissors", font=("Helvetica", 18))
score_label = tk.Label(window, text="Score: 0 - 0", font=("Helvetica", 12))
result_label = tk.Label(window, font=("Helvetica", 12), pady=10)

# Create buttons
# Create buttons with colors and backgrounds
rock_button = tk.Button(window, text="Rock", padx=10, pady=5, font=("Helvetica", 12),
                        command=lambda: send_choice("rock"), fg="white", bg="#333333")
paper_button = tk.Button(window, text="Paper", padx=10, pady=5, font=("Helvetica", 12),
                         command=lambda: send_choice("paper"), fg="white", bg="#0074D9")
scissors_button = tk.Button(window, text="Scissors", padx=10, pady=5, font=("Helvetica", 12),
                            command=lambda: send_choice("scissors"), fg="white", bg="#FF4136")

# Position the widgets using grid geometry manager
title_label.grid(row=0, column=0, columnspan=3)
score_label.grid(row=1, column=0, columnspan=3)
result_label.grid(row=2, column=0, columnspan=3)
rock_button.grid(row=3, column=0)
paper_button.grid(row=3, column=1)
scissors_button.grid(row=3, column=2)

# Initialize scores
user_score = 0
computer_score = 0

score_label.config(text=f"Score: {user_score} - {computer_score}")

# Connect to server
s = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
port = 7002
s.connect((host, port))

# Send user choice to server
def send_choice(choice):
    s.send(choice.encode('utf-8'))

# Receive game results from server
def receive_results():
    global user_score
    global computer_score
    global user_choice
    while True:
        if window.winfo_exists():
            results = s.recv(1024).decode()
            if results.startswith("Score:"):
                scores = results.split(": ")[1]
                if "Computer wins!" in scores or "You win!" in scores:
                    user_score, computer_score = 0, 0
                    if "Computer wins!" in scores:
                        result_label.config(text="Computer wins!")
                    else:
                        result_label.config(text="You win!")
                    score_label.config(text=f"Final Score: {scores}")
                    window.after(5000, window.destroy)  # Close the window immediately when one of the players wins
                    break
                else:
                    user_score, computer_score = map(int, scores.split(" - "))
                    score_label.config(text=results)
            else:
                user_choice = results.split()[2]
                result_label.config(text=f" {results}")
        else:
            break
        
# Start a new thread to receive game results from server
t = Thread(target=receive_results)
t.start()

# Start the main event loop
window.mainloop()