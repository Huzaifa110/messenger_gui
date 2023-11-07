import threading
import socket
import tkinter as tk

host = '127.0.0.1'
port = 8000

# Create a GUI window for the server
server_window = tk.Tk()
server_window.title("Server Status")

# Create a label to display server status
status_label = tk.Label(server_window, text="Server is listening...", font=("Arial", 12))
status_label.pack()

# Create a text widget to display server activity
activity_text = tk.Text(server_window, height=20, width=50)
activity_text.pack()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message, currentClient=None):
    for client in clients:
        # if client != currentClient:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            names.remove(name)
            broadcast(f'{name} left the chat'.encode('ascii'))
            print(f'{name} left the chat.')
            break

def receive():
    while True:
        client, address = server.accept()
        activity_text.insert(tk.END, f'Connected with {str(address)}\n')
        activity_text.see(tk.END)

        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        activity_text.insert(tk.END, f'Name of Client is {name}.\n')
        activity_text.see(tk.END)

        broadcast(f'{name} joined the chat'.encode('ascii'), client)
        client.send('Connected to the server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start the server in a separate thread
server_thread = threading.Thread(target=receive)
server_thread.start()

# Start the Tkinter GUI main loop for the server
server_window.mainloop()
