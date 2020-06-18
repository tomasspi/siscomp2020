obj-m := ./encrypter/encrypter_navcoll.o
obj-m += ./decrypter/decrypter_navcoll.o

KERNEL_DIR = /usr/src/linux-headers-$(shell uname -r)

all:	
	$(MAKE) -C $(KERNEL_DIR) SUBDIRS=$(PWD) modules
	$(MAKE) clean


clean:
	rm -rf ./encrypter/*.o ./encrypter/*.mod.* ./encrypter/*.symvers ./encrypter/*.order ./encrypter/*~ ./decrypter/*.o ./decrypter/*.mod.* ./decrypter/*.symvers ./decrypter/*.order ./decrypter/*~ ./*.symvers ./*.order

load:
	$ sudo insmod ./encrypter/encrypter_navcoll.ko && sudo insmod ./decrypter/decrypter_navcoll.ko
	$ dmesg

restore:
	$ sudo rmmod decrypter_navcoll && sudo rmmod encrypter_navcoll
	$ sudo rm /dev/decrypter_navcoll && sudo rm /dev/encrypter_navcoll
	$ ls /dev
	$ lsmod |head
