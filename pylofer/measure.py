import socket
import threading
import json

from storage import FileStorage

class Measurement(object):
    def __init__(self, config={}, obj={}):
        pass

class MeasureClient(object):
    def __init__(self, config={}):
        self.port = getattr(config, "port", 60000)
        self.host = getattr(config, "host", "")

        self.allowed_hosts = getattr(config, "allowed_hosts", ["127.0.0.1"])
        self.storage = getattr(config, "storage", FileStorage())

        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

    def send(self, measure):
        obj = json.dumps(measure)
        self.sock.send(obj)

class MeasureServer(object):
    def __init__(self, config={}):
        self.port = getattr(config, "port", 60000)
        self.host = getattr(config, "host", "")

        self.allowed_hosts = getattr(config, "allowed_hosts", ["127.0.0.1"])
        self.storage = getattr(config, "storage", FileStorage())

        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        threading.Thread(target=_handle, name="handle_incoming_measurements")

    def _handle(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            if addr[0] in self.allowed_hosts:
                obj = json.loads(data)
                measure = Measurement(obj)

                storage.save(measure)

