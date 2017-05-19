Title: Android: Getting up and running on the iMX6
Date: 2017-04-27
Category: aosp
Tags: android, aosp, imx6, sabre, rdu2, vivante, etnaviv, linux, collabora
Description: Getting Android up and running on the iMX6 platform using an open source graphics stack has been impossible up until recently, but now you can. Here's a guide through the steps.

Since the hardware very much matters this is going to be divided into a few parts, the common steps and the hardware specific ones.

This post is a bit of a living document and will be changed over time, and if you have any questions about it, please reach out through email (robert.foss at collabora.com) or irc (tomeu or robertfoss on #dri-devel on freenode).

    Changelog:
    2017-04-27: build_android.sh, setup_sdcard.sh: Added -b [device] support to build_android.sh and setup_sdcard.sh
    2017-05-02: build_android.sh: Don't write to SD-card without -b option
    2017-05-04: Switch git repo urls to shared repository
    2017-05-09: Add compiler installation to apt-get
    2017-05-09: Re-ordered some instructions
    2017-05-10: Add java installation to apt-get
    2017-05-19: Change paths to android-etnaviv instead of client
    2017-05-19: Change kernel branch
    2017-05-19: Add -d, device flag and info about it
    2017-05-19: Add sabrelite board info


## Common steps

    # Install mkimage tool from u-boot and a suitable compiler
    sudo apt install u-boot-tools gcc-arm-linux-gnueabihf openjdk-8-jdk

    mkdir /opt/android
    repo init -u https://android.googlesource.com/platform/manifest -b android-7.1.1_r28
    cd /opt/android/.repo
    git clone https://customer-git.collabora.com/git/android-etnaviv/android_manifest.git local_manifests -b android-etnaviv
    repo sync -j10

    mkdir /opt/imx6_android
    cd /opt/imx6_android

    # Fetch Kconfig, bootloaders and some scripts
    git clone https://customer-git.collabora.com/git/android-etnaviv/android-etnaviv.git .

    # Fetch the Linux Kernel
    git clone https://customer-git.collabora.com/git/android-etnaviv/linux.git -b android-etnaviv

    # This will destroy all data on /dev/mmcblk0 and
    # create boot/system/cache/data partitions
    ./setup_sdcard.sh -b /dev/mmcblk0
    

## Hardware: iMX6 Sabre
### Build Android and Linux

    # Build android, the kernel, and flash it onto an SD-card
    # Run build_android with the correct -d flag
    ./build_android.sh -b /dev/mmcblk0 -d imx6q-sabre
    ./build_android.sh -b /dev/mmcblk0 -d imx6qp-sabre


### Start Android

The SD-card can now be put into the middlemost slot and
the device can be restarted.


## Hardware: iMX6 Sabrelite
### Build Android and Linux

    # Build android, the kernel, and flash it onto an SD-card
    # Run build_android with the correct -d flag
    ./build_android.sh -b /dev/mmcblk0 -d imx6q-sabrelite


### Start Android

The SD-card can now be put into the middlemost slot and
the device can be restarted.


## Hardware: RDU2
### Build Android and Linux

    # Build android, the kernel, and flash it onto an SD-card
    # Run build_android with the correct -d flag
    ./build_android.sh -b /dev/mmcblk0 -d imx6q-zii-rdu2
    ./build_android.sh -b /dev/mmcblk0 -d imx6qp-zii-rdu2

### Install the bootloader

    # Depending if you have a >=13" version of the RDU2
    # use the imx6qp, if <13" then use the imx6q
    
    IMX6_TYPE=imx6q
    IMX6_TYPE=imx6qp
    BAREBOX="zodiac/barebox-zii-${IMX6_TYPE}-rdu2.img"
    
    # Flash bootloader to SD-card
    dd if=${BAREBOX} of=/dev/mmcblk0 bs=1k
    sync

    # Put SD-card in the middle-most slot on the RDU2
    
    # Install lrzsz, since it is used for a ymodem upload
    sudo apt install lrzsz

    # Connect to serial device /dev/ttyUSB2 and
    # /dev/ttyUSB3 with minicom
    # The numbering assumes the RDU2 is the only serial
    # serial device connected
    sudo minicom -s
        +------------------------------------------+
        | A -    Serial Device      : /dev/ttyUSB3
        | B - Lockfile Location     : /var/lock
        | C -   Callin Program      :
        | D -  Callout Program      :
        | E -    Bps/Par/Bits       : 115200 8N1
        | F - Hardware Flow Control : No
        | G - Software Flow Control : No
        |
        |    Change which setting?
        +------------------------------------------+ 
     
    # Connect to Quark console on /dev/ttyUSB3
    # Set boot SD-card as boot source 
    #HostBoot s 0
    reset
    
    # Restart device, connect to barebox loaded just loaded
    # from the SD-card on /dev/ttyUSB2
    pic_setwdt 0 60
    loady
    
    # Using the minicom quickly initiate a ymodem file
    # of the same barebox image you wrote to the SD-card
    # Be quick, the upload will timeout after a few seconds
    
    # Write the bootloader to SPI NOR
    erase /dev/m25p0.barebox
    # Depending on your RDU2 type flash one of the following
    cp barebox-zii-imx6q-rdu2.img /dev/m25p0.barebox
    # Or
    cp barebox-zii-imx6qp-rdu2.img /dev/m25p0.barebox
    
    # Connect to the Quark console on /dev/ttyUSB3 again
    # Set SPI NOR as the boot source
    #HostBoot s 2
    reset
    
    # Connect to the barebox console on /dev/ttyUSB2 again
    # Edit configuration to automatically boot from mmc:
    sedit /env/config
    export global.boot.default=/env/boot/mmc
    export global.bootm.image=/mnt/mmc1.0/android_zImage
    export global.bootm.initrd=/mnt/mmc1.0/android_ramdisk.img.gz
    export global.bootm.oftree=/mnt/mmc1.0/imx6qp-zii-rdu2.dtb
    export global.linux.bootargs.base="console=ttymxc0,115200 console=tty0 rw rootwait ip=dhcp buildvariant=userdebug debug ignore_loglevel root=/dev/mmcblk0p2 rootfstype=ext4 rootwait init=/init printk.devkmsg=on verbose enforcing=0 androidboot.selinux=permissive drm.debug=0x00"

    sedit /env/boot/mmc
    #!/bin/sh
    detect mmc1
    mkdir -p /mnt/mmc1.0
    automount -d /mnt/mmc1.0 'mount /dev/mmc1.0 /mnt/mmc1.0'
    bootm

    pic_setwdt 0 60     # Disable watchdog

    exit

### Start Android

The SD-card created in the common steps can now be put into
the middlemost slot and the device can be restarted.

## Thanks

This work is built on efforts by a lot people:

  * Pengutronix who's been doing i.MX6 platform work.
  * Christian Gmeiner, Wladimir Van Der Laan, and the other etanviv developers.
  * Rob Herring at Linaro for getting the ball rolling with AOSP for Zii.
  * Andrey Smirnov for driver support for the RDU2 such as i.MX6 PCI, ARM PL310 L2 Cache controller, RTC, and other i.MX6qp driver fixups.

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
