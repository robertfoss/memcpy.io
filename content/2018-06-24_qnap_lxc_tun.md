Title: Configuring QNAP LXC containers for VPNs using TUN
Date: 2018-06-24 22:16
Category: sysadmin
Tags: qnap, container, station, lxc, lxd, vpn, tun, tap
Description: Setting up a QNAP NAS as a VPN client is easy, but setting its containers up for VPNs is harder.

[![Alt text](/images/2018-06-24_lxc_config.png "QNAP Container Station LXC Config")
](/images/2018-06-24_lxc_config.png)

### Configuring the QNAP device
The first step is to SSH into your QNAP device using the _admin_ account.


    ssh admin@NAS_IP
    cat >> /share/Container/container-station-data/lib/lxc/CONTAINER_NAME/config << EOF
    lxc.cgroup.devices.allow = c 10:200 rwm
    EOF

### Configuring the container guest
The second step is open the QNAP web-ui, open the Container Station
application and enter the console of your container.

    sed -i '/exit 0/d' /etc/rc.local
    cat >> /etc/rc.local << EOF
    if ! [ -c /dev/net/tun ]; then
        mkdir -p /dev/net
        mknod -m 666 /dev/net/tun c 10 200
    fi

    exit 0
    EOF

Lastly the container needs to be restarted, and then your VPN application
should be able to access TUN devices and work normally.
