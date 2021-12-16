import tkinter as tk
from tkinter import messagebox
import socket
import threading

# Server port, language format, and client name
port = 56574
format_client = "utf-8"
name = ''
# Create a socket, using IPv4 and TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Client GUI
window = tk.Tk()
window.title("ChatBox Client")

# Entry username, password, server IP and connect button
top_block = tk.Frame(window)
# Server IP
label_server = tk.Label(top_block, text="Server IP:", font=14)
label_server.pack(side=tk.TOP)
entry_ip = tk.Entry(top_block, font=14)
entry_ip.pack(side=tk.TOP, pady=(5, 10))
# Username
label_name = tk.Label(top_block, text="Username:", font=14)
label_name.pack(side=tk.TOP)
entry_name = tk.Entry(top_block, font=14)
entry_name.pack(side=tk.TOP, pady=(5, 10))
# Password
label_password = tk.Label(top_block, text="Password:", font=14)
label_password.pack(side=tk.TOP)
entry_password = tk.Entry(top_block, font=14)
entry_password.pack(side=tk.TOP, pady=(5, 10))
# Connect button
button_connect = tk.Button(top_block, text="Connect", font=14, command=lambda: connect())
button_connect.pack(side=tk.TOP, pady=(5, 10))
top_block.pack(side=tk.TOP, padx=(15, 15), pady=(10, 10))

# Display box and scrollbar
middle_block = tk.Frame(window)
# Scrollbar
scrollbar = tk.Scrollbar(middle_block)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# Display box
text_display = tk.Text(middle_block, height=20, width=40, font=14)
text_display.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollbar.config(command=text_display.yview)
text_display.config(yscrollcommand=scrollbar.set, background="black", highlightbackground="grey", state="disabled")
middle_block.pack_forget()

# Text message
bottom_block = tk.Frame(window)
text_message = tk.Text(bottom_block, height=1.25, width=40, font=14)
text_message.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
text_message.config(highlightbackground="grey", state="disabled")
text_message.bind("<Return>", (lambda event: send_message(text_message.get('1.0', tk.END))))
bottom_block.pack_forget()


# Making sure entry name isn't empty
def connect():
    if len(entry_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You must enter your name")
    else:
        connect_to_server()


# Setup client, connect to server
def connect_to_server():
    try:
        # Server ip address and port, connect to remote socket
        address = (entry_ip.get(), port)
        client_socket.connect(address)

        # Thread to receive messages
        threading.Thread(target=message_incoming).start()
    except:
        # If server isn't up, info user
        tk.messagebox.showerror(title="ERROR!!!", message="Server may be Unavailable. Try again later")


# When a message comes in
def message_incoming():
    global name

    while True:
        try:
            # Get message from server
            message = client_socket.recv(1024).decode(format_client)

            # If any, exit
            if not message:
                break

            # In start up, return username and password
            if message == 'Welcome To The Dark Side':
                client_info = entry_name.get() + ", " + entry_password.get()
                client_socket.send(client_info.encode(format_client))
            elif message == 'Dark Side Passed':
                # Set name
                name = entry_name.get()
                # Remove unnecessary widgets
                top_block.destroy()
                # Set up message app
                middle_block.pack(side=tk.TOP)
                bottom_block.pack(side=tk.BOTTOM)
                text_message.config(state=tk.NORMAL)
            elif message == 'Dark Side Failed':
                # If login isn't right, info user
                tk.messagebox.showerror(title="ERROR!!!", message="Your login credentials isn't correct. Try again")
                break
            else:
                # Add message to text window
                text_display.config(state=tk.NORMAL)
                text_display.insert(tk.END, message + "\n")
                text_display.config(state=tk.DISABLED)
                text_display.see(tk.END)
        except:
            # End thread
            break


# When client wants to send a message to everyone
def send_message(message):
    global name
    # Get message entry
    message = message.replace('\n', '')
    # Erase message entry
    text_message.delete('1.0', tk.END)

    # End program if user enters exit
    if message == "Dark Side Exit":
        client_socket.close()
        window.destroy()
    else:
        # Message setup
        format_message = f'{name}: {message}'
        # Send message
        client_socket.send(format_message.encode(format_client))


# If user tries to exit window, use pop up
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to leave the chatroom?"):
        send_message("Dark Side Exit")


# Loop window
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
