Title: Running Docker privileged inside of LXC / LXD
Date: 2018-12-03 19:00
Category: linux
Tags: linux, virtualization, lxc, lxd, docker, privileged
Description: Being able to run Docker containers inside of LXC containers comes in quite handy due to them solving slightly different issues.

The architecture is a bit of container matroska, but what we're trying to
achieve is running Docker privileged inside of a LXC container on a baremetal
host.

[![Alt text](/images/2018-12-03_docker.png "Docker running inside of LXC")
](/images/2018-12-03_docker.png)

## Setup container on LXC Host

In order to give Docker in the guest privileges, the guest container
itself has to be given privileges.

There is no simple switch for doing this in LXC unfortunately, but a few
config options will do the trick.



    lxc launch images:ubuntu/bionic container

    lxc config set container security.nesting true
    lxc config set container security.privileged true
    cat <<EOT | lxc config set container raw.lxc -
    lxc.cgroup.devices.allow = a
    lxc.cap.drop =
    EOT

    lxc restart container



## Setup docker on container

Just to verify that this works, start a privileged Docker container inside
of the LXC container.

    $ lxc exec container bash
    $ docker run --privileged hello-world
    Unable to find image 'hello-world:latest' locally
    latest: Pulling from library/hello-world
    d1725b59e92d: Pull complete
    Digest: sha256:0add3ace90ecb4adbf7777e9aacf18357296e799f81cabc9fde470971e499788
    Status: Downloaded newer image for hello-world:latest

    Hello from Docker!
    This message shows that your installation appears to be working correctly.

    To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
    3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

    To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

    Share images, automate workflows, and more with a free Docker ID:
    https://hub.docker.com/

    For more examples and ideas, visit:
    https://docs.docker.com/get-started/


## Thanks
This write-up is based [info](https://github.com/lxc/lxd/issues/4902) provided
by Stéphane Graber.