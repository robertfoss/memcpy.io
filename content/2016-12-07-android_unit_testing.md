Title: Running an Android Unit Test
Date: 2016-12-07 20:23
Category: android
Tags: linux, kernel, android, aosp, adb

Here's a short snippet for running a specific unit test from an Android AOSP
checkout.

A similar approach can be used for any Android module.

    cd aosp
    bash
    source build/envsetup.sh && \
    lunch linaro_arm64-userdebug && \
    mmm system/core/libsync/tests && \
    adb root && \
    adb remount && \
    adb sync && \
    adb shell /data/nativetest64/sync-unit-tests/sync-unit-tests



