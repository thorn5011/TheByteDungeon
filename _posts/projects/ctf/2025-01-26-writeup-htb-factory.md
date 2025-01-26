---
layout: newpost
title: "Writeup: HTB Challenge Factory"
date: 2025-01-26
categories: [tech]
tags: [htb, ctf, hardware]
---

- Challenge: [Factory](https://app.hackthebox.com/challenges/factory)
- Category: Hardware
- Solve date: 2025-01-26

---
### Description

> Our infrastructure is under attack! The HMI interface went offline and we lost control of some critical PLCs in our ICS system. Moments after the attack started we managed to identify the target but did not have time to respond. The water storage facility's high/low sensors are corrupted thus setting the PLC into a halt state. We need to regain control and empty the water tank before it overflows. Our field operative has set a remote connection directly with the serial network of the system.

### Provided files

- `PLC_Ladder_Logic.pdf`
- `interface_setup.png`

---
# modbus RTU frame

This is the way a [modbus](https://en.wikipedia.org/wiki/Modbus) frame looks like:

| Slave address | Function Code | Data          | CRC                                         |
| ------------- | ------------- | ------------- | ------------------------------------------- |
| 1 byte        | 1 byte        | 0 – 252 bytes | 2 bytes: 1 CRC low byte and 1 CRC high byte |

## Coil addresses (from png)

| Addr | Hex    | Coil                |
| ---- | ------ | ------------------- |
| 12   | 0xc    | in_valve            |
| 21   | 0x15   | out_valve           |
| 33   | 0x21   | start               |
| 9947 | 0x26db | manual_mode_control |
| 5    | 0x05   | cutoff              |
| 26   | 0x1a   | cutoff_in           |
| 52   | 0x34   | force_start_out     |
| 1336 | 0x538  | force_start_in      |

## Connecting to remote host

```sh
❯ nc 83.136.250.116 54224
Water Storage Facility Interface
1. Get status of system
2. Send modbus command
3. Exit
Select: 1
{"auto_mode": 1, "manual_mode": 0, "stop_out": 0, "stop_in": 0, "low_sensor": 0, "high_sesnor": 0, "in_valve": 1, "out_valve": 0, "flag": "HTB{}"}
```

Current settings:
```json
{"auto_mode": 1, "manual_mode": 0, "stop_out": 0, "stop_in": 0, "low_sensor": 0, "high_sesnor": 0, "in_valve": 1, "out_valve": 0, "flag": "HTB{}"}
```

---

# What do we know?

We know that:
- the slave address is 0x52 (82 in decimal)
- "laptop-2" take care of the CRC.
- we need to configure "coils" with a modbus command
- we want the water to flow out since the sensors are messed up, so we *probably* want to set:
	- manual_mode_control -> manual_mode = 1
	- cutoff_in -> stop_in = 1
	- out_valve -> out_valve = 1
	- force_start_out = 1

## Compile modbus command

### Function
- Write Single Coil = 5 -> `0x5`

### Data
Address + on/off:
- `FF 00` = ON (1)
- `00 00` = OFF (0)

### Command

| Set these to ON     | Slave address | Function Code | Data        |
| ------------------- | ------------- | ------------- | ----------- |
| manual_mode_control | 52            | 05            | 26db + FF00 |
| force_start_out     | 52            | 05            | 0034 + FF00 |
| out_valve           | 52            | 05            | 0015 + FF00 |
| cutoff_in           | 52            | 05            | 001a + FF00 |

We will then send these commands:  `52050015FF00`, `520526dbFF00`, `52050034FF00`, `5205001aFF00`

This leave us the these settings (and the flag!):
```json
{"auto_mode": 0, "manual_mode": 1, "stop_out": 0, "stop_in": 1, "low_sensor": 0, "high_sesnor": 0, "in_valve": 0, "out_valve": 1, "flag": "HTB{14dd32_..._5y573m5}"}
```
