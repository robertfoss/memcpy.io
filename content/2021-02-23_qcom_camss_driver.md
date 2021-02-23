Title: Upstream camera support for Qualcomm platforms
Date: 2021-02-23 14:54
Category: kernel
Tags: linux, kernel, camera, v4l2, qualcomm, camss, sdm845, yocto, open embedded, db845c, sdm845
Description: The CAMSS driver for Qualcomm Image Signal Processors (ISPs) isn't new, but now has support for the next generation of ISP architecture.



[Linaro](https://www.linaro.org/) has been working together with Qualcomm to enable camera support on
their platformssince 2017. The Open Source CAMSS driver was written to support the ISP IP-block with
the same name that is present on Qualcomm SoCs coming from the smartphone space.

The first development board targeted by this work was the DragonBoard 410C, which was followed in 2018 by
DragonBoard 820C support. Recently support for the Snapdragon 660 SoC was added to the driver,
which will be part of the v5.11 Linux Kernel release. These SoCs all contain the CAMSS
(Camera SubSystem) version of the ISP architecture.

Currently, support for the ISP found in the Snapdragon 845 SoC and the DragonBoard 845C is in
the process of being upstreamed to the mailinglists. Having seen major changes, the ISP is
no longer referred to as CAMSS, but is instead known as Titan.

The Titan architecture offers improvements in resolution, framerates and most other dimensions
of the ISP, and is the latest architecture shipped on modern Qualcomm chipsets.


Overview
--------

CAMSS is a V4L2 (Video for Linux 2) Linux driver which focuses on supporting the basic use cases of the ISP,
such as receiving the [MIPI CSI-2](https://www.mipi.org/specifications/csi-2) signals from the sensors,
decoding them, and then writing them to memory. This leaves a lot of functionality typically provided
by an ISP unimplemented, but that is intentional as the development priority has been to enable the
data path from camera sensor to userspace.

The sub-components that the CAMSS drivers supports are the following:

 - CSIPHY - the CSI PHYsical layer manages the physical electrical signals sent by camera sensors.

 - CSID - the CSI Decoder decodes the CSI-2 encoded data transmitted by the sensors

 - VFE - the Video Front End formats received data and exposes it through to further hardware blocks.
         The VFE block was renamed to IFE (Image Front End) in the Titan architecture.

 - RDI - the Raw Dump Interface is exposed by the VFE, and is used to write the raw decoded
         CSI output directly to memory.

 - PIX - the PIXel interface is exposed by the VFE, and is used to transmit data prepared
         for advanced processing by more specialized hardware blocks.

 - ISPIF - the Image Signal Processor InterFace ties together a lot of specialized hardware blocks
           into a data pipeline which can provide various levels of additionalprocessing.


### Qualcomm ISP Gen 1 - CAMSS

The first generation of the ISP hardware block supported by the (aptly named) CAMSS driver is
called CAMSS by Qualcomm.

[![Alt text](/images/2021-02-23_camss_gen1.svg "Qualcomm CAMSS ISP Generation 1")
](/images/2021-02-23_camss_gen1.svg)

The CSIPHY, CSID & VFE IP-blocks are relatively fully featured, but some functionality like
Virtual Channels are not implemented. However, a more substantial limitation of the ISPIF
support is that only basic cropping and rotation is currently implemented.

An obstacle caused by this limited ISPIF functionality is that it's not able to do format
conversions using the ISP. So whatever format the camera sensor is outputting, is directly
output to userspace. This can be a problem for Bayer pixel format sensors, because
they're poorly supported by userspace applications and require at least debayering to be
done in a post-processing step before the output can be viewed.



### Qualcomm ISP Gen 2 - Titan

The next iteration of the Qualcomm ISP architecture is called Titan. The changes from Gen1
to Gen2/Titan can be summarized in two parts.

[![Alt text](/images/2021-02-23_camss_gen2_titan.svg "Qualcomm CAMSS ISP Generation 2, Titan")
](/images/2021-02-23_camss_gen2_titan.svg)

The Titan frontend blocks (CSIPHY, CSID & VFE) are almost identical between Gen1 and Gen2
with only minor structural changes and improvements.

However, the image processing pipeline has been revamped, and the ISPIF no longer exists.
What replaces it is an embedded CPU which is fed commands and in turn configures the
data processing blocks. Adding support for this CPU is beyond the current scope
of CAMSS due to the amount of work it would take to enable and the lack of documentation
for the CPU command stream. However, userspace applications are able to manage some of this
post processing. This is enough to support the most basic use cases, but many will be CPU/GPU
intensive and likely not have the same quality as an ISP based implementation would.


Future
------

Linaro will continue to maintain this driver, and is likely to extend it to support
additional hardware platforms. However, contributions are very welcome and platforms
like the SDM630 and SSDM660 have already had support contributed to the CAMSS driver.

Currently [libcamera](https://libcamera.org/index.html) is a very useful development tool
for working with CAMSS. It is more flexible than most V4L2 applications, and using the
[libcamera/qcam](https://libcamera.org/getting-started.html) application makes it possible
to view live output of even Bayer camera sensors without the ISP doing any debayering.

Recent Linaro contributions towards libcamera have enabled GPU accelerated format conversion
and debayering for the [libcamera/qcam](https://libcamera.org/getting-started.html) test
application, you can read more about that
[here](https://www.linaro.org/blog/accelerating-libcamera-qcam-format-conversion-using-opengl-shaders/).
Linaro has also contributed the Open Embedded [libcamera recipe](http://cgit.openembedded.org/meta-openembedded/tree/meta-multimedia/recipes-multimedia/libcamera/libcamera.bb?h=master)
for developers building their products with Yocto Project based Linux distributions.

Other Linaro contributions to the Linux camera landscape include work in both
userspace with libcamera and in the kernel with camera sensor drivers,
ISP drivers and V4L2 API work.

Further developments regarding software and GPU debayering are expected for libcamera,
and hopefully the community will see libcamera debayering enabled for all of its data paths
soon enough.


Acknowledgments
---------------

A lot of different contributors enabled this work, both directly and indirectly.

   * Todor Tomov for creating the camss driver.
   * [Jonathan Marek](https://gitlab.freedesktop.org/flto) for trail-blazing Titan driver work.
   * [Andrey Konovalov](https://github.com/andrey-konovalov) for testing, finding bugs & being a great sounding board.
   * Qualcomm for sponsoring and providing hardware documentation.

This post has been a part of work undertaken by my employer [Linaro](https://www.linaro.org/blog/upstream-camera-support-for-qualcomm-platforms/).
