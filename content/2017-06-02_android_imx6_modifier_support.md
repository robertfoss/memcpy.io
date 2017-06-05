Title: Android: NXP i.MX6 Buffer Modifier Support
Date: 2017-06-02
Category: aosp
Tags: android, aosp, imx6, vivante, etnaviv, linux, mesa, tiling, modifier, collabora
Description: GPUs like those of Intel and Vivante support storing the contents of graphical buffers in different formats. Support for describing these formats using modifiers has now been added to Android and Mesa, enabling tiling artifact free running of Android on the iMX6 platform.

<iframe width="100%" height="380" src="https://www.youtube.com/embed/Dn7hOa9WiYk" frameborder="0" allowfullscreen></iframe>

With modifier support added to Mesa and gbm_gralloc, it is now possible to boot Android on iMX6
platforms using no proprietary blobs at all.
This makes iMX6 one of the very few embedded SOCs that needs no blobs at all to run a full graphics stack.

Not only is that a great win for Open Source in general, but it also makes the iMX6 more attractive as a platform.
A further positive point is that this lays the groundwork for the iMX8 platform, and supporting it will come much easier.


## What are modifiers used for?
Modifiers are used to represent different properties of buffers. These properties can cover a range of
different information about a buffer, for example compression and [tiling](https://en.wikipedia.org/wiki/Tiled_rendering).

For the case of the iMX6 and the Vivante GPU which it is equipped with, the modifiers are related to tiling.
The reason being that buffers can be tiled in different ways (Tiled, Super Tiled, etc.) or not at all (Linear).
Before sending buffers out to a display, they need to have the associated tiling information made available,
so that the actual image that is being sent out is not tiled.

This of course raises the question "Why use tiling at all?", to which the short answer is reduced memory bandwidth, which
translates to power savings, bot of which are desirable in the embedded as well as the mobile space.


## How was support added?
Support was added in two places; Mesa and gbm_gralloc. Mesa has had support added to many of the buffer allocation
functions and to GBM (which is the API provided by Mesa, that gbm_gralloc uses).

gbm_gralloc in turn had support added for using a new GBM API call, GBM_BO_IMPORT_FD_MODIFIER, which imports
a buffer object as well as accompanying information like modifier used by the buffer object in question.


## Getting up and running
Currently the modifiers work is in the process of being upstreamed, but in the meantime it can be
found [here](https://customer-git.collabora.com/cgit/android-etnaviv/). If you'd like to test
this out yourself a How-To can be found [here](../android-getting-up-and-running-on-the-imx6.html).


## Thanks

This work is built on efforts by a lot people:

  * [Varad Gautam](https://varadgautam.wordpress.com/) - Collabora
  * Lucas Stach - Pengutronix
  * [Tomeu Vizoso](http://blog.tomeuvizoso.net/) - Collabora
  * Rob Herring - Linaro
  * Emil Velikov - Collabora
  * [Christian Gmeiner](https://www.christian-gmeiner.info/) - Independent
  * [Wladimir Van Der Laan](https://laanwj.github.io/) - Independent


This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com),
and has been funded by [Zodiac Inflight Innovations](http://zii.aero).
