# Qemu-Beagle
Qemu setup for Embedded linux development on Beagle Bone Black 


## Goal
- setup qemu to emulate the beagle bone black for embedded linux as close as possible

to start off we need to setup qemu to emulate or machine, the current qemu dosent have support for the beagle bone black

the closest we can get is using a fork of qemu by linaro that has support for the beagle board
- this still works for us as the beagle board and beagle bone black are similar

#### Similarities
- same boot procces
  - MLO -> u-boot -> kernel
- ARM cortex a8 CPU
- the main diffrence is the memory map of the CPUs
  - begale bone black uses am335x
  - beagle board uses omap3
  - we will have to change the config slightly when compiling the linux kernel for qemu vs actual board
 
with this knowledge we know we wont be able to emulate the BBB perfectly but we can get close, as qemu is a great tool for development

## Setting up qemu-linaro

the linaro qemu fork is located at https://git.linaro.org/qemu/qemu-linaro.git

*note this is an old repo meaning python 2 is required to be able to build it, you may have to build python2 yourself 

```sh
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
tar -xzf Python-2.7.18.tgz
cd Python-2.7.18
./configure
make -j$(nproc)
sudo make install -j$(nproc)
```

Building qemu-linaro

```sh

#install dependencies
sudo apt-get install libpixman-1-dev
sudo apt-get install libfdt-dev
sudo apt-get install zlib1g-dev
sudo apt install libglib2.0-dev

# clone into the repo
git clone https://git.linaro.org/qemu/qemu-linaro.git
cd qemu-linaro
mkdir build
cd build
../configure --disable-werror
make -j$(nproc)
make install -j$(nproc)
```
run install if you want this qemu version in your bin, if you already have qemu installed 

then the executable we need can be found in qemu-linaro/build/arm-softmmu/qemu-system-arm

copy that executable into your working directory

```sh
# test build using this command
./qemu-system-arm -M beagle -cpu cortex-a8 -m 512M -clock unix -serial stdio -usb -device usb-kbd -k /usr/share/qemu/keymaps/en-us
```
-k points to keymap file, if you can find that file or is in diffrent path, update path or use the file I provided in the repo

*note the emulation will dump registers and crash, this is normal as we havent given it an img file to boot off of yet

## Building sd card img

our sd card will have 2 partitions
- partition 1 will be the boot partition
  - MLO
  - u-boot
  - uEnv.txt
  - uInitrd
  - uImage
  - board.dtb
- partition 2 will be our root file system

#### Creating virtual img

```sh
# create img file
dd if=/dev/zero of=beaglebone.img bs=1M count=4096
```

create partitions using parted

```sh
parted beaglebone.img

mklabel msdos

mkpart primary fat32 63s 106495s

mkpart primary ext4 106496s 6291455s

quit
```

mark first partition as bootable using fdisk

```sh
fdisk beaglebone.img

3. Mark it as bootable:
    - `a` → Toggle bootable flag.
    - set it to 1
4. Write changes:
    - `w`.
```

format partitions


```sh
# check if any loops are in use
losetup

# kill any in use that you dont need
losetup -d /dev/loop0

#set up loop device
sudo losetup --partscan /dev/loop0 beaglebone.img

#partition 1 FAT 32 bootable
mkfs.vfat -F 32 /dev/loop0p1

#partition 2 linux root file system
mkfs.ext4 /dev/loop0p2

#unmount loop device
losetup -d /dev/loop0

```

## Adding files to sd img

we need to add MLO, u-boot.img, uIntrd, uEnv.txt into the first partition

i have included files for the boot partition in the repo that work with this config, building these files can be tedious so i added them to save time

```sh
mkdir /mnt/beagle

sudo losetup --partscan /dev/loop0 beaglebone.img

sudo mount /dev/loop0p1 /mnt/beagle

sudo cp bootpartition/* /mnt/beagle

umount /mnt/beagle

```

do the same for the root file system, ive also added in a working rfs for time saving

```sh
sudo mount /dev/loop0p2 /mnt/beagle/

sudo cp rfs/* /mnt/beagle/

umount /mnt/beagle

losetup -d /dev/loop0

```

the last step is to build the linux kernel

## Building the linux kernel

you can clone from the offical linux repo or from https://github.com/beagleboard/linux

make sure you have arm cross compilers installed

clone into linux and enter the repo

```sh
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean

# compile for beagle board, required to work on qemu
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- omap2plus_defconfig -j$(nproc)

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- uImage dtbs LOADADDR=0x80008000 -j$(nproc)

```
after compiling make sure to remove thermal driver support, as they cause the kernel to error in qemu

```sh
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig
```
Device Drivers > Thermal drivers > Texas Instruments thermal drivers

disable Texas Instruments SoCs temperature sensor driver  

recompile
```sh
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- uImage dtbs LOADADDR=0x80008000 -j$(nproc)
```

## loading uImage onto bootpartition

```sh
mkdir /mnt/beagle

sudo losetup --partscan /dev/loop0 beaglebone.img

sudo mount /dev/loop0p1 /mnt/beagle

sudo cp linux/arch/arm/boot/uImage /mnt/beagle

# make sure toe rename omap3-beagle.dtb to board.dtb to work with uEnv.txt
sudo cp linux/arch/arm/boot/dts/ti/omap/omap3-beagle.dtb /mnt/beagle/board.dtb

umount /mnt/beagle

```

*make sure to unmount before launching qemu

## booting up

one issue we will face is the init script will fail to mount our rfs so we have to do it manually

Boot up qemu
```sh
./qemu-system-arm -M beagle -cpu cortex-a8 -m 512M -sd ./beaglebone.img -clock unix -serial stdio -usb -device usb-kbd -k /usr/share/qemu/keymaps/en-us
```

wait for u-boot to auto boot, and dont press anything

after a bit, (if it stalls after it gets to mounting on /root just wait) we will drop into an initramfs

from here we will continue and mount the root file system manually

```sh
# mount file system
(initramfs) mount -t ext4 /dev/mmcblk0p2 /root
(initramfs) cp /bin/busybox /root/bin/

# not sure if this is mandatory but the script attempts to do this
(initramfs) mount --bind /dev /root/dev 
(initramfs) mount -t proc proc /root/proc 
(initramfs) mount -t sysfs sysfs /root/sys

# change root file system, it will show an erorr message about tty this is normal
(initramfs) chroot /root

# start bash shell
(initramfs) /bin/bash

```

we are now in a root shell on an emulated beagle 

we can now develop for embedded linux using qemu sicne we compiled our own kernel

to get your kernel changes to work on the actual beagle bone black you will have to use diffrent preset config and .dtb, likely diffrent versions of MLO and u-boot

i will update this once i get to working with the actual board


