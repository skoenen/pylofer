from socketserver import ThreadingUDPServer, ThreadingUnixDatagramServer, DatagramRequestHandler

from utils.socket_client import client_from_url

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


__all__ = ['ServerStorage']

SCHEME = ("udp", "udp6", "unix")

class ServerStorage(object):
    def __init__(self, config, parsed_url=None):
        self.config = config

        if parsed_url is None:
            self.url = urlparse(self.config.storage_endpoint)
        else:
            self.url = parsed_url

class ServerStorageClient(object):
    def __init__(self, config):
        self.config = config

        self.endpoint = self.config.endpoint
        self.client = client_from_url(self.endpoint)

    def send(self, measure):
        self.sock.send(str(measure))

class ServerStorageServer(object):

    def __init__(self, config):
        self.config = config

        self.endpoint = self.config.endpoint
        if "udp" in self.endpoint.scheme:
            self.server = TUDPServer(
                    self.endpoint.host, self.endpoint.port,
                    ServerStorageRequestHandler)
        else:
            self.server = TUnixServer(
                    self.endpoint.path, ServerStorageRequestHandler)

        self.server.allowed_hosts = self.config.allowed_hosts

        from storage.factory import storage_factory
        self.storage = storage_factory(self.config.storage_server.storage_endpoint)
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

