Title: An Overview of the Panfrost driver
Date: 2019-03-13 16:25
Category: graphics
Tags: linux, open source, gpu, driver, arm, mali, panfrost
Description: During the past few months significant progress has been made on the Open Source Arm Mali GPU driver front, culminating in the Panfrost driver targeting Mali T and G-series of GPUs being available now.
Canonical: https://www.collabora.com/news-and-blog/blog/2019/03/13/an-overview-of-the-panfrost-driver/

![Arm driver timeline](/images/2019-03-13_arm_driver_timeline.png)

The process of reverse engineering Arm GPUs has been going on for a long time,
starting with [Luc Verhaegens](https://github.com/libv) work on the low-end Mali 2/3/400 series of GPUs based
on the Arm Utgard family of GPUs.  
This driver has recently seen a lot new attention and is itself progressing quickly,
which means it will likely be accepted into the kernel soon.  
A piece of trivia is that this GPU architecture was what Arm received when they
purchased the Norwegian GPU IP vendor Falanx Microsystems.

The Mali T and G-series of GPUs are based on the Midgard and Bifrost architectures
respectively, both of which are quite different from the 2/3/400 series.
However the T and G-series are somewhat similar at least when it comes to the
way a driver can be built for them. This is why the Panfrost driver is aiming
to support both architectures with one driver.

<div style="text-align:center;">
<iframe src="https://drive.google.com/file/d/1GqOHbaI2ZcBkYnWBpMXy-LgCyLgzdLRg/preview" width="640" height="480"></iframe>
</div>

At [Embedded World 2019](https://www.embedded-world.de/en) Collabora demoed the
Panfrost driver running kmscube (pictured to the right).
The singleboard computer used was a [Radxa Rock Pi 4](https://rockpi.org),
which was generously sent to us by [Tom Cubie](https://twitter.com/hipboi_).

Panfrost currently runs simple 3D applications like kmscube, the Wayland based
Weston desktop and even more complex 3D benchmarks like glmark2.

This is still a new driver and it is in heavy development currently.

## Current status
There are two semi-parallel parts under development currently; the new kernel
driver and the Mesa userspace driver.

![Panfrost demo](/images/2019-03-13_panfrost.svg)

The new kernel driver is intended to replace the Open Source driver that Arm
provides for its Mali GPUs (mali_kbase). Up until recently the Mesa Panfrost driver
has been used with a shim between the Arm kernel driver and the userspace driver.
While the Arm kernel driver exists, it cannot be accepted into the upstream Linux
kernel project for multiple reasons, but most importantly it doesn't expose the
DRM API that userspace expects of modern GPU drivers in the kernel.

As for the Panfrost Mesa driver, this driver is under heavy development
and is seeing fixes, improvements to the compiler and new features added at a
rapid pace.
This driver is being built on top of the common Gallium driver framework in
Mesa, which means that it will be relatively easy to move features from other
drivers to the Panfrost driver.  
Additionally the Panfrost driver uses the NIR intermediate representation (IR) for
its compiler, which is the most common and most modern IR that Mesa implements.
This again means that new and upcoming features like OpenCL for example, will
be portable from the other Gallium/NIR drivers to Panfrost.

## Thanks
These drivers are community drivers, but have been spearheaded by
[Alyssa Rosenzweig](https://rosenzweig.io/blog/),
[Lyude Paul](https://twitter.com/_Lyude),
[Connor Abott](https://github.com/cwabbott0),
[Rob Herring](https://github.com/robherring) and
Collabora's very own [Tomeu Vizoso](https://blog.tomeuvizoso.net).

I would also like to thank [Tom Cubie](https://twitter.com/hipboi_) for sending
out Rock Pi 4 boards to not just me, but the wider Panfrost development community.

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).