Title: GALLIUM_HUD: Debug Mesa Graphics Performance
Date: 2017-06-28
Category: mesa
Tags: android, aosp, linux, mesa, gallium, hud, peformance, diagnostics, debug, collabora
Description: Debugging graphics performance in a simple and high-level manner is possible for all Gallium based Mesa drivers.


## GALLIUM_HUD

GALLIUM_HUD is a feature that adds performance graphs to applications that describe
various aspects like FPS, CPU usage, etc in realtime.

It is enabled using an environment variable, GALLIUM_HUD, that can be set for GL/EGL/etc
applications. It only works for Mesa drivers that are Gallium based, which means that
the most drivers (with the notable exception of some Intel drivers) support GALLIUM_HUD.

See GALLIUM_HUD options:

    export GALLIUM_HUD=help
    glxgears 

### Android
If you're building Android, you can supply system-wide environment values by doing an
export in the init.rc file of the device you are using, like 
[this](https://customer-git.collabora.com/cgit/android-etnaviv/android-device-linaro-generic.git/commit/?h=android-etnaviv&id=48755378c388707260a8bb50e0fb62a309ded986).

    # Go to android source code checkout
    cd android
    
    # Add export to init.rc (linaro/generic is the device I use)
    nano device/linaro/generic/init.rc
    export GALLIUM_HUD cpu,cpu0+cpu1+cpu2+cpu3;pixels-rendered,fps,primitives-generated



### Linux
If you're using one of the usual Linux distros, GALLIUM_HUD can be enabled by setting
the environtment variable in a place that it loaded early.

    # Add export to /etc/environment
    nano /etc/environment 
    export GALLIUM_HUD cpu,cpu0+cpu1+cpu2+cpu3;pixels-rendered,fps,primitives-generated


## Thanks

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
