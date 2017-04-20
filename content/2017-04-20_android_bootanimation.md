Title: Android: Changing the bootanimation
Date: 2017-04-20
Category: aosp
Tags: android, aosp, bootanimation, boot, animation, collabora
Description: For various reasons you might want to change the Android boot animation to something other than the stock one, this is how you do it.

There exists [official documentation](https://android.googlesource.com/platform/frameworks/base/+/master/cmds/bootanimation/FORMAT.md)
for how to create a custom boot animation, but unfortunately it is lacking
in actual examples.

So this guide is a bit more hands on.

## Structure of bootanimation.zip

Without covering too much of the same gound as the documentation,
let's have a quick look at what is in a simple bootanimation.zip.

    $ ls -la bootanimation
    total 28
    drwxr-xr-x 4 hottuna hottuna 4096 Apr 19 22:39 .
    drwxr-xr-x 8 hottuna hottuna 4096 Apr 19 22:39 ..
    -rw-r--r-- 1 hottuna hottuna   92 Apr 19 15:21 desc.txt
    drwxr-xr-x 2 hottuna hottuna 4096 Apr 19 12:44 part0
    drwxr-xr-x 2 hottuna hottuna 4096 Apr 19 12:45 part1
    
    $ cat bootanimation/desc.txt 
    1920 1080 30         # WIDTH HEIGHT FPS
    c 5 15 part0 FFFFFF  # TYPE COUNT PAUSE PATH [#RGBHEX] [CLOCK]
    c 5 15 part1 FFFFFF  # TYPE COUNT PAUSE PATH [#RGBHEX] [CLOCK]
    
    ls -la bootanimation/part0 
    total 28
    drwxr-xr-x 2 hottuna hottuna  4096 Apr 19 12:44 .
    drwxr-xr-x 6 hottuna hottuna  4096 Apr 19 15:40 ..
    -rw-r--r-- 1 hottuna hottuna 10688 Apr 19 12:31 0000.png
    -rw-r--r-- 1 hottuna hottuna 10688 Apr 19 12:31 0001.png
    -rw-r--r-- 1 hottuna hottuna 10688 Apr 19 12:31 0002.png
    -rw-r--r-- 1 hottuna hottuna 10688 Apr 19 12:31 0003.png
    -rw-r--r-- 1 hottuna hottuna 10688 Apr 19 12:31 XXXX.png

Note that the "#" comments are mine and not actually present in the files.

An important thing to note with the zip file is needs to have compression
turned off.


## Switch bootanimation

Download [bootanimation.zip](/files/2017-04-20/bootanimation.zip).

    unzip bootanimation.zip
    cd bootanimation
    # Edit desc.txt and partN folders to your needs
    zip -0qry -i \*.txt \*.png \*.wav @ ../bootanimation.zip *.txt part*
    
    # Option 1, use adb to send bootanimation.zip
    adb root
    adb remount
    adb push bootanimation.zip /system/media/bootanimation.zip
    
    # Option 2, bake bootanimation.zip into your AOSP build
    cp bootanimation.zip /opt/aosp/out/target/product/linaro_arm/system/bootanimation.zip
    ./your_favorite_buildscript_here.sh


## References
[bootanimation documentation](https://android.googlesource.com/platform/frameworks/base/+/master/cmds/bootanimation/FORMAT.md)

## Thanks
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
