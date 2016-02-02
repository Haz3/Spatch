#! /usr/bin/env python

import os
import socket
import sys
import threading
import traceback

import paramiko
from paramiko.py3compat import b, u, decodebytes

# setup logging
paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
#host_key = paramiko.DSSKey(filename='test_dss.key')


class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'user') and (password == 'password'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED


    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True


if __name__ == '__main__':
    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 2200))
    except Exception as e:
        print('*** Bind failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    try:
        sock.listen(100)
        print 'Server start on port 2200'
        print('Listening for connection ...')
        client, addr = sock.accept()
    except Exception as e:
        print('*** Listen/accept failed: ' + str(e))
        traceback.print_exc()
        sys.exit(1)

    print('Got a connection!')

    try:
        t = paramiko.Transport(client)
        t.set_gss_host(socket.getfqdn(""))
        try:
            t.load_server_moduli()
        except:
            print('(Failed to load moduli -- gex will be unsupported.)')
            raise
        t.add_server_key(host_key)
        server = Server()
        try:
            t.start_server(server=server)
        except paramiko.SSHException:
            print('*** SSH negotiation failed.')
            sys.exit(1)

        # wait for auth
        try:
            chan = t.accept(20)
            print "Accept"
        except Exception as e:
            print #!/usr/bin/env python

        if chan is None:
            print('*** No channel.')
            sys.exit(1)
        print('Authenticated!')

        server.event.wait(10)
        if not server.event.is_set():
            print('*** Client never asked for a shell.')
            sys.exit(1)

        chan.send('\r\n\r\nWelcome to Spatch Proxy!\r\n\r\n')
        chan.send('Select your server: ')

        f = chan.makefile('rU')
        server_name = f.readline()
        chan.send('\r\nI don\'t like this, ' + server_name + '.\r\n')
        chan.close()

    except Exception as e:
        print('*** Caught exception: ' + str(e.__class__) + ': ' + str(e))
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)
