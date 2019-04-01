Title: Running Android next to Wayland
Date: 2019-04-01 18:07
Category: android
Tags: linux, open source, graphics, wayland, android, 3d, acceleration
Description: It's now possible to run Android applications in the same graphical environment as regular Wayland Linux applications with full 3D acceleration.
Canonical: https://www.collabora.com/news-and-blog/blog/2019/04/01/running-android-next-to-wayland/

Running Android has some advantages compared to native Linux applications,
for example with regard to the availability of applications and application
developers.

For current non-Android systems, this work enables a path forward to running
Android applications in the same graphical environment as traditional non-Android
applications are run.

<div style#"text-align:center;">
<iframe width="830" height="460" src="https://www.youtube.com/embed/594fIHWQSj4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## What is SPURV?
SPURV is our experimental containerized Android environment, and
this is a quick overview of what it is.

It's aptly named after the [first robotic fish](https://en.wikipedia.org/wiki/SPURV)
since a common Android naming scheme is fish-themed names. Much like its spiritual
ancestor Goldfish, the Android emulator.

### Other Android Compatibility Layers
This means that Anbox which is LXC based, is different from SPURV in terms of
how hardware is accessed. The hardware access that Anbox provides in indirect,
and through the Qemu Pipes functionality, which is something it adopted from
the Android (goldfish) emulator.

Shashlik and Genimobile are Android on Linux integration layers both based on
Qemu, which means even better security properties than Anbox and certainly SPURV,
but at the cost of an even larger performance penalty.

### Direct Hardware Access
SPURV is different from other Linux desktop integrations for Android
since it offers direct hardware access to the Android application.
This is a choice we made for performance reasons. But has drawbacks, especially
when it comes to security.  
Using direct hardware access does however grant us increased GPU and CPU
performance, which is important since we're targeting embedded platforms
which can have very limited resources.

## Components
SPURV consists of a few different parts, all living in the same [project](https://gitlab.collabora.com/spurv/).

![An overview of the SPURV stack](/images/2019_spurv.svg)

### Android target device
This component integrates SPURV into Android, and it does so by using the
`device` infrastructure that the Android codebase provides.

Devices are normally used to customize an Android build to the
specific needs of a given hardware platform, like a new smartphone
SOC. In the case of SPURV, we're targeting being run inside of
a `systemd-nspawn` container.

### SPURV Audio
This component bridges the Android Audio Hardware Abtraction Layer (HAL) to
the host PulseAudio stack.

### SPURV HWComposer
Integrates Android windows into Wayland. It does so by implementing a HWC-to-Wayland bridge.

HWC is the Android API for implementing display & buffer management, and what it essentially
does in interpret all of the different display buffers that Android applications produce,
and organizes them into one cohesive Desktop.

This protocol is conceptually not unlike the Wayland protocol, which allows for the HWC to
be translated into Wayland. This is essentially what the SPURV HWComposer does.

Additionally it deals with input, like touch screen events and passes them along from Wayland
to Android, this however is unrelated to the HWC API.

### How does it work?
The SPURV Android target device behaves as a faux Android device, and tailors
the Android build to our requirements.

Functions SPURV performs:

 - Customizes defaults.
 - Configures network.
 - Enables an audio bridge from Android to PulseAudio.
 - Enables a graphics bridge from Android to Wayland.

## How can I use it?

Full build instructions as can be found on our [GitLab](https://gitlab.collabora.com/spurv/device_freedesktop/blob/master/spurv/README.md) for the [SPURV project](https://gitlab.collabora.com/spurv).

An overview of setting up:

 - Fetch Android (AOSP) and the Linux kernel,
 - Integrate SPURV into Android,
 - Build Android & Linux Kernel,
 - Build a debootstrap based root filesystem, and
 - Flash Kernel, Android and root filesystem to the device of your choice.

## What comes next?
The next few steps will be adding support for more hardware platforms
in our build scripts, but also optimizing the experience.

In no particular order, this is what we would like to look at next:

 - Bring-up on the i.MX8M with the etnaviv graphics driver.
 - Slimming things down so it takes less time to start an app and consumes less
   RAM for the case where the goal is to just to run a single app.
 - Bring-up on x86 with Ubuntu, publishing runtime binaries.


## Caveats
The way SPURV is implemented means that a full OS is being run in a container,
which has implications both positive and negative.

One of the positive effects is increased isolation of Android applications,
which means improved security and privacy for potentially untrusted applications.

Additionally, this approach allows for Android applications to be run next to
Wayland based applications in a desktop environment.

The downsides relate to hardware access and performance. All hardware access
that is needed by Android has to be passed into the container.
Besides manually having to configure such access using `systemd-nspawn`,
there are also performance costs associated with running a container.
One part of this is the static cost of having to load an entire OS on top
of the base OS, but there are also additional runtime performance penalties
for applications in the container.

## Acknowledgements
   * Pengutronix
   * Zodiac
   * Boundary Devices


This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).