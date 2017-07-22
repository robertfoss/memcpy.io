Title: Android: NXP i.MX6 on Etnaviv Update
Date: 2017-07-21
Category: aosp
Tags: android, android, aosp, imx6, sabre, vivante, etnaviv, linux, collabora
Description: More progress is being made in the area of i.MX6, etnaviv and Android.

Since the last post a lot work has gone into upstreaming and stabilizing the
etnaviv on Android ecosystem. This has involved Android, kernel and Mesa
changes. Many of which are available upstream now. A How-To for getting you
up and running on an iMX6 dev board is available [here](../android-getting-up-and-running-on-the-imx6.html).


## Improvements

#### Modifiers support 
Modifiers support has been accepted into Mesa, GBM and gbm_gralloc.
Modifiers were mentioned in a [previous post](../android-nxp-imx6-buffer-modifier-support.html).


#### Etnaviv driver support for Android
Patches enabling the etnaviv Mesa driver being built for Android have now
landed upstream.

#### Stability on Android
A number for small stability issues present while running Android on i.MX6
hardware have now been fixed, and the platform is now relatively stable.

#### Performance diagnostics
We have a decent understanding that the platform is slow when running the desktop and other apps that have multiple surfaces due to rendering using CPU instead of GPU.
 
#### Etnaviv improvements
Etnaviv performance and feature set have both been increased since Mesa v17.1.


#### EGL support
A number of games using EGL have been successfully run on Android, some
minor graphical issues still remain, but overall games run well and fast.

## Thanks

This work is built on efforts by a lot people:

  * [Aleksander Morgado](https://aleksander.es/) - Independent
  * [Daniel Stone](https://fooishbar.org/) - Collabora
  * Christian Gmeiner - Independent
  * Emil Velikov - Collabora
  * Lucas Stach - Pengutronix
  * Rob Herring - Linaro
  * [Varad Gautam](https://varadgautam.wordpress.com/) - Collabora
  * [Wladimir Van Der Laan](https://laanwj.github.io/) - Independent

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com),
and has been funded by [Zodiac Inflight Innovations](http://zii.aero).
