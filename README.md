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
  - we will have to change the device tree blob when flashing the linux kernel for qemu vs actual board
 
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

we need to add MLO, u-boot.bin, uIntrd, uEnv.txt into the first partition

i have included files for the boot partition in the repo that work with this config, building these files can be tedious so i added them to save time

```sh
mkdir /mnt/beagle

sudo losetup --partscan /dev/loop0 beaglebone.img

sudo mount /dev/loop0p1 /mnt/beagle

sudo cp bootpartition/* /mnt/beagle

umount /mnt/beagle

```

## Getting the Root file system for Debian 12 Bookworm

we are gonna steal it from the offical image

```sh
wget https://beagleboard.org/latest-images/am335x-debian-12.2-iot-armhf-2023-10-07-4gb.img.xz
unxz am335x-debian-12.2-iot-armhf-2023-10-07-4gb.img.xz

sudo losetup --partscan /dev/loop1 am335x-debian-12.2-iot-armhf-2023-10-07-4gb.img
sudo mount /dev/loop1p1 /mnt/beagle

mkdir rfs
sudo cp /mnt/beagle/* rfs -r

sudo umount /mnt/beagle

losetup -d /dev/loop1
 
```
now copy rfs to second partition of img

```sh
sudo mount /dev/loop0p2 /mnt/beagle/

sudo cp rfs/* /mnt/beagle/

umount /mnt/beagle

losetup -d /dev/loop0

```

the last step is to build the linux kernel

## Building the linux kernel

you can clone from https://github.com/beagleboard/linux

make sure you have arm cross compilers installed

clone into linux and enter the repo

the beagle bone black uses version 5.10.168-ti-r63
*note this version dosent compile so i switched to 5.10.168-ti-r77

```sh
git checkout 5.10.168-ti-r77

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- distclean

# compile for beagle board, required to work on qemu
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi- omap2plus_defconfig -j$(nproc)

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


Boot up qemu
```sh
./qemu-system-arm -M beagle -cpu cortex-a8 -m 512M -sd ./beaglebone.img -clock unix -serial stdio -usb -device usb-kbd -k /usr/share/qemu/keymaps/en-us
```

Cancel u-boot auto boot

run these commands
```sh
setenv mmcrootfstype ext4

saveenv

boot
```

we are now in a root shell on an emulated beagle 

we can now develop for embedded linux using qemu since we compiled our own kernel

# Getting the kernel on the real board

#### Updating the img file

```sh
# make a copy of the beaglebone.img with a new name
cp beaglebone.img beagle.img

sudo losetup --partscan /dev/loop2 beagle.img

sudo mount /dev/loop2p1 /mnt/beagle

# remove board.dtb a

# move linux/arch/arm/boot/dts/am335x-boneblack.dtb into /mnt/beagle/ and rename it to board.dtb

# now unmount

sudo umount /mnt/beagle
```

## Flashing the img to the microsd

Install Balena Etcher from https://etcher.balena.io/

use this to flash the img to the microsd using this

ok now we have or microsd card setup time to boot

## Setup UART serial output

![Screenshot from 2020-08-25 22-18-12](https://user-images.githubusercontent.com/32474027/91179255-3c4f7a00-e721-11ea-8006-a49083c3fb5e.png)

connect UART using that usb thing

## Accessing serial output

this wont work with wsl so get a linux virutal machine using virtual box

connect the USB to the virtual machine

it should be under /dev/ttyUSB0

```sh
tio /dev/ttyUSB0
```

## Powering on the machine

when powered off
- insert microsd
- hold BOOT button
- now hold the power button
- you should see output in the tio terminal



