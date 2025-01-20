# Broadcast Server

A simple Python-based broadcast server for message sharing between multiple clients. This application enables a server to broadcast messages from one client to all other connected clients in real-time. It includes both server and client functionalities and uses a command-line interface to manage connections.

---

## Features

- **Server**:
  - Handles multiple client connections simultaneously.
  - Broadcasts messages from one client to all others.
  - Notifies clients of new connections and disconnections.

- **Client**:
  - Connects to the server and sends messages.
  - Receives and displays messages broadcast by the server.

- **Command-line Interface (CLI)**:
  - Simplifies running the server and connecting clients.
  - Provides commands to start the server and connect clients.

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Ensure you have Python 3.7+ installed on your system.

3. Install any required dependencies (none currently required).

---

## Usage

### Starting the Server

Run the following command to start the server:
```bash
python cli.py start
```

- The server listens on `127.0.0.1:8080` by default.

### Connecting a Client

Run the following command to connect a client to the server:
```bash
python cli.py connect
```

- After connecting, type messages to broadcast them to other connected clients.
- To disconnect, simply close the client process or press `Ctrl+C`.

---

## How It Works

- **Server** (`server.py`):
  - Listens for client connections on the specified host and port.
  - Handles client communication in separate threads to enable concurrency.
  - Broadcasts messages received from one client to all other connected clients.

- **Client** (`client.py`):
  - Connects to the server and starts a thread to listen for incoming messages.
  - Allows the user to input messages, which are sent to the server.

- **CLI** (`cli.py`):
  - Acts as an entry point to manage the server and client functionalities using subcommands.

---

## Example

1. Start the server:
   ```bash
   python cli.py start
   ```
   Output:
   ```
   Server started on 127.0.0.1:8080
   ```

2. Connect a client:
   ```bash
   python cli.py connect
   ```
   Output:
   ```
   Connected to server at 127.0.0.1:8080
   ```

3. Send messages between clients. Messages will be displayed in real-time across all connected clients.

---



## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or fixes.

