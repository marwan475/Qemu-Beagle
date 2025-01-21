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

the linaro qemu for is located at https://git.linaro.org/qemu/qemu-linaro.git

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

the executable we need can be found in qemu-linaro/build/arm-softmmu/qemu-system-arm

copy that executable into your working directory
