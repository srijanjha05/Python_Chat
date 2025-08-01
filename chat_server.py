import socket
import threading

clients = []
nicknames = {}

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)
            client.close()

def handle_client(client):
    try:
        nickname = client.recv(1024).decode('utf-8')
        nicknames[client] = nickname
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        print(f"[JOIN] {nickname} connected.")

        while True:
            message = client.recv(1024)
            if not message:
                break
            full_message = f"{nickname}: {message.decode('utf-8')}"
            broadcast(full_message.encode('utf-8'))
            print(full_message)
    except:
        pass
    finally:
        if client in clients:
            clients.remove(client)
        left_name = nicknames.get(client, "Unknown")
        broadcast(f"{left_name} left the chat.".encode('utf-8'))
        print(f"[LEAVE] {left_name} disconnected.")
        client.close()

def admin_broadcast():
    while True:
        msg = input()
        if msg:
            broadcast(f"[SERVER]: {msg}".encode('utf-8'))
            print(f"[SERVER]: {msg}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen()
    print("✅ Server started on port 12345...")

    threading.Thread(target=admin_broadcast, daemon=True).start()

    while True:
        client, _ = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    start_server()