---
layout: newpost
title: "Writeup: HTB Challenge Mini line"
date: 2025-01-29
categories:
  - tech
tags:
  - htb
  - ctf
  - hardware
---

- Challenge: [Mini line](https://app.hackthebox.com/challenges/miniline)
- Category: Hardware
- Solve date: 2025-01-29

---

### Description

> The Investigation after a recent breach revealed that one of our standard firmware flashing tools is backdoored. We also identified the last device that we flashed the firmware onto. We use LPC2148 microcontrollers in our devices. Can you analyze the firmware and see if any data was sent?

### Provided files

- `firmware.hex: ASCII text, with CRLF line terminators`

---

# What is a "LPC2148 microcontroller"?

This i a microcontroller used in IoT appliances with a CPU based on "ARM7TDMI-S", [Datasheet](https://www.nxp.com/docs/en/data-sheet/LPC2141_42_44_46_48.pdf) for more information.

---

# What is in the firmware.hex?

Well, we can be pretty sure it is hex.. 182 lines off this:
```
:100154002F6C69622F6C642D6C696E75782E736FC9
:030164002E330037
...
```

That is ["Intel hex](https://en.wikipedia.org/wiki/Intel_HEX) which [we can convert into an ELF](https://community.st.com/t5/automotive-mcus/how-to-convert-hex-file-to-elf-file/td-p/335527) for us to load into Ghidra.

## Converting

`sudo apt-get install gcc-arm-none-eabi -y`

```
> arm-none-eabi-objcopy -I ihex -O elf32-littlearm firmware.hex executable.elf
> file *
firmware.hex:   ASCII text, with CRLF line terminators
executable.elf: ELF 32-bit LSB relocatable, ARM, version 1 (ARM), stripped
```

---

# Ghidra to the resuce

Loading the file into Ghidra we can find a bit to relevant code where I renamed some variables and data to make it more readable (I not sure if they all actually makes sense..)

```c
  buffer1 = *(undefined4 *)(offset1 + 0x10720);
  uStack_20 = *(undefined4 *)(offset1 + 0x10724);
  uStack_1c = *(undefined4 *)(offset1 + 0x10728);
  uStack_18 = *(undefined4 *)(offset1 + 0x1072c);
  buffer2 = offset2;
  buffer3 = *(undefined4 *)(offset3 + 0x1073c);
  uStack_34 = *(undefined4 *)(offset3 + 0x10740);
  uStack_30 = *(undefined4 *)(offset3 + 0x10744);
  uStack_35 = (undefined)*(undefined4 *)(offset3 + 0x10748);
  output(spi_init + 0x10754);
  set_memory_values();
  output(set_start_bit + 0x10768);
  spi_transmit(1);
  output(transmit_data_to_slave + 0x10780);
  for (i = 0; i < 0x11; i = i + 1) {
    spi_transmit(*(byte *)((int)&buffer1 + i) ^ 0x1a);
  }
  for (i1 = 0; i1 < 5; i1 = i1 + 1) {
    spi_transmit(*(byte *)((int)&buffer2 + i1) >> 1 ^ 0x39);
  }
  for (i2 = 0; i2 < 0xe; i2 = i2 + 1) {
    spi_transmit(*(byte *)((int)&buffer3 + i2) >> 1 ^ 0x39);
  }
  output(data_transfer_complete + 0x1086c);
  spi_transmit(0);
  return 0;
```

There are three for loops which do some data mangling and then transmit data over SPI (Serial Peripheral interface). We should dig into those!

---

# Extracting the buffers

I am doing this semi-manually by:
1. Looking up the offset1
	1. 0x000002E0
2. Adding the value
	1. python3 -c "(print(hex(0x000002E0 + 0x10720)))"
3. Looking up that memory address (press "G")
	1. 0x10a00 -> 0x61584E52

I will continue this until I have all the values needed and then print each in full:

```python
combined_value = (buffer1_4_value << 96) | (buffer1_3_value << 64) | (buffer1_2_value << 32) | buffer1_1_value
print(combined_value)
```

## Printing the flag

- Loop 1: XORs each byte with `0x1a`, <`0x11` times.
- Loop 2: 1 bit right shift and XOR each byte with `0x39`, < 5 times.
- Loop 3: 1 biy right shift and XOR each byte with `0x39`, < `0xe` times.

```python
first= bytes.fromhex('..')
second = bytes.fromhex('..')
third = bytes.fromhex('..')
 
def main():
	first_result = ""
	second_result = ""
	third_result = ""

	# for (i = 0; i < 0x11; i = i + 1) {
	# spi_transmit(*(byte *)((int)&var1 + i) ^ 0x1a);
	# }
	for i in range(0x10):
		char = chr(first[i] ^ 0x1a)
		first_result += char
	
	# for (i1 = 0; i1 < 5; i1 = i1 + 1) {
	# spi_transmit(*(byte *)((int)&var3 + i1) >> 1 ^ 0x39);
	# }
	for i1 in range(4):
		char = chr(((second[i1] >> 1) ^ 0x39))
		second_result += char

	# for (i2 = 0; i2 < 0xe; i2 = i2 + 1) {
	# spi_transmit(*(byte *)((int)&var2 + i2) >> 1 ^ 0x39);
	# }
	for i2 in range(13):
		char = chr((third[i2] >> 1) ^ 0x39)
		third_result += char  
		print(first_result[::-1], end="")
		print(second_result[::-1], end="")
		print(third_result[::-1]

if __name__ == "__main__":
	main()
```

:checkered_flag:
