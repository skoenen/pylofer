from pylofer import Configuration
from pylofer.storage import Storage

from SocketServer import ThreadingUDPServer, ThreadingUnixDatagramServer

from pylofer.util.socket_client import client_from_url


__all__ = ['ServerStorage']

class ServerStorage(Storage):
    def __init__(self, config=None):
        self.config = config if config is not None else Configuration()

class ServerStorageClient(object):
    def __init__(self, config=None):
        self.config = config if config is not None else Configuration()

        self.endpoint = self.config.endpoint
        self.client = client_from_url(self.endpoint)

    def send(self, measure):
        self.sock.send(str(measure))


class ServerStorageServer(ThreadingMixIn, object):
    def __init__(self, config=None):
        self.config = config if not config is None else Configuration()

        self.endpoint = self.config.endpoint
        if self.endpoint.scheme == "udp":
            self.server = TUDPServer(
                    self.endpoint.host, self.endpoint.port,
                    ServerStorageRequestHandler)
        else:
            self.server = TUnixServer(
                    self.endpoint.path, ServerStorageRequestHandler)

        self.server.allowed_hosts = self.config.allowed_hosts
        self.server.serve_forever()

class TUDPServer(ThreadingUDPServer):
    def verify_request(self, request, client_addr):
        return True if client_addr in self.allowed_hosts else False

class TUnixServer(ThreadingUnixDatagramServer):
    def verify_request(self, request, client_addr):
        return True if client_addr in self.allowed_hosts else False

class ServerStorageRequestHandler(DatagramRequestHandler):
    def handle(self):
        pass

