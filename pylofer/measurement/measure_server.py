import socket
import threading

from measurement import Measurement

__all__ = ['MeasureServer']

class MeasureServer(object):
    allowed_hosts = ["127.0.0.1", "::1"]

    def __init__(self, config={}):
        self.port = getattr(config, "port", 60000)
        self.host = getattr(config, "host", "")

        self.allowed_hosts = getattr(config, "allowed_hosts", self.allowed_hosts)

        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.handle_thread = threading.Thread(target=self._handle,
                                              name="handle_incoming_measurements")

        self.event_exit = threading.Event()


    def _handle(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            if addr[0] in self.allowed_hosts:
                measure = Measurement(data=data)
                measure.save()

            if self.event_exit.is_set():
                break

    def quit(self):
        self.event_exit.set()

    def serv(self):
        self.handle_thread.run()
