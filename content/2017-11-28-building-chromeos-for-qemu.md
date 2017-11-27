Title: Building ChromiumOS for Qemu
Date: 2017-11-28 11:32
Category: kernel
Tags: linux, kernel, chromeos, chromiumos, chromium, qemu, ssh, collabora
Description: Getting ChromiumOS building is reasonably easy, but running it under Qemu requires some work. 

![Alt text](/images/2017-11-28_chromeos_qemu.png "ChromiumOS running on Qemu")

So let's start off by covering how ChromiumOS relates to ChromeOS. The
ChromiumOS project is essentially ChromeOS minus branding and some
packages for things like the media digital restrictions management.

But on the whole, almost everything is there, and the pieces that aren't,
you don't _need_.

## ChromiumOS
### Depot tools
ChromiumOS is entirely open source, however in order to build it you'll need the
Google depot tools.

    git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    export PATH=$PATH:$(PWD)/depot_tools

Maybe you'd want to add the PATH export to your .bashrc.

### Building ChromiumOS
    mkdir chromiumos
    cd chromiumos
    repo init -u https://chromium.googlesource.com/chromiumos/manifest.git --repo-url https://chromium.googlesource.com/external/repo.git [-g minilayout]
    repo sync -j75
    cros_sdk
    export BOARD=amd64-generic
    ./setup_board --board=${BOARD}
    ./build_packages --board=${BOARD}
    ./build_image --board=${BOARD} --boot_args "earlyprintk=serial,keep console=tty0" --noenable_rootfs_verification test
    ./image_to_vm.sh --board=${BOARD} --test_image

### How to (not) boot ChromiumOS
So, this is a command baked into ChromiumOS using the `cros_start_vm` command,
but at least on my machine it does not seem to boot properly.
I have as of yet not been able to get any graphical output (over VNC).

    cros_sdk
    ./bin/cros_start_vm --image_path=../build/images/${BOARD}/latest/chromiumos_qemu_image.bin --board=${BOARD}


## Running Qemu ourselves
So if the intended tools to work, we'll just have to roll up our sleeves
and do it ourselves. This is how I got ChromiumOS booting.

### Install build dependencies
These dependencies were available on Ubuntu 17.10, some alternative packages
might be needed for _your_ distributions.

    sudo apt install autoconf libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev libcap-dev libcap-ng-dev libcurl4-gnutls-dev libepoxy-dev libfdt-dev libgbm-dev libgles2-mesa-dev libglib2.0-dev libgtk-3-dev libibverbs-dev libjpeg8-dev liblzo2-dev libncurses5-dev libnuma-dev librbd-dev librdmacm-dev libsasl2-dev libsdl1.2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh2-1-dev libspice-server-dev libspice-server1 libtool libusb-1.0-0 libusb-1.0-0-dev libvde-dev libvdeplug-dev libvte-dev libxen-dev valgrind xfslibs-dev xutils-dev zlib1g-dev libusbredirhost-dev usbredirserver


### Virglrenderer
Virglrenderer creates a virtual 3D GPU, that allows the Qemu guest to use the
graphics capabilities of the host machine.

This step is optional, but allows for hardware accelerated OpenGL support on
the guest system.
If you don't want to use Virgl, remove it from the Qemu configure step and
the Qemu runtime flags.

    git clone git://git.freedesktop.org/git/virglrenderer
    cd virglrenderer
    ./autogen.sh
    make -j7
    sudo make install


### Qemu
Qemu is a full system emulator, and supports a multitude of machine architectures.
We're going to to use _x86_64_.

    git clone git://git.qemu-project.org/qemu.git
    mkdir -p qemu/build
    cd qemu/build
    ../configure --target-list=x86_64-softmmu --enable-gtk --with-gtkabi=3.0 --enable-kvm --enable-spice --enable-usb-redir --enable-libusb --enable-virglrenderer --enable-opengl
    make -j7
    sudo make install


### Run image
Now you can boot the image using Qemu.

Note that running Qemu with the virtio options requires that your host machine
is running a Linux kernel which was built with the kconfig options `CONFIG_DRM_VIRTIO`,
`CONFIG_VIRT_DRIVERS` and `CONFIG_VIRTIO_XXXX`.


    cd chromiumos
    /usr/local/bin/qemu-system-x86_64 \
        -enable-kvm \
        -m 2G \
        -smp 4 \
        -hda src/build/images/amd64-generic/latest/chromiumos_qemu_image.bin \
        -vga virtio \
        -net nic,model=virtio \
        -net user,hostfwd=tcp:127.0.0.1:9222-:22 \
        -usb -usbdevice keyboard \
        -usbdevice mouse \
        -device virtio-gpu-pci,virgl \
        -display gtk,gl=on


## Conclusion
Hopefully this guide will have helped you to build all of the software needed to
run boot your very own ChromiumOS.

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
