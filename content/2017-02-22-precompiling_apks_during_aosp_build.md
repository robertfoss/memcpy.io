Title: Precompiling APK files during Android AOSP build
Date: 2017-02-22 16:55
Category: android
Tags: aosp, apk, dex2oat, android, collabora
Description: By precompiling APK files during AOSP build a few minutes can be shaved off of the development iteration time on most commonly found Android hardware.

## Enable precompilation

    cd /opt/aosp_checkout/

    find . -name BoardConfig.mk
    ./device/huawei/angler/BoardConfig.mk
    ./device/generic/mini-emulator-x86/BoardConfig.mk
    ./device/generic/arm64/BoardConfig.mk
    ./device/generic/mini-emulator-x86_64/BoardConfig.mk
    ./device/generic/mini-emulator-armv7-a-neon/BoardConfig.mk
    ./device/generic/mips/BoardConfig.mk
    ./device/generic/mips64/BoardConfig.mk
    ./device/generic/x86_64/BoardConfig.mk
    ./device/generic/mini-emulator-arm64/BoardConfig.mk
    ./device/generic/mini-emulator-mips/BoardConfig.mk
    ./device/generic/x86/BoardConfig.mk
    ./device/generic/armv7-a-neon/BoardConfig.mk
    ./device/generic/mini-emulator-mips64/BoardConfig.mk
    ./device/lge/bullhead/BoardConfig.mk
    ./device/linaro/generic/linaro_x86_64_only/BoardConfig.mk
    ./device/linaro/generic/linaro_arm64/BoardConfig.mk
    ./device/linaro/generic/linaro_arm64_only/BoardConfig.mk
    ./device/linaro/generic/linaro_x86_64/BoardConfig.mk
    ./device/linaro/generic/BoardConfig.mk
    ./device/linaro/generic/linaro_arm/BoardConfig.mk
    ./device/linaro/hikey/hikey/BoardConfig.mk
    
    # Edit the BoardConfig.mk that you are using for your build
    cd device/linaro/generic/
    nano BoardConfig.mk

    # Add the config option
    WITH_DEXPREOPT := true
    
    # Propagate the new settings
    make defconfig
    make all


## Increase system partition size
Depending on the previous system partition size and how many APKs that are built, you may need to increase the system partition size.

    nano configs/defconfig

    # Change the below variable to something big enough to house all of you binaries
    CONFIG_BOARD_SYSTEMIMAGE_PARTITION_SIZE=1100000000
    
    # Propagate the new settings
    make defconfig
    make all


## Thanks
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
