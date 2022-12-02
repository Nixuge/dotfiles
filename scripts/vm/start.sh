#!/bin/bash
# Helpful to read output when debugging
set -x

# Stop display manager
systemctl stop lightdm.service
## Uncomment the following line if you use GDM
#killall gdm-x-session

# Unbind VTconsoles
echo 0 > /sys/class/vtconsole/vtcon0/bind
echo 0 > /sys/class/vtconsole/vtcon1/bind

# Unbind EFI-Framebuffer
echo efi-framebuffer.0 > /sys/bus/platform/drivers/efi-framebuffer/unbind

# Avoid a Race condition by waiting 2 seconds. This can be calibrated to be shorter or longer if required for your system
sleep 4

# Unbind the GPU from display driver
virsh nodedev-detach pci_0000_27_00_0
virsh nodedev-detach pci_0000_27_00_1
virsh nodedev-detach pci_0000_27_00_2
virsh nodedev-detach pci_0000_27_00_3

# Load VFIO Kernel Module
modprobe vfio-pci
