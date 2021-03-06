import socket

try:
    from urllib.parse import urlparse, ParseResult
except ImportError:
    from urlparse import urlparse, ParseResult


__all__ =   ['BaseClient',
            'TCPClient',
            'UDPClient',
            'UnixStreamClient',
            'UnixDatagramClient']


class ResponseHandler(object):
    def __init__(self, response, client):
        pass

    def __call__(self):
        pass

"""Provides easy instantiation and handling of a client to a server.
Needs the client addr in the form:


((tcp)|(udp))(6)?://<host>:<port>

or

unix://<socket path>


<host> = IP or hostname of the server
<port> = Portnumber the server is listening on

<socket path> = Absolute path to the socket file for unix datagram
"""
class BaseClient(object):
    timeout = None
    socket_family = None

    def __init__(self, client_addr, response_handler = None):
        self.client_addr = client_addr

        if response_handler is not None:
            self.response_handler_class = response_handler
        else:
            self.response_handler_class = response_handler

        self.connect()

    def handle(self, data):
        self.send(data)

        timeout = self.socket.gettimeout()
        if timeout is None:
            timeout = self.timeout

        elif self.timeout is not None:
            timeout = min(timeout, self.timeout)

        fd_sets = _eintr_retry(select.select, [self], [], [], timeout)
        if not fd_sets[0]:
            self.handle_timeout()

        try:
            response = self.get_response()
        except socket.error:
            return

        if self.verify_response(response):
            return self.process_response(response)

        return response

    def handle_timeout(self):
        pass

    def get_response(self):
        """Nothing to get here, should be overwriten in subclasses.
        """
        raise NotImplementedError("Use subclass that implement this.")

    def verify_response(self, response):
        """Return always true, what else should be verified?!
        Maybe overwriten.
        """
        return True

    def process_response(self, response):
        return self.response_handler_class(response, self)()

    def send(self, data):
        if self.connection is not None:
            self.connect()

        try:
            encoded_data = b'' + str(data)
        except UnicodeError:
            data = unicode(data)
            if hasattr(data, 'encode'):
                if callable(data.encode):
                    encoded_data = b'' + data.encode('unicode_escape')

                else:
                    raise IOError(  ("Data has an attribute `encode`"
                                    " but could not convert from `string`"
                                    " to byte compatible object"))

        self.connection.send(encoded_data)

class TCPClient(BaseClient):
    MAX_BUFFER_SIZE = 8192

    socket_type = socket.SOCK_STREAM

    def __init__(self, client_addr):
        if not isinstance(client_addr, (ParseResult)):
            self.url = urlparse(client_addr)
        else:
            self.url = client_addr

        if "6" in self.url.scheme:
            self.family = socket.AF_INET6
        else:
            self.family = socket.AF_INET

        self.socket = socket.socket(self.family, self.type)
        super(TCPClient, self).__init__(client_addr)

    def connect(self):
        self.socket.connect(self.url.host, self.url.port)
        self.connection = self.socket

    def get_response(self):
        addr, data = self.socket.recv(self.MAX_BUFFER_SIZE)
        return data

class UDPClient(TCPClient):
    socket_type = socket.SOCK_DGRAM

if hasattr(socket, 'AF_UNIX'):
    class UnixClientMixIn:
        def connect(self):
            self.socket.connect(self.url.path)
            self.connection = self.socket

    class UnixStreamClient(UnixClientMixIn, TCPClient):
        def __init__(self, client_addr):
            super(UnixStreamClient, self).__init__(client_addr)

            self.family = socket.AF_UNIX

    class UnixDatagramClient(UnixClientMixIn, UDPClient):
        def __init__(self, client_addr):
            super(UnixStreamClient, self).__init__(client_addr)

            self.family = socket.AF_UNIX


def client_from_url(url):
    parsed_url = urlparse(url)

    if "tcp" in parsed_url.scheme:
        return TCPClient(url)
    elif "udp" in parsed_url.scheme:
        return UDPClient(url)
    else:
        return UnixStreamClient(url)

