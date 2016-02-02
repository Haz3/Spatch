#! /usr/bin/env python

import paramiko
import interactive
import getpass

# enable GSS-API / SSPI authentication
UseGSSAPI = True
DoGSSAPIKeyExchange = True

port = 22

def list_server():
    server_dic = {
        "server55": "192.168.1.18",
        "server23": "192.168.1.40",
        "server56": "192.168.1.39"
    }

    print "Welcome to Spatch ! \nSelect a server to connect\n"

    for name_server in server_dic:
        print "-- \t", name_server

    try:
        user_hostname = raw_input()
        if  user_hostname in [hostname for hostname in server_dic]:
            return server_dic[user_hostname]
        else:
            print "ERROR MOTHERFUCKER"
    except KeyboardInterrupt:
        print "\nBye !"


def connect_server(user, password):
    ip_server = list_server()

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        print('*** Connecting...')

        try:
            client.connect(ip_server, port, "user1", "password")
        except Exception:
            print "Error connection"

        chan = client.invoke_shell()

        print(repr(client.get_transport()))
        print('*** Here we go!\n')

        interactive.posix_shell(chan)
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

if __name__ == '__main__':

    user = raw_input('Login: ')
    password = getpass.getpass()
    print user
    print password

    connect_server(user, password)


"""
    HOST= sys.argv[1]
    COMMAND="uname -a"

    ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                           shell=False,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >>sys.stderr, "ERROR: %s" % error
    else:
        print result
"""
