Title: Setting up a ChromiumOS dev environment
Date: 2017-02-16 10:31
Category: chromiumos
Tags: linux, chromiumos, chromebook, collabora
Description: How to get up and running, developing ChromiumOS on actual Chromebook hardware.


## Set up environment
    export DEV_DIR="/opt"
    mkdir -p $DEV_DIR
    export CHROMIUM_DIR="$DEV_DIR/chromiumos"
    mkdir -p $CHROMIUM_DIR
    export PATH="$DEV_DIR/depot_tools:$PATH"
    
    # The BOARD variable used here is specific for the Chromebook that is
    # being targeted, a more generic target like "amd64-generic" could
    # be more useful for you needs.
    export BOARD=chell
    
    # The USB_DEVICE variable refers to the USB device that will be used
    # for flashing ChromiumOS onto a Chromebook.
    # Make sure that this device does not contain anything important!
    export USB_DEVICE="/dev/sda"


## Install dependencies
    sudo apt install git-core gitk git-gui subversion curl
    cd $DEV_DIR
    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git


## Get ChromiumOS source
    cd ${CHROMIUM_DIR}
    repo init -u https://chromium.googlesource.com/chromiumos/manifest.git
    repo sync -j25


## Build ChromiumOS
    cros_sdk -- ./build_packages --board=${BOARD}
    cros_sdk -- ./build_image --board=${BOARD}


## Flash ChromiumOS to storage medium
    cros_sdk -- cros flash --board=${BOARD} usb:/$USB_DEVICE


## Install ChromiumOS on Chromebook
### Enter Chromebook into dev-mode
This part is highly device specific, and depends on how the manufacturer of your device has chosen
to implement the dev-mode switch.

A partial list of devices and how to enter them into dev-mode can be found [here](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices).

### Flash ChromiumOS to Chromebook
Fire up your Chrombook device and hit Ctrl+Alt+Back, followed by 'chronos' and hit enter.
Followed by the below command to install the ChromiumOS build that was just flashed.

    /usr/sbin/chromeos-install

## Debug an application
### On Chromebook
Again fire up your Chrombook device and hit Ctrl+Alt+Back, followed by 'chronos' and hit enter.

    # Remount the root drive read / write
    sudo mount -o remount,rw /

    # Open port so that gdbserver can be reached
    sudo /sbin/iptables -A INPUT  -p tcp --dport 1234 -j ACCEPT

    # Run gdb server, listening on port 1234 (opened in iptables command above)
    sudo gdbserver :1234 chrome

### On dev machine

    # On x86
    cros_sdk -- sudo USE=expat emerge cross-i686-pc-linux-gnu/gdb
    # On ARMv7
    cros_sdk -- sudo USE=expat emerge cross-armv7a-cros-linux-gnueabi/gdb
    
    cros_sdk -- i686-pc-linux-gnu-gdb "/build/$BOARD/opt/google/chrome/chrome"
    (gdb) set sysroot /build/$BOARD/
    (gdb) target remote IP_ADDR_CHROMEBOOK:1234
    (gdb) continue


## Conclusion
This is a bit of a rough outline, and is only suitable for Chromebook devices that already are in dev-mode.


## Thanks
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).


## References
[ChromiumOS Depo Tools](http://dev.chromium.org/developers/how-tos/install-depot-tools)<br>
[ChromiumOS Quick Start](https://www.chromium.org/chromium-os/quick-start-guide)<br>
[ChromiumOS Dev Mode](https://www.chromium.org/chromium-os/developer-information-for-chrome-os-devices)<br>
[ChromiumOS Debug](https://www.chromium.org/chromium-os/how-tos-and-troubleshooting/debugging-tips)
