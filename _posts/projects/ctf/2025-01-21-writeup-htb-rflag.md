---
layout: newpost
title: "Writeup: HTB Challenge RFlag"
date: 2025-01-21
categories: [tech]
tags: [htb, ctf, hardware]
---

- Challenge: [RFlag](https://app.hackthebox.com/challenges/RFlag)
- Category: Hardware
- Solve date: 21 Jan 2025

### CHALLENGE DESCRIPTION: 

> We have found the garage where some cyber criminals have all their stuff. Using an SDR device, we captured the signal from the remote key that opens the garage. Can you help us to analyze it?

### Provided files

- [`signal.cf32`](({{site.baseurl}}/assets/ctf_files/htb_rflag/signal.cf32)) : 3,7M radio capture

---

# Decode the signal data

The challenge mentions SDR (software defined radio), so we can use the [Universal radio hacker](https://github.com/jopohl/urh) to try to understand the data.

After some research we understand that remote garage keys use ["on-off keying"](https://en.wikipedia.org/wiki/On%E2%80%93off_keying) which is a type of ASK ("amplitude-shifting keying") so let's use that.

![urh1](/assets/ctf_files/htb_rflag/urh1.png)


Using "autodetect" changes the "Samples/Symbols" to 900 which is the size of each bit as can be visualized here (~7200/900):

![urh2](/assets/ctf_files/htb_rflag/urh2.png)

Once we have interpreted the data, we move on to the Analysis tab. I played around with settings but turns out that ["Manchester code"](https://en.wikipedia.org/wiki/Manchester_code) is a common encoding schema to use.  Wikipedia also mentions that is was (and is) used for uploading commands to the Voyager spacecraft!

Anyway, we view the data as ASCII and set the decoding to "Manchester 2" and the flag pops up!

![urh3](/assets/ctf_files/htb_rflag/urh3.png)