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
 
whit this knowledge we know we wont be able to emulate the BBB perfectly but we can get close, as qemu is a great tool for development
