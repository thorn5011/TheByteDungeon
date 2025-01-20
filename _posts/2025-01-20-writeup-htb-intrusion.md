---
layout: newpost
title: "Writeup: HTB Challenge Intrusion"
date: 2025-01-20
categories: [tech]
tags: [htb, ctf, hardware]
---

# Challenge: Intrusion

- Challenge name: Intrusion
- CATEGORY: Hardware
- Solve date: 2025-01-19

### CHALLENGE DESCRIPTION: 

> After gaining access to the enemy's infrastructure, we collected crucial network traffic data from their Modbus network. Our primary objective is to swiftly identify the specific registers containing highly sensitive information and extract that data.

### Provided files

- `client.py`: Python starting file to communicate with remote modbus service
- `network_logs.pcapng`: PCAP with modbus traffic with 168 modbus packets

---

# What is "modbus"?

Modbus is a protocol used in SCADA environments to communicate with industrial control systems.

## Packet structure

The captured packages are using a version of the protocol to communicate over TCP called "modbus TCP" where the payloads are strutured like this `ba d1 00 00 00 04 34 01 01 03`

1. First 2 bytes: `ba d1` is the transaction number
2. `00 00`: The protocol identifier
3. `00 04`: The length
4. `34`: Unit identifier
5. `01`: The function, in this case "Read Coils"
6. The modbus function data is function specific, i.e. `01 03`

---

# Finding a relevant function in the capture

They ask us to "identify the specific registers" so we need to find something which interacts with a register. We can see 3 functions in the capture:
- `0x01` Read Coils
- `0x0f` Write multiple coils
- `0x10` Write multiple registries

Let's look at "Write multiple registries".

## Write multiple registries

[modbus.org](https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf) (page 30) tells this about the request payload structure. Let's include one package seen in our capture (post function bytes): `10 00 06 00 01`.

|What|Bytes|Example|Our payload|
|-|-|-|-|
Function code |1 Byte |0x10|0x10
Starting Address |2 Bytes |0x0000 to 0xFFFF|0x0006
Quantity of Registers |2 Bytes |0x0001 to 0x007B|0x0001
Byte Count| 1 Byte| 2 x N*|n/a
Registers Value |N* x 2 Bytes |value|n/a

So it looks like we don't see any value being written.. but we do know that the register is at `0x0006`!

# Read the registers

In the python code provided they use `from umodbus.client import tcp`.
The write function will add data to "holding" registries so we should use [`read_holding_registers`](https://umodbus.readthedocs.io/en/latest/_modules/umodbus/client/tcp.html#read_holding_registers).

---

# Putting it all together

- We will use `scapy` to parse data from the capture
- We will find all the "Write multiple registries" functions and collect the addresses
- We will read the holding registries addresses

Code -> [client.py](({{site.baseurl}}/assets/ctf_files/htb_intursion/client.py)

```py
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
```

Output:
```sh
❯ python client.py
Found 42 Modbus registers

HTB{23...}
```