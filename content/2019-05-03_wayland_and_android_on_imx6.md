Title:  Running Android and Wayland on Embedded Devices
Date: 2019-05-03 10:39
Category: android
Tags: linux, open source, graphics, wayland, android, 3d, acceleration, imx6, nitrogen6
Description: Let's get Android running next to Wayland on an i.MX6 based Nitrogen6_MAX board.
Canonical: https://www.collabora.com/news-and-blog/blog/2019/05/02/running-android-and-wayland-on-embedded-devices/


[A previous post](/running-android-next-to-wayland.html) introduced the [SPURV](https://gitlab.collabora.com/spurv/device_freedesktop/blob/master/spurv/)
Android compatibility layer for Wayland based Linux environment.  
In this post we're going to dig into how you can run an Android application
on the very common i.MX6 based [Nitrogen6_MAX](https://boundarydevices.com/product/nitrogen6max/)
board from [Boundary Devices](https://boundarydevices.com/).

## Install dependencies
    sudo apt install \
        apt-transport-https \
        bmap-tools \
        ca-certificates \
        curl \
        git \
        gnupg2 \
        repo \
        software-properties-common \
        u-boot-tools \
        qemu-kvm


## Set up Docker container for building
    
    # Install Docker
    curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install docker-ce
    
    # Set up privileges for Docker
    sudo usermod -aG docker ${USER}
    su - ${USER}
    
    # Fetch Docker image
    docker pull godebos/debos:latest

## Build
### Build Android

    mkdir android; cd android
    repo init -u https://android.googlesource.com/platform/manifest -b android-9.0.0_r10
    git clone https://gitlab.collabora.com/spurv/android_manifest.git .repo/local_manifests/
    repo sync -j15
    . build/envsetup.sh
    lunch spurv-eng
    make -j12
    cd ..

### Build Linux Kernel

    git clone https://gitlab.collabora.com/spurv/linux.git -b android-container_v5.1-rc5
    cd linux
    sh ../android/device/freedesktop/spurv/build-kernel.sh
    cd ..

### Create root filesystem

Just a kernel does not make an OS, so we're using Debian as a base.  
The way we're going to create the root filesystem is using [debos](https://github.com/go-debos/debos),
which is a tool for creating Debian based OS images.


### Create & flash image

Now we're ready to integrate all of the above into one coherent image.
This is where the Nitrogen6_MAX devboard targeting comes in.  

    git clone https://gitlab.collabora.com/spurv/linux.git
    sudo debos/build_image.sh -b /dev/mmcblk0

The platform specific parts are contained in [uboot_nitrogen6qp-max.scr](https://gitlab.collabora.com/spurv/debos/blob/master/uboot_nitrogen6qp-max.scr)
and [build_image.sh](https://gitlab.collabora.com/spurv/debos/blob/master/build_image.sh).

## Boot!

Pop the flashed SD-card into your device and restart it, and then log in as
`root/root`.

In order to start Android, run one of these two commands:

    # Launch just and Android application
    /home/aosp/run.sh

Starting the Android application might take a minute or two, but Weston should
start immediately.

## Acknowledgments

A lot of different contributors enabled this work, both directly and indirectly.

   * Boundary Devices
   * Pengutronix
   * Zodiac


This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).