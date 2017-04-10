Title: Building Android for Qemu with Mesa and Virgil3D
Date: 2016-08-30 15:22
Category: kernel
Tags: linux, kernel, android, qemu, collabora
Description: Running the Linux mainline graphics stack on Android devices is currently not a reality, but this is a viable development environment for improving the situation.

![Alt text](/images/2016-08-30_android_qemu.png "Android running on Qemu")

Developing Linux for Android on Qemu allows you to do some things that are
not necessarily possible using the stock emulator.
For my purposes I need access to a GPU and be able to modify the driver, which
is where Virgilrenderer and Qemu comes in handy.

The guide below helps you compile Android and run it on top of Qemu with
Mesa/Virgilrenderer supplying a virtual GPU.
Because of this, the following guide is aimed at Linux hosts.

This guide is based on Rob Herrings [fantastic guide](https://github.com/robherring/generic_device/wiki/KConfig-based-Multi-platform-Android-Device-(and-Mesa-graphics)), but has
been slightly streamlined and had physical hardware support stripped out.


## Install dependencies
These dependencies were available on Ubuntu 16.04, some alternative packages
might be needed for other distributions.

    sudo apt install autoconf gcc-aarch64-linux-gnu libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev libcap-dev libcap-ng-dev libcurl4-gnutls-dev libepoxy-dev libfdt-dev libgbm-dev libgles2-mesa-dev libglib2.0-dev libibverbs-dev libjpeg8-dev liblzo2-dev libncurses5-dev libnuma-dev librbd-dev librdmacm-dev libsasl2-dev libsdl1.2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh2-1-dev libtool libusb-1.0-0 libusb-1.0-0-dev libvde-dev libvdeplug-dev libvte-2.90-dev libxen-dev valgrind xfslibs-dev xutils-dev zlib1g-dev libusbredirhost-dev usbredirserver


## Set up paths
Naturally all of the paths below are configurable, this is just what I used.

    export PROJECT_PATH="/opt/qemu_android"
    export VIRGLRENDERER_PATH="${PROJECT_PATH}/virglrenderer"
    export QEMU_PATH="${PROJECT_PATH}/qemu"
    export LINUX_PATH="${PROJECT_PATH}/linux"
    export ANDROID_PATH="${PROJECT_PATH}/android"
    export ANDROID_TOOLS_PATH="${PROJECT_PATH}/android-tools"


## Virglrenderer
Virglrenderer creates a virtual 3D GPU, that allows the Qemu guest to use the
graphics capabilities of the host machine.

    git clone git://git.freedesktop.org/git/virglrenderer ${VIRGLRENDERER_PATH}
    cd ${VIRGLRENDERER_PATH}
    ./autogen.sh
    make -j7
    sudo make install


## Qemu
Qemu is a full system emulator, and supports a multitude of machine architectures.
We're going to to use x86_64 but also build support for arm64/aarch64.

    git clone git://git.qemu-project.org/qemu.git ${QEMU_PATH}
    mkdir ${QEMU_PATH}/build
    cd ${QEMU_PATH}/build
    ../configure --target-list=aarch64-softmmu,x86_64-softmmu --enable-gtk --with-gtkabi=3.0 --enable-kvm --enable-spice --enable-usb-redir --enable-libusb
    make -j7


## Linux kernel
Build trunk of mainline linux kernel.

**Important:** The below instructions use upstream/master but during testing of
this guide, *https://git.kernel.org/pub/scm/linux/kernel/git/padovan/linux.git*
and the *fences* branch was used due to SW_SYNC not yet being included in upstream.
Inclusion is targeted for *v4.9*.

    git clone git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git ${LINUX_PATH}
    cd ${LINUX_PATH}
    wget http://memcpy.io/files/2016-08-30/Kconfig -O ${LINUX_PATH}/.config
    make oldconfig
    make -j7


**Important:** If you decide not to use the *.config* linked in this step, a few
Kconfig options need to be set:

    CONFIG_ANDROID=y
    CONFIG_ANDROID_BINDER_IPC=y
    CONFIG_AUDIT=y
    CONFIG_HAVE_ARCH_AUDITSYSCALL=y
    CONFIG_AUDITSYSCALL=y
    CONFIG_AUDIT_WATCH=y
    CONFIG_AUDIT_TREE=y
    CONFIG_SECURITY_SELINUX=y
    CONFIG_SECURITY_SELINUX_BOOTPARAM=y
    CONFIG_SECURITY_SELINUX_BOOTPARAM_VALUE=1
    CONFIG_SECURITY_SELINUX_DISABLE=y
    CONFIG_SECURITY_SELINUX_DEVELOP=y
    CONFIG_SECURITY_SELINUX_AVC_STATS=y
    CONFIG_SECURITY_SELINUX_CHECKREQPROT_VALUE=0
    CONFIG_DEFAULT_SECURITY_SELINUX=y
    CONFIG_DEFAULT_SECURITY="selinux"
    CONFIG_VIRTIO_BLK=y
    CONFIG_SCSI_VIRTIO=y
    CONFIG_VIRTIO_NET=y
    CONFIG_VIRTIO_CONSOLE=y
    CONFIG_HW_RANDOM_VIRTIO=y
    CONFIG_DRM_VIRTIO_GPU=y
    CONFIG_VIRT_DRIVERS=y
    CONFIG_VIRTIO=y
    CONFIG_VIRTIO_PCI=y
    CONFIG_VIRTIO_PCI_LEGACY=y
    CONFIG_VIRTIO_BALLOON=y
    CONFIG_VIRTIO_INPUT=y
    CONFIG_VIRTIO_MMIO=y
    CONFIG_VIRTIO_MMIO_CMDLINE_DEVICES=y
    CONFIG_NET_9P=y
    CONFIG_NET_9P_VIRTIO=y
    CONFIG_SYNC=y
    CONFIG_SW_SYNC=y
    CONFIG_SYNC_FILE=y


## Android
Build the Android Open Source Project.

**Important:** When running *source build/envsetup.sh* make sure that you are
using bash. I had issues running *lunch* using zsh.

    mkdir ${ANDROID_PATH}
    cd ${ANDROID_PATH}
    repo init -u https://android.googlesource.com/platform/manifest -b master
    cd .repo
    git clone https://github.com/robherring/android_manifest.git -b android-6.0 local_manifests
    cd ..
    repo sync -j20
    cd device/linaro/generic
    make defconfig
    make all
    cd ../../..
    # The following snippet must be run in bash
    bash
    source build/envsetup.sh
    # Select linaro_x86_64-userdebug
    lunch
    make -j7
    # We don't need to use bash any longer
    exit


As of this writing DRM fences related patches by Gustavo Padovan have yet to be included
into AOSP, and therefore have to be included manually until it is upstreamed.
After switching to this branch, the AOSP project has to be rebuilt again. 

    cd $ANDROID_PATH/system/core/
    git remote add padovan git://git.collabora.com/git/user/padovan/android-system-core.git
    git fetch padovan
    git checkout padovan/master

## mkbootimg
Fetch the make boot image script. This script later assembles the boot image, *boot.img*.

    git clone https://android.googlesource.com/platform/system/core.git $ANDROID_TOOLS_PATH


## Run Qemu machine
When running the below script, make sure that the all of the paths from step two
have been exported.

    wget http://memcpy.io/files/2016-08-30/boot_android_qemu.sh -O ${PROJECT_PATH}/boot_android_qemu.sh
    chmod +x ${PROJECT_PATH}/boot_android_qemu.sh
    ${PROJECT_PATH}/boot_android_qemu.sh x86_64


## Conclusion
Hopefully this guide will have enabled you build the required software and run Android on
Qemu with a virtual GPU.
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
