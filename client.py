import threading
import socket
import tkinter as tk

def send_name():
    global name
    name = name_entry.get()
    name_entry.config(state="disabled")
    submit_button.config(state="disabled")
    client.send(name.encode('ascii'))

def send_message():
    message = message_entry.get()
    message_entry.delete(0, tk.END)  # Clear the message entry field
    client.send(f'{name}: {message}'.encode('ascii'))

# Create a GUI window for the client
window = tk.Tk()
window.title("Chat Application")

# Create a label for the name input
name_label = tk.Label(window, text="Enter your name:")
name_label.pack()

# Create an entry field for the name
name_entry = tk.Entry(window, width=50)
name_entry.pack()

# Create a "Submit" button for the name
submit_button = tk.Button(window, text="Submit", command=send_name)
submit_button.pack()

# Create a text widget to display messages
chat_text = tk.Text(window, height=20, width=50)
chat_text.pack()

# Create an entry widget to type messages
message_entry = tk.Entry(window, width=50)
message_entry.pack()

# Create a "Send" button for messages
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            chat_text.insert(tk.END, message + "\n")
        except:
            print("An error occurred.")
            client.close()
            break

recv_thread = threading.Thread(target=receive)
recv_thread.start()

# Start the GUI main loop
window.mainloop()
