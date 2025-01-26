---
layout: newpost
title: "Writeup: HTB Challenge Signals"
date: 2025-01-26
categories: [tech]
tags: [htb, ctf, hardware]
---

- Challenge: [Signals](https://app.hackthebox.com/challenges/signals)
- Category: Hardware
- Solve date: 2025-01-26

---
### Description

> Some amateur radio hackers captured a strange signal from space. A first analysis indicates similarities with signals transmitted by the ISS. Can you decode the signal and get the information?

### Provided files

- `Signal.wav`

### ExifTool

```sh
ExifTool Version Number         : 12.76
File Name                       : Signal.wav
Directory                       : .
File Size                       : 12 MB
File Modification Date/Time     : 2021:06:14 14:04:59+02:00
File Access Date/Time           : 2025:01:26 18:05:39+01:00
File Inode Change Date/Time     : 2025:01:26 18:02:48+01:00
File Permissions                : -rw-r--r--
File Type                       : WAV
File Type Extension             : wav
MIME Type                       : audio/x-wav
Encoding                        : Microsoft PCM
Num Channels                    : 1
Sample Rate                     : 48000
Avg Bytes Per Sec               : 96000
Bits Per Sample                 : 16
Duration                        : 0:02:08
```

---
#  Slow-scan television (SSTV)

The ISS (see hint) transmits [SSTV](https://en.wikipedia.org/wiki/Slow-scan_television) signals, i.e. static images. We need some kind of software to decode it.

# QSSTV

We install [QSSTV](https://github.com/ON4QZ/QSSTV) and open the file (Options -> Configurations -> Sound -> "From file", then Start the receiver) and violà, the flag is here!


![flag](/assets/ctf_files/htb_signals/flag.png)
