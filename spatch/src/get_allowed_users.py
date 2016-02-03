import paramiko
import json
from scp import SCPClient

user = "root"
password = "menace"


"""
server23 = ["192.168.1.18", 22, tuple()]
server55 = ["192.168.1.40", 22, tuple()]
server56 = ["192.168.1.39", 22, tuple()]
listServer = (server23, server55, server56)
"""


def open_config_file(server_name):
    list_server_ip = []
    # Bonus, chiffrement du fichier json

    with open("config.json") as config_file:
        dict_config = json.load(config_file)
        return dict_config[str(server_name).upper()]


def getTupleUser(userListStr):
    users = []
    for user in userListStr.split(" "):
            users.append(user.rstrip('\n'))
    return tuple(users)


def OpenFileaddToPermission(serverPermission):
    # delete this line when not debug
    serverPermission = tuple()
    with open("/etc/ssh/sshd_config", "r+") as files:
            for line in files:
                    if "AllowUsers" in line:
                            serverPermission = serverPermission + getTupleUser(
                                            line[12:len(line)])
    return serverPermission


def createSSHClient(server, port, user, password):
    print "contacting %s: %d" % (server, int(port))
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, port, user, password)
        return client
    except Exception as e:
        print str(e)
        print "Unable to connect"


def getAllserver(list_server_ip):
    for server in list_server_ip:
        print server
        try:
            ssh = createSSHClient(server, 22, user, password)
            SCPClient(ssh.get_transport()).get('/etc/ssh/ssh_config')
            server[2] = OpenFileaddToPermission(server[2])
            print server[0] + " added new permission for : " + str(server[2])
            ssh.close()
        except Exception as e:
            print e

# getAllserver()
