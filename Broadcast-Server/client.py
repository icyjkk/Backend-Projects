import argparse
import socket
import threading

HOST = '127.0.0.1'  # Localhost address
PORT = 8080         # Server port

def receive_messages(client_socket):
    """
    Listens for incoming messages from the server and prints them.

    Parameters:
    - client_socket (socket.socket): The socket connected to the server.
    """
    try:
        while True:
            # Receive message from the server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                # If an empty string is received, the server has closed the connection
                print("Server has closed the connection.")
                break
    except Exception as e:
        print(f"Error receiving message: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

def connect_command(args):
    """
    Connects to the server and handles sending and receiving messages.

    Parameters:
    - args: Command-line arguments (not used in this script).
    """
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Start a thread to listen for incoming messages from the server
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.daemon = True  # Allows the thread to exit when the main program exits
        receive_thread.start()

        # Main loop to send messages to the server
        while True:
            message = input()  # Get user input
            if message:
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break
    except ConnectionRefusedError:
        print(f"Unable to connect to server at {HOST}:{PORT}. Is the server running?")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Client has been shut down.")

