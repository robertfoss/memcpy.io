Title: Fixing bluetooth on the XPS 15 9550 on Ubuntu
Date: 2017-10-28
Category: hack
Tags: desktop, debian, ubuntu, broadcom, brcm, bluetooth, connecting, pairing, driver
Description: The bluetooth module of the Dell XPS 15 9550 has never been working for me, but copying a firmware blob onto my machine fixed my issues.

## Why doesn't this work automatically?
The firmware blob that is needed by Broadcom devices is not supplied by default, and it has to be supplied manually.

## How To
Download [BCM-0a5c-6410.hcd](/files/2017-10-28/BCM-0a5c-6410.hcd) and copy it into `/lib/firmware/brcm/` and then reboot your device.

    wget https://memcpy.io/files/2017-10-28/BCM-0a5c-6410.hcd
    sudo cp BCM-0a5c-6410.hcd /lib/firmware/brcm/
    sudo chmod 0644 /lib/firmware/brcm/BCM-0a5c-6410.hcd
    sudo reboot
