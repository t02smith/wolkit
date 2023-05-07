from re import search
import time
import struct
import socket
import logging as log

def magic_packet(mac_addr: str):
    """
    Generates a magic packet for a given MAC address
    This packet can be sent to the target machine to wake it up
    """
    if search("^([0-9a-zA-Z]{2}[:-]){5}[0-9a-zA-Z]{2}$", mac_addr) is None:
        # ! invalid mac address format
        raise ValueError(f"Invalid mac addr {mac_addr}")

    mac_addr = mac_addr.replace(":", "")
    data = ''.join(['FFFFFFFFFFFF', mac_addr * 20])
    send_data = b''

    # Split up the hex values and pack.
    for j in range(0, len(data), 2):
        send_data = b''.join([
            send_data,
            struct.pack('B', int(data[j: j + 2], 16))
        ])

    log.debug(f"Created magic packet {send_data}")
    return send_data


def send_magic_packet(mac_addr: str, broadcast_addr: str):
    """
    Sends a magic packet to a target mac address.
    Assumes that the mac_addr is well-formed.
    """
    packet = magic_packet(mac_addr)
    log.debug(f"Broadcasting magic packet to wake {mac_addr}")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(packet, (broadcast_addr, 7))
    log.debug(f"Broadcast magic packet for {mac_addr}")
