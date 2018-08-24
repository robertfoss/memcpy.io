Title: kms_swrast: A hardware-backed graphics driver
Date: 2018-07-31 09:14
Category: graphics
Tags: collabora, kms_swrast, drm, kms, swrast, dumb, buffer, driver, gpu
Canonical: https://www.collabora.com/news-and-blog/blog/2018/08/01/kms-swrast-hardware-backed-graphics-driver/
Description: kms_swrast is a software driver, built upon the Mesa gallium driver framework, which uses kernel kms drm nodes for memory allocation.

## Stack overview

Let's start with having a look at a high level overview of what the
graphics stack looks like.


[![Alt text](/images/2018-07-31_kms_swrast_overview.svg "Linux graphics stack")
](/images/2018-07-31_kms_swrast_overview.svg)

Before digging too much further into this, lets cover some terminology.

DRM - Direct Rendering Manager - is the Linux kernel graphics subsystem,
which contains all of the graphics drivers and does all of the interfacing with
hardware.  
The DRM subsystem implements the KMS - kernel mode setting - API.

Mode setting is essentially configuring output settings like resolution
for the displays that are being used. And doing it using the kernel means that
userspace doesn't need access to setting these things directly.


[![Alt text](/images/2018-07-31_kms_swrast_mesa.svg "Mesa internals")
](/images/2018-07-31_kms_swrast_mesa.svg)

The DRM subsystem talks to the hardware and Mesa is used by applications through
the APIs it implements. APIs like OpenGL, OpenGL ES, Vulkan, etc.
All of Mesa is built ontop of DRM and libdrm.  

libdrm is a userspace library that wraps the DRM subsystem in order to simplify
talking to drivers and avoiding common bugs in every user of DRM.


[![Alt text](/images/2018-07-31_kms_swrast_detailed.svg "kms_swrast diagram")
](/images/2018-07-31_kms_swrast_detailed.svg)

Looking inside Mesa we find the Gallium driver framework. It is what _most_
of the Mesa drivers are built using, with the Intel i965 driver being the major
exception.

kms_swrast is built using Gallium, with the intention of re-using as much of the
infrastructure provided by Gallium and KMS as possible instead.

kms_swrast itself is backed by a backend, like softpipe or the faster llvmpipe,
which actually implements the 3D primitives and functionality needed in order
to reach OpenGL and OpenGL ES compliance.

Softpipe is the older and less complicated of the two implementations,
whereas is llvmpipe is newer and relies on LLVM as an external dependency.  
But as a result llvmpipe support JIT-compilation for example, which
makes it a lot faster.


## Why is this a good idea?

Re-using the Gallium framework gives you a lot of things for free. And the
driver can remain relatively lightweight.  

Apart from the features that Gallium provides today, you'll also get free
access to new features in the future, without having to write them yourself.  
And since Gallium is shared between many drivers, it will be better tested and
have fewer bugs than any one driver.

kms_swrast is built using DRM and actual kernel drivers, but no rendering
hardware is actually used. Which may seem a bit odd.  

So why are the kernel drivers used for a software renderer? The answer is
two-fold.  

It is what Gallium expects, and there is a kernel driver called VGEM
(Virtual GEM) which was created specifically for this usecase. In order to
not have to make invasive changes to it or make the switch to VGEM right away,
just providing it with access to _some_ driver
is the simplest possible solution. Since the actual hardware is mostly unused,
it doesn't really matter what hardware you use.

The DRM driver is actually only used for a single thing, to allocate a slice
of memory which can be used to render pixels to and then be sent to the display.


## Thanks

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
