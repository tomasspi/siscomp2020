- Instalar *flex* y *bison*:

  `$sudo apt install flex bison -y`

- Ejecutar los siguientes comandos:

  ```shell
  $ make
  $ cd ./userspace
  $ make
  $ cd ../encrypter
  $ sudo insmod encrypter_navcoll
  $ cd ../decrypter
  $ sudo insmod decrypter_navcoll
  $ dmesg
  $ cd ../userspace
  $ ./userspace
  ```
