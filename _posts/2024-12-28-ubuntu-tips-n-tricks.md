---
layout: newpost
title: "Ubuntu tips and tricks"
date: 2024-12-28
categories: [tech]
tags: [ubuntu, linux, vim, zsh, qemu]
---

There are always some command, shortkey or sequence of events I need to remeber once a blue moon and I almost never remeber them. So instead of googling or dumpster diving in the command history, I'll just try to gather them here. That means this should be a somewhat of a living document..

---
# System

- `sudo systemctl -f -k` looks to incoming kernal messages
- `sudo journalctl -k --grep=brcmfmac` with grep

# Vim

[Cheat sheet](https://vim.rtorr.com/)

## Command mode (default)
```sh
y - copy line
p - paste line
dd - cut  line
d10 - delete 10 lines
u - undo
```

# zsh and powerlevel

[Guide](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#manual)


- `p10k configure` for wizard
- `vi ~/.p10k.zsh` for manual edit

# virtual machines

- [Guide](https://ubuntuhandbook.org/index.php/2024/12/kvm-qemu-virtual-machines-ubuntu/)
- [Guide 2](https://www.blackhillsinfosec.com/qemu-msys2-and-emacs/) for Kali and qemu

`qcow2` is a "qemu" format which expand the size as needed. The VM can be shutdown with persistent storage.

```sh
sudo apt install qemu-kvm

qemu-system-x86_64 \
-enable-kvm                                                    \
-cpu host \
-m 4G                                                          \
-smp 2                                                         \
-hda /opt/virtualmachines/kali-linux-2024.4-qemu-amd64.qcow2   \
-netdev user,id=net0,net=192.168.100.0/24,dhcpstart=192.168.100.9,hostfwd=tcp::1337-:22  \
-device virtio-net-pci,netdev=net0                             \
-vga qxl                                                       \
-device AC97 # For sound if needed
```