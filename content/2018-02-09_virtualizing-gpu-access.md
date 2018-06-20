Title: Virtualizing GPU Access
Date: 2018-02-09 11:17
Category: graphics
Tags: linux, gpu, virtualization, virgl, virglrenderer, opengl, vulkan, gles, collabora
Canonical: https://www.collabora.com/news-and-blog/blog/2018/02/12/virtualizing-gpu-access/
Description: Virtualized GPU access is becoming common in the containerized and virtualized application space. Let's have a look at why and how.

For the past few years a clear trend of containerization of applications
and services has emerged. Having processes containerized is beneficial
in a number of ways. It both improves portability and strengthens security,
and if done properly the performance penalty can be low.

In order to further improve security containers are commonly run in
virtualized environments. This provides some new challenges in terms
of supporting the accelerated graphics usecase.

### OpenGL ES implementation
Currently Collabora and Google are implementing OpenGL ES 2.0
support. OpenGL ES 2.0 is the lowest common denominator for many mobile
platforms and as such is a requirement for Virgil3D to be viable on
the those platforms.

That is is the motivation for making Virgil3D work on OpenGL ES hosts.

## How does this work?
This stack is commonly referred to as [Virgil3D](https://virgil3d.github.io/), since all of the parts originated from a project with that name.

[![Alt text](/images/2018-02-09_virgl.svg "Virtualized OpenGL Stack")
](/images/2018-02-09_virgl.svg)

There are a few parts to this implementation.
QEMU, virglrenderer and virtio-gpu. They way it works is by letting the guest
applications speak unmodified OpenGL to the Mesa. But instead of Mesa handing
commands over to the hardware it is channeled through virtio-gpu on the guest
to QEMU on the host.

QEMU then receives the raw graphics stack state (Gallium state) and interprets
it using virglrenderer from the raw state into an OpenGL form, which can be
executed as entirely normal OpenGL on the host machine.

The host OpenGL stack does not even have to be Mesa, and could for example
be the proprietary nvidia stack.

## Trying it out
### Environment

First of all, let's have a look at the development environment.
When doing graphical development I find it quite helpful to set
up a parallel graphics stack in order to not pollute or depend on
the stack of the host machine more than we have to.

    function concatenate_colon {
      local IFS=':'
      echo "$*"
    }

    function add_export_env {
      local VAR="$1"
      shift
      local VAL=$(eval echo "\$$VAR")
      if [ "$VAL" ]; then
        VAL=$(concatenate_colon "$@" "$VAL");
      else
        VAL=$(concatenate_colon "$@");
      fi
      eval "export $VAR=\"$VAL\""
    }

    function prefix_setup {
      local PREFIX="$1"

      add_export_env PATH "$PREFIX/bin"
      add_export_env LD_LIBRARY_PATH "$PREFIX/lib"
      add_export_env PKG_CONFIG_PATH "$PREFIX/lib/pkgconfig/" "$PREFIX/share/pkgconfig/"
      add_export_env MANPATH "$PREFIX/share/man"
      export ACLOCAL_PATH="$PREFIX/share/aclocal"
      mkdir -p "$ACLOCAL_PATH"
      export ACLOCAL="aclocal -I $ACLOCAL_PATH"
    }

    function projectshell {
      case "$1" in
        virgl | virglrenderer)
        	export ALT_LOCAL="/opt/local/virgl"
        	mkdir -p "$ALT_LOCAL"
    		prefix_setup "$ALT_LOCAL"
    		;;
    }

The above snippet is something that I would put in my `.bashrc` or `.zshrc`.
Don't forget so run `source ~/.bashrc` or the equivalent after making changes.

To enter the environment I simply type `projectshell virgl`.

### Build libepoxy

libepoxy is a library for managing OpenGL function pointers for you.
And it is a dependency of virglrenderer, which we'll get to below.

    git clone https://github.com/anholt/libepoxy.git
    cd libepoxy
    ./autogen.sh --prefix=$ALT_LOCAL
    make -j$(nproc --ignore=1)
    make install

### Build virglrenderer

Virgilrenderer is the component that QEMU uses to provide
accelerated rendering.
It receives Gallium states from the guest kernel
via its virtio-gpu interface, which are then translated
into OpenGL on the host. It also translates shaders from the
TGSI format used by Gallium into the GLSL format used by OpenGL.

    git clone git://anongit.freedesktop.org/virglrenderer
    cd virglrenderer
    ./autogen.sh --prefix=$ALT_LOCAL
    make -j$(nproc --ignore=1)
    make install

### Build Mesa
    # Fetch dependencies
    sudo sed -i 's/\#deb-src/deb-src/' /etc/apt/sources.list
    sudo apt update
    sudo apt-get build-dep mesa

    # Actually build Mesa
    git clone https://anongit.freedesktop.org/git/mesa/mesa.git
    cd mesa
    ./autogen.sh \
        --prefix=$ALT_LOCAL \
        --enable-driglx-direct \
        --enable-gles1 \
        --enable-gles2 \
        --enable-glx-tls \
        --with-platforms=drm,x11,wayland \
        --with-dri-drivers=i915,i965,nouveau \
        --with-gallium-drivers=nouveau,swrast,radeonsi \
        --without-vulkan-drivers
    make -j$(nproc --ignore=1)
    make install


### Build QEMU

    git clone git://git.qemu.org/qemu.git
    cd qemu
    ./configure \
        --prefix=$ALT_LOCAL \
        --target-list=x86_64-softmmu \
        --enable-gtk \
        --with-gtkabi=3.0 \
        --enable-kvm \
        --enable-spice \
        --enable-usb-redir \
        --enable-libusb \
        --enable-opengl \
        --enable-virglrenderer
    make -j$(nproc --ignore=1)
    make install

## Set up a VM

As a guest we're going to use Ubuntu 17.10, but just use the latest
release of whatever distro you like. The kernel _has_ to have been
built with the appropriate virtio-gpu Kconfig options though.

    wget http://releases.ubuntu.com/17.10/ubuntu-17.10.1-server-amd64.iso
    qemu-img create -f qcow2 ubuntu.qcow2 35G
    qemu-system-x86_64 \
        -enable-kvm -M q35 -smp 2 -m 4G \
        -hda ubuntu.qcow2 \
        -net nic,model=virtio \
        -net user,hostfwd=tcp::2222-:22 \
        -vga virtio \
        -display sdl,gl=on \
        -boot d -cdrom ubuntu-17.10.1-desktop-amd64.iso

### Run VM

    qemu-system-x86_64 \
    	-enable-kvm -M q35 -smp 2 -m 4G \
    	-hda ubuntu.qcow2 \
    	-net nic,model=virtio \
    	-net user,hostfwd=tcp::2222-:22 \
    	-vga virtio \
    	-display sdl,gl=on

Et Voila! Your guest should now have GPU acceleration!

## Conclusion
Hopefully this guide will have helped you to build all of the software needed to
set up your very own virglrenderer enabled graphics stack.

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).
