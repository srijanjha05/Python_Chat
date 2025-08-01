import socket
import threading

class ChatClient:
    def __init__(self):
        self.client = None
        self.receive_thread = None
        self.is_connected = False
        self.gui_callback = None

    def connect(self, host, port, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((host, port))
            self.client.send(name.encode('utf-8'))
            self.is_connected = True
            self.receive_thread = threading.Thread(target=self.receive)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            return True
        except:
            return False

    def receive(self):
        while self.is_connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if self.gui_callback:
                    self.gui_callback(message)
            except:
                break

    def send(self, message):
        if self.is_connected:
            self.client.send(message.encode('utf-8'))

    def disconnect(self):
        self.is_connected = False
        try:
            self.client.close()
        except:
            pass