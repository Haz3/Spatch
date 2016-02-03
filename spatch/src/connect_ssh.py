import base64
import getpass
import os
import socket
import sys
import traceback

import paramiko

# setup logging
paramiko.util.log_to_file('demo_simple.log')
# Paramiko client configuration
port = 22


def connect(username, password, hostname):
    """username, password.base64(), hostname."""
    username = ''
    # get username
    if username == '':
        default_username = getpass.getuser()
        if len(username) == 0:
            username = default_username

    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')
        client.connect(hostname, port, username, password)

        chan = client.invoke_shell()
        print(repr(client.get_transport()))
        print('*** Here we go!\n')
        interactive.interactive_shell(chan)
        chan.close()
        client.close()

    except Exception as e:
        print('*** Caught exception: %s: %s' % (e.__class__, e))
        traceback.print_exc()
        try:
            client.close()
        except:
            pass
        sys.exit(1)
