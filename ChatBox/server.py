import tkinter as tk
from tkinter import messagebox
import socket
import threading
import sqlite3

# Server port, IP address, socket, language format
#ip_address = socket.gethostbyname(socket.gethostname())
#ip_address = '127.0.0.1'
ip_address = ''
port = 56574
address = (ip_address, port)
format_server = "utf-8"

# Create a socket, using IPv4 and TCP; Bind socket with IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)

# List of clients entering the chat, and name of the clients
clients = []
clients_names = []

# Server GUI
window = tk.Tk()
window.title("ChatBox Server")

# Connect and disconnect button
top_block = tk.Frame(window)
# Connect button
button_connect = tk.Button(top_block, text="Connect", command=lambda: start_server())
button_connect.pack(side=tk.LEFT)
# Disconnect button
button_disconnect = tk.Button(top_block, text="Disconnect", command=lambda: stop_server(), state=tk.DISABLED)
button_disconnect.pack(side=tk.LEFT)
top_block.pack(side=tk.TOP, pady=(5, 0))

# Display labels with server information
middle_block = tk.Frame(window)
label_host = tk.Label(middle_block, text="Host:0.0.0.0")
label_host.pack(side=tk.LEFT)
label_port = tk.Label(middle_block, text="Port:0000")
label_port.pack(side=tk.LEFT)
middle_block.pack(side=tk.TOP, pady=(5, 0))

# Display box of clients
bottom_block = tk.Frame(window)
tk.Label(bottom_block, text="Clients:").pack()
scrollbar = tk.Scrollbar(bottom_block)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(bottom_block, height=15, width=30, font=14)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollbar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollbar.set, background="black", highlightbackground="gray", state="disabled")
bottom_block.pack(side=tk.BOTTOM, pady=(5, 10))


# Start server function
def start_server():
    # Switch button status
    button_connect.config(state=tk.DISABLED)
    button_disconnect.config(state=tk.NORMAL)
    # Update host and port
    label_host["text"] = "Host: " + ip_address
    label_port["text"] = "Port: " + str(port)

    # Listen to socket
    server_socket.listen(5)

    # Start accepting clients
    threading.Thread(target=accepting_clients).start()


# Stop server function
def stop_server():
    # Switch button status
    button_connect.config(state=tk.NORMAL)
    button_disconnect.config(state=tk.DISABLED)

    # Close socket
    server_socket.close()


# Collect client's IP addresses, and accept the connection
def accepting_clients():
    while True:
        try:
            # Get ip address of client, accepting connection
            client, client_ip = server_socket.accept()
            client.send('Welcome To The Dark Side'.encode(format_server))
            client_info = client.recv(1024).decode(format_server).split(", ", 1)

            # Get username of client; Look for username and password in database
            users_db = sqlite3.connect('ChatBoxUsers.db')

            approve = "Dark Side Failed"
            cursor = users_db.execute("SELECT Username, Password\nFROM ChatBoxUser\nWHERE Username = '" + client_info[0] + "'")

            for row in cursor:
                if row[0] == client_info[0]:
                    if row[1] == client_info[1]:
                        approve = "Dark Side Passed"

            client.send(approve.encode(format_server))

            if approve == 'Dark Side Passed':
                # Add client name to list
                clients_names.append(client_info[0])
                clients.append(client)
                update_list()

                # Inform server of client
                to_everyone(f'Welcome {client_info[0]} everyone!'.encode(format_server))

                # Thread to start receiving messages from client
                threading.Thread(target=client_message, args=(client,)).start()
        except:
            break


# Update client list display
def update_list():
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for i in clients_names:
        tkDisplay.insert(tk.END, i + "\n")

    tkDisplay.config(state=tk.DISABLED)


# When client send a message, try sending it to everyone
def client_message(client):
    while True:
        message = client.recv(1024)

        # Break if one is detected
        if not message:
            break
        elif str(message).split(': ', 1)[0] == "Dark Side Exit":
            break

        to_everyone(message)

    # Get client info
    index = client_index(client)
    client_username = clients_names[index]
    # Remove client info
    del clients[index]
    del clients_names[index]
    # Close client socket and update list
    client.close()
    update_list()

    # Inform server of client
    to_everyone(f'{client_username} left!'.encode(format_server))


# Send message to everyone on server
def to_everyone(message):
    for client in clients:
        client.send(message)


# Get the index of the client from the list
def client_index(client):
    index = 0

    for i in clients:
        if i == client:
            break
        index = index + 1

    return index


# If user tries to exit window, use pop up
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to end the chatroom?"):
        server_socket.close()
        window.destroy()


# Loop window
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
