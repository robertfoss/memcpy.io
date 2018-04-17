Title: Upstream Linux support for the new NXP i.MX 8M
Date: 2018-04-13 11:39
Category: imx
Tags: imx, i.mx, nxp, imx6, imx8, imx8m, 8m
Description: A quick look into the 2018Q1 status of the i.MX 6 & 8 platforms.

[![Dart iMX 8M](/images/2018-04-13_dart_imx8m.png)
](/images/2018-04-13_dart_imx8m.png)

The i.MX6 platform has for the past few years enjoyed a large effort to add
upstream support to Linux and surrounding projects. Now it is at the point
where nothing is really missing any more. Improvements are still being made,
to the graphics driver for i.MX 6, but functionally it is complete.

[![Etnaviv driver development timeline](/images/2018-04-13_timeline_vivante_kernel_and_mesa.svg)
](/images/2018-04-13_timeline_vivante_kernel_and_mesa.svg)

The i.MX8 is a different story. The newly introduced platform, with hardware still difficult to get access to, is seeing lots of work being done, but much
still remains to be done.

That being said, initial support for the GPU, the Vivante GC7000, is in place
and is able to successfully run Wayland/Weston, glmark, etc.
This should also mean that running Android ontop of the currently not-quite-upstream stack is possible using [drm_hwcomposer](https://gitlab.freedesktop.org/drm-hwcomposer/drm-hwcomposer).

An upstream display/scanout driver does currently not exist, since the display IP in the i.MX 8 is different and more capable than the IP in the i.MX 6 platform, the current imx-drm driver is not capable of supporting it.
A driver is provided by the NXP base support package.
This BSP driver is based on KMS Atomic and supports most of the bells and whistles one would hope for, but is currently not in an upstreamable shape.

[![i.MX8 Kernel Support](/images/2018-04-13_timeline_imx8qm_kernel.svg)
](/images/2018-04-13_timeline_imx8qm_kernel.svg)

But patches for the gpio, clk, netdev & arm-kernel subsystems have been submitted to their respective mailing lists by Lucas Stach.

The direct support for the i.MX8 that has landed in the kernel at this point is mostly done by NXP engineers.

But there are lots of components that currently have no support. The Video Processor Unit IP, the Hantro G1/G2, does not have any upstream support.

[![i.MX8 U-Boot Support](/images/2018-04-13_timeline_imx8qm_i.mx_8_u-boot.svg)
](/images/2018-04-13_timeline_imx8qm_i.mx_8_u-boot.svg)

Looking at bootloader support, U-Boot has good support for the i.MX 8M platform
since early 2018, and can be expected to just work.


## Looking forward
While lot's of support is still missing for the i.MX 8, the platform
is under active development, with many new pieces of the hardware seeing attention.

[Purism](https://puri.sm/) is one of the vendors who currently is actively
working towards full Open Source support of the i.MX8 platform.


## Devboards
[WandPi 8M](https://www.wandboard.org/products/wandpi-8m/) is a series of 3 different boards based on the i.MX 8M platform.

[Nitrogen 8M](https://boundarydevices.com/product/nitrogen8m-imx8/) is another i.MX 8M based option, made by Boundary Devices who also made the popular Sabre Lite series of boards for the i.MX 6.


## Thanks
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
