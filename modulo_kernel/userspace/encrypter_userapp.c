#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h> /* acrónimo de 'file control'. permite llevar a cabo distintas operaciones de control sobre descriptores de archivos */
#include <string.h>
#include <errno.h>

#define DEVICE_ENC "/dev/encrypter_navcoll"
#define DEVICE_DEC "/dev/decrypter_navcoll"
#define BUFFER_LENGTH 100

int main(int argc, char* argv[]){
	
	/* variables utiles a lo largo del código */
	int i, encrypter, decrypter;
	char ch, write_buf[100], read_buf[100], read_buf2[100];
	
	encrypter = open(DEVICE_ENC, O_RDWR); /* abre el archivo encriptador, lee el dispositivo ubicado en el macro DEVICE y lo abre para leer y escribir */
	decrypter = open(DEVICE_DEC, O_RDWR); /* abre el archivo desencriptador, lee el dispositivo ubicado en el macro DEVICE y lo abre para leer y escribir */
	
	if(encrypter == -1){ // si hay algun error abriendo
		printf("el archivo %s no existe o está siendo utilizado por otro proceso \n", DEVICE_ENC);
		exit(-1);
	}

	if(decrypter == -1){ // si hay algun error abriendo
		printf("el archivo %s no existe o está siendo utilizado por otro proceso \n", DEVICE_DEC);
		exit(-1);
	}
	
	/* indicaciones para el usuario */
	//printf("r = leer del dispositivo sin desencriptar\nw = escribir y encriptar al dispositivo\nd = leer del dispostivo y desencriptar\nintroducir comando: ");
	//scanf ("%c %[^\n]", &ch, write_buf);
	switch (*argv[1]){
		case 'w':
			//printf("introducir texto: ");
			//scanf(" %[^\n]", write_buf);
			if (write(encrypter, argv[2], sizeof(write_buf)) < 0){
				//printf("userspace: error escribiendo\n");	
				return errno;		
			}
			//printf("mensaje encriptado satisfactoriamente: %s\n", argv[2]);
			break;
		case 'r':
			//printf("opcion 'r' ingresada\n");
			read(encrypter, read_buf, BUFFER_LENGTH);
			printf("%s\n", read_buf);
			break;
		case 'd':
			//printf("opcion 'd' ingresada\n");
			read(decrypter, read_buf2, BUFFER_LENGTH);
			printf("%s\n", read_buf2);
			break;
		default:
			//printf("comando desconocido\n");
			break;
	}
	close(encrypter);
	close(decrypter);
	return 0;
}

/*
 *  compilar '$ gcc -o userapp userapp.c'
 *  si se trata de correr y sale el error de la linea 15, es porque el dispositivo fue cargado desde un proceso de superusuario
 *  y lo tiene bloqueado, para solucionarlo correr '$ sudo chmod 777 /dev/[nombre_del_disp]
 *
 */
