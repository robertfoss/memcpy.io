#!/bin/bash

set -e

PATH="${ANDROID_PATH}/out/host/linux-x86/bin/:$PATH"
ARCH=${ARCH:="$1"}
ARCH=${ARCH:="x86_64"}
QEMU_ARCH=$ARCH

case "$ARCH" in
arm)
    QEMU_OPTS="-cpu cortex-a15 -machine type=virt"
    KERNEL_CMDLINE='console=ttyAMA0,38400 earlycon=pl011,0x09000000 debug nosmp drm.debug=0 rootwait androidboot.selinux=permissive'
    KERNEL=${LINUX_PATH}/arch/arm/boot/zImage
    ;;
arm64)
    QEMU_ARCH="aarch64"
    QEMU_OPTS="-cpu cortex-a57 -machine type=virt"
    KERNEL_CMDLINE='console=ttyAMA0,38400 earlycon=pl011,0x09000000 nosmp drm.debug=0 rootwait rootdelay=5 androidboot.selinux=permissive'
    KERNEL=${LINUX_PATH}/arch/arm64/boot/Image
    ;;
x86_64)
    KERNEL=${LINUX_PATH}/arch/x86/boot/bzImage
    QEMU_OPTS="-enable-kvm -smp 2"
    KERNEL_CMDLINE='console=tty0 console=ttyS0 debug drm.debug=0 androidboot.selinux=permissive'
    ;;
x86)
    QEMU_ARCH="x86_64"
    KERNEL=${LINUX_PATH}/arch/x86/boot/bzImage
    QEMU_OPTS="-enable-kvm -smp 2"
    KERNEL_CMDLINE='console=tty0 console=ttyS0 debug  drm.debug=0 androidboot.selinux=permissive'
    ;;
esac

ANDROID_IMAGE_PATH=${ANDROID_PATH}/out/target/product/linaro_${ARCH}
echo $ANDROID_IMAGE_PATH
if [ ! -f system_${ARCH}.raw -o ${ANDROID_IMAGE_PATH}/system.img -nt system_${ARCH}.raw ]; then
    simg2img ${ANDROID_IMAGE_PATH}/system.img system_${ARCH}.raw
fi
if [ ! -f cache_${ARCH}.raw -o ${ANDROID_IMAGE_PATH}/cache.img -nt cache_${ARCH}.raw ]; then
    simg2img ${ANDROID_IMAGE_PATH}/cache.img cache_${ARCH}.raw
fi
if [ ! -f userdata_${ARCH}.raw -o ${ANDROID_IMAGE_PATH}/userdata.img -nt userdata_${ARCH}.raw ]; then
    simg2img ${ANDROID_IMAGE_PATH}/userdata.img userdata_${ARCH}.raw
fi

${QEMU_PATH}/build/${QEMU_ARCH}-softmmu/qemu-system-${QEMU_ARCH} \
    ${QEMU_OPTS} \
    -append "${KERNEL_CMDLINE}" \
    -m 1024 \
    -serial mon:stdio \
    -kernel ${KERNEL} \
    -initrd ${ANDROID_IMAGE_PATH}/ramdisk.img \
    -drive index=0,if=none,id=system,file=system_${ARCH}.raw \
    -device virtio-blk-pci,drive=system \
    -drive index=1,if=none,id=cache,file=cache_${ARCH}.raw \
    -device virtio-blk-pci,drive=cache \
    -drive index=2,if=none,id=userdata,file=userdata_${ARCH}.raw \
    -device virtio-blk-pci,drive=userdata \
    -netdev user,id=mynet,hostfwd=tcp::5550-:5555 -device virtio-net-pci,netdev=mynet \
    -device virtio-gpu-pci,virgl -display gtk,gl=on \
    -device virtio-mouse-pci -device virtio-keyboard-pci \
    -device nec-usb-xhci,id=xhci                    \
    -device sdhci-pci \
    -d guest_errors \
    -nodefaults \
    $*
