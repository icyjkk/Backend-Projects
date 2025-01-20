import socket
import sys
import threading

# List to store client connections
clients = []

HOST = '127.0.0.1'  # Localhost address
PORT = 8080         # Server port

def broadcast_message(message, sender_socket=None):
    """
    Sends a message to all connected clients except the sender.

    Parameters:
    - message (str): The message to be sent.
    - sender_socket (socket.socket, optional): The socket of the client who sent the message.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending message to a client: {e}")
                client.close()
                clients.remove(client)

def handle_client(client_socket, client_address):
    """
    Handles communication with a connected client.

    Parameters:
    - client_socket (socket.socket): The socket representing the client connection.
    - client_address (tuple): The address of the connected client.
    """
    print(f"New connection: {client_address}")
    clients.append(client_socket)
    try:
        while True:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{client_address}: {message}")
                # Broadcast the received message to other clients
                broadcast_message(f"{client_address}: {message}", sender_socket=client_socket)
            else:
                # No message means the client has disconnected
                break
    except Exception as e:
        print(f"Error handling {client_address}: {e}")
    finally:
        print(f"{client_address} disconnected.")
        clients.remove(client_socket)
        # Notify other clients about the disconnection
        broadcast_message(f"{client_address} has disconnected.", sender_socket=client_socket)
        client_socket.close()

def start_server():
    """
    Starts the socket server and listens for incoming client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")
    try:
        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            # Create and start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()
        # Close all client connections gracefully
        for client in clients:
            client.close()

if __name__ == "__main__":
    start_server()
