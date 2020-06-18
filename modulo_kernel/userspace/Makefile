all: userspace
	$(MAKE) clean

userspace: encrypter_userapp.o
	gcc -o userspace encrypter_userapp.o

encrypter_userapp.o: encrypter_userapp.c
	gcc -c encrypter_userapp.c

clean:
	rm -f *.o
