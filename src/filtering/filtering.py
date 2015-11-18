import sys
import libpcap
import argparse

def openPacket(packet, filter):


def __init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-filter', action='store', dest='filter',
                        help='filtering packet')
    parser.add_argument('-packet', action='store', dest='packet',
                        help='destination of packet')
    parser.add_argument('-live', action="store", dest='live',
                        help="live capture network")
    parser.add_argument('--version', action='version',
            version="%(prog)s 0.7")

    results = parser.parse_args()
    openPacket(results.packet, results.filter)


__init()
