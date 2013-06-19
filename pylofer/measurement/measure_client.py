import socket
import threading

__all__ = ['MeasureClient']

class MeasureClient(object):
    def __init__(self, config={}):
        self.port = getattr(config, "port", 60000)
        self.host = getattr(config, "host", "")

        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

    def send(self, measure):
        self.sock.send(str(measure))

