#!/usr/bin/python3

import socket
from time import sleep
from umodbus import conf
from umodbus.client import tcp
from scapy.all import rdpcap, TCP

# Adjust modbus configuration
conf.SIGNED_VALUES = True

# Create a socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "94.237.50.7"
sock.connect((ip, 36363))

modbus_functions = {
    "01": "Read Coils",
    "02": "Read Discrete Inputs",
    "03": "Read Holding Registers",
    "04": "Read Input Registers",
    "05": "Write Single Coil",
    "06": "Write Single Register",
    "15": "Write Multiple Coils",
    "10": "Write Multiple Registers",
}

def read_pcap():
    sus_bytes = []
    packets = rdpcap('network_logs.pcapng')
    for packet in packets:
        if TCP in packet:
            payload = bytes(packet[TCP].payload)
            # ex: b'\xba\xd1\x00\x00\x00\x044\x01\x01\x03'
            if payload:
                try:
                    transaction = payload[:2]
                    protocol = payload[2:4]
                    lenght = payload[4:6]
                    unit = payload[6]
                    func = payload[7]
                    other = payload[8:]
                    transaction = int.from_bytes(transaction, byteorder='big')
                    # print(f"transaction: {transaction}, protocol: {protocol}, lenght: {lenght}, unit: {unit:02x}, func: {func:02x}")
                    function_name = modbus_functions.get(f"{func:02x}", "Unknown")
                    if function_name == "Write Multiple Registers":
                        sus_bytes.append({
                            "addr": other[:2],
                            "quantity": other[2:4],
                            })
                except Exception as e:
                    print(f"------------\nFailed to parse Modbus data: {e}")
                    print(payload)
            # break
    return sus_bytes

registers = read_pcap()

print(f"Found {len(registers)} Modbus registers\n   ")

"""
 umodbus.client.tcp.read_holding_registers(slave_id, starting_address, quantity)

    Return ADU for Modbus function code 03: Read Holding Registers.
    Parameters:	slave_id – Number of slave.
    Returns:	Byte array with ADU.
"""
for reg in registers:
    add = int.from_bytes(reg["addr"])
    quantity = int.from_bytes(reg["quantity"])
    message = tcp.read_holding_registers(slave_id=52, starting_address=int(add), quantity=int(quantity))
    response = tcp.send_message(message, sock)
    print(chr(response[0]), end="", flush=True)
    sleep(0.5)

sock.close()
