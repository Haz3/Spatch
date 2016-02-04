#! /usr/bin/env python

import socket
import select
import time
import sys

buffer_size = 4096
delay = 0.0001
forward_to = ('10.26.112.27', 22)


class Forward():
    """class to init forward."""
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        """stat forwardind with params"""
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False


class Server():
    """class to init the server."""
    input_list = []
    channel = {}

    def __init__(self, host, port):
        """init socket."""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        """main_loop catch input from user."""
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    # let's get started
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    # close connection
                    self.on_close()
                    break
                else:
                    # receive data from client
                    self.on_recv()

    def on_accept(self):
        """accpet for forward."""
        # nedd to check here for authorization and do the job after
        forward = Forward().start(forward_to[0], forward_to[1])
        clientsock, clientaddr = self.server.accept()
        if forward:
            # print le client, catch l'input, renvoi sur le forward
            print clientaddr, "connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            # Error
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()

    def on_close(self):
        """close connection and clean."""
        print self.s.getpeername(), "disconnected"
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        self.channel[out].close()  # equivalent to do self.s.close()

        # close channel
        self.channel[self.s].close()
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        """Received data and send it."""
        data = self.data
        # just some hieroglyph for fun :)
        print data
        self.channel[self.s].send(data)

if __name__ == '__main__':
        server = Server('', 9090)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)
