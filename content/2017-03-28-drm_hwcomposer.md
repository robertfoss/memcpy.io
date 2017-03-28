Title: Android: Enabling mainline graphics
Date: 2017-03-28 15:18
Category: aosp
Tags: android, aosp, graphics, drm, drm_hwcomposer, hwcomposer, HWC2, collabora
Description: Android uses the HWC API to communicate with graphics hardware. This API is not supported on the mainline Linux graphics stack, but by using drm_hwcomposer as a shim it now is.

[![Alt text](images/2017-03-28_android_graphics_stack.png "Android Graphics Stack")](images/2017-03-28_android_graphics_stack.png)

The traditional Android graphics stack is built ontop of the proprietary drivers of a
GPU vendor, that expose the [HWC](https://source.android.com/devices/graphics/implement-hwc.html)
(Hardware Composer) API. SurfaceFlinger then talks to
the hardware through the HWC API.

Since Android 7.0 version 2 of the HWC API is used by SurfaceFlinger. HWC2 differs in a few
ways from the previous version, for example it supports explicit fencing and using the GPU
as a fallback when compositioning of layers.

Gustavo Padovans work on 
[adding fence support](http://padovan.org/blog/2016/09/mainline-explicit-fencing-part-1/)
to the kernel and the other components of the mainline graphics stack was successfully
upstreamed in [v4.10](http://padovan.org/blog/2017/02/collabora-contributions-to-linux-kernel-4-10/).

Recent work on drm_hwcomposer has added HWC2 support and support for explicit fencing.
And with it we are now able to boot Android on the db410c running the freedreno driver.
But in theory it should work on any mainline kernel graphics stack enabled GPU.

Currently the work is being upstreamed to the
[ChromiumOS repo](https://chromium.googlesource.com/chromiumos/drm_hwcomposer/)
which is the official upstream for drm_hwcomposer.

A number of projects have seen contributions to in order to enable this work:

  * kernel - sync_file, in-fence and out-fence support added.
  * libdrm - fence support added.
  * mesa - support for passing fences added.
  * intel-gpu-tools - sync and fence tests added.
  * drm_hwcomposer - HWC2 and fences support added.

## Thanks
This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
