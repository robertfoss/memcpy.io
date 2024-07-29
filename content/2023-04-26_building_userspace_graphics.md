Title: Setting up a Linux userspace graphics dev environment
Date: 2023-04-26 10:32
Category: graphics
Tags: xwayland, wayland, mesa, graphics, userspace
Description: This is a simple guide for how to build and run Wayland & Weston.

## Set up alternative install location

These build instructions are based on the [Wayland instructions](https://wayland.freedesktop.org/building.html)
from freedesktop.org.

You probably don't want to install experimental builds of software among the usual
software of your operating system, so let's define a prefix for where to install
our builds.

    # Change ALT_LOCAL to any location you like
    export WORK_DIR="/opt"
    export PROJECT_NAME="feature_x"
	export PROJECT_PATH="$WORK_DIR/$PROJECT_NAME"
	export ALT_LOCAL="$PROJECT_PATH/local"
    export LD_LIBRARY_PATH="$ALT_LOCAL/lib"
    export PKG_CONFIG_PATH="$ALT_LOCAL/lib/pkgconfig/:$ALT_LOCAL/share/pkgconfig/"
    export PATH="$ALT_LOCAL/bin:$PATH"
    export ACLOCAL_PATH="$ALT_LOCAL/share/aclocal"
    export ACLOCAL="aclocal -I $ACLOCAL_PATH"

    # Needed by autotools
    mkdir -p "$ALT_LOCAL/share/aclocal"

    export XDG_RUNTIME_DIR="$ALT_LOCAL/xdg"
    export XDG_CONFIG_HOME="$ALT_LOCAL/home"
    export MESA_LOADER_DRIVER_OVERRIDE=zink

## Installing dependencies

Start by installing the build dependencies of mesa, weston and wayland.

    # Enable source packages
    sudo sed -e "s/#\sdeb-src/deb-src/g" -i /etc/apt/sources.list
    sudo apt update

The above step can alternatively be completed using the GUI of your
package manager, by enabling source packages.

    # Install build dependencies of mesa
    sudo apt build-dep gtk3 gtk4 libinp/opt/zink/local/home/weston.iniut mesa wayland weston xserver

    sudo apt install xcb-util-cursor-dev

    # Install a recent version of meson
    pip3 install --user meson

## Building Wayland

    git clone https://gitlab.freedesktop.org/wayland/wayland.git \
    cd wayland \
    meson build/ --prefix="$ALT_LOCAL" \
    ninja -C build/ install \
    cd ..

## Building Wayland Protocols

    git clone https://gitlab.freedesktop.org/wayland/wayland-protocols.git \
    cd wayland-protocols \
    meson build/ --prefix="$ALT_LOCAL" \
    ninja -C build/ install \
    cd ..

## libglvnd OpenGL Vendor-Neutral Dispatch library

    git clone https://github.com/NVIDIA/libglvnd.git \
    cd libglvnd \
    meson setup build/ --prefix="$ALT_LOCAL" \
    ninja -C build/ install \
    cd ..

## libinput
libinput is a dependency of Weston, handles input devices like keyboards, touchpads and mice.

    git clone https://gitlab.freedesktop.org/libinput/libinput \
    cd libinput \
    meson setup build/ --prefix="$ALT_LOCAL" \
    ninja -C build/ install \
    cd ..

## Building Mesa

This build is targeting using swrast for Vulkan and Zink for OpenGL support.

    git clone https://gitlab.freedesktop.org/mesa/mesa.git \
    cd mesa
    meson setup build/ -Dprefix="$ALT_LOCAL" \
      -Degl=x11,wayland,drm \
      -Degl=enabled \
      -Dgallium-drivers=swrast,zink,r600 \
    ninja -C build/ install

    # On some systems the lib paths need to be symlinked
    ln -s "$ALT_LOCAL/lib64" "$ALT_LOCAL/lib"

## Weston
Finally we've built all of the dependencies of Weston and can now build it.

    git clone git://anongit.freedesktop.org/wayland/weston \
    cd weston \
    meson setup build/ --prefix="$ALT_LOCAL" \
    ninja -C build/ install \
    cd ..

## x server
    git clone git://git.freedesktop.org/git/xorg/xserver \
    cd xserver \
    meson setup build/ -Dprefix="$ALT_LOCAL" \
      -Dxkb_bin_dir=/usr/bin \
    ninja -C build/ install \
    cd ..


## Running Weston
That wasn't so bad, it took a little while, but now we're ready to start Weston.
Now, let's fire up a (virtual) terminal. Make sure that you're not running an
X terminal, ssh terminal or serial terminal.

    mkdir -p $XDG_RUNTIME_DIR
    mkdir -p $XDG_CONFIG_HOME/.config
    cp $PROJECT_PATH/weston/build/compositor/weston.ini $XDG_CONFIG_HOME/
    export WESTON_CONFIG_FILE="$XDG_CONFIG_HOME/.config/weston.ini"
    chmod -R 0700 $XDG_RUNTIME_DIR
    chmod -R 0700 $XDG_CONFIG_HOME



    # Make sure that $DISPLAY is unset.
    unset DISPLAY

    # And that $XDG_RUNTIME_DIR has been set and created.
    if test -z "${XDG_RUNTIME_DIR}"; then
      export XDG_RUNTIME_DIR=/tmp/${UID}-runtime-dir
      if ! test -d "${XDG_RUNTIME_DIR}"; then
        mkdir "${XDG_RUNTIME_DIR}"
        chmod 0700 "${XDG_RUNTIME_DIR}"
      fi
    fi

    # Run weston:
    weston

## Try weston applications
Now that we're running weston, let's try some applications.
They're located in the top level directory of weston.

 * weston-terminal
 * weston-flower
 * weston-gears
 * weston-smoke
 * weston-image
 * weston-view
 * weston-resizor
 * weston-eventdemo

When you've started all of your favorite applications you can grab a screenshot 
by pressing **Super + s**, which will save wayland-screenshot.png in your home
directory.

