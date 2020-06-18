/*  
 *  Modulo del encriptador
 */
#include <linux/module.h>	/* necesario para todos los modulos */
#include <linux/kernel.h>	/* necesario KERN_INFO */
#include <linux/fs.h>		/* estructura file_operations - permite el uso de open/close, read/write al dispositivo */
#include <linux/cdev.h>		/* es un dispositivo de caracteres */
#include <linux/semaphore.h>	/* uso de semaforos para sincronización si hace falta */
#include <linux/uaccess.h>	/* copy_to_user ; copy_from_user */

MODULE_AUTHOR("Navarro - Collante 2018");
MODULE_DESCRIPTION("3er trabajo prático - FCEFyN UNC 2018 - Sistemas Operativos 1 // Encriptador de mensajes."); 
MODULE_LICENSE("GPL"); /* para eliminar los mensajes en el log sobre licencia */

/*
 *  PRIMERO. Se crea una estructura para el dispositivo. 
 */
struct fake_device {
	char data[100];
	struct semaphore sem;
}virtual_device;

/*
 *  SEGUNDO. Para luego poder registrar el dispositivo se necesita un objeto 'cdev' y algunas variables. 
 */
#define BUF_LEN 100
#define DEVICE_NAME		"encrypter_navcoll"
struct cdev *mcdev;		/* m es 'my' acrónimo de 'my character device' */
int major_number;		/* almacena el major_number- el cual se extrae de dev_t usando el macro - mknod /director/file c major minor */
int ret;			/* utilizado para almacenar el return de las funciones, necesario porque el stack del kernel es muy pequeño, declarar muchas variables en el stack 						del kernel puede causar problemas, por eso se declaran globalmente */
dev_t dev_num;			/* almacenará el major number que el kernel nos dé */
static char msj[BUF_LEN];	/* almacena el mensaje enviado desde el espacio de usuario */
static int i;			/* variable util */

/* 
 *  funcion que se llama cuando se desea abrir el dispositivo
 *  inode referencia al archivo en el disco y contiene información sobre ese archivo
 *  struct file representa una forma abstracta de abrir un archivo
 */
int device_open(struct inode *inode, struct file *filp){
	/* solo se permite que un proceso a la vez abra este dispositivo usando el semaforo en exclusión mutua */
	if(down_interruptible(&virtual_device.sem) != 0){
		printk(KERN_ALERT "nav-coll(encrypter): error de exclusión mutua\n");
		return -1;
	}
	printk(KERN_INFO "nav-coll(encrypter): dispositivo abierto\n");

	return 0;
}

/*
 *  función llamada cuando el usuario quiere extraer información del dispostivo
 */
ssize_t device_read(struct file* filp, char* bufStoreData, size_t bufCount, loff_t* curOffset){
	/* toma informacion del kernel space(el dispositivo) al user space(procesos) */
	/* copy_to_user (destino, fuente, tamaño_a_transferir) */
	printk(KERN_INFO "navcoll(encrypter): leyendo del dispositivo\n");
	ret = copy_to_user(bufStoreData, msj,bufCount); /* véase que lee el bufer 'msj' sin procesar un desencriptado */

	return ret;
}

/*
 *  función llamada cuando el usuario quiere insertar información al dispositivo. Además ésta es encriptada.
 */
ssize_t device_write(struct file* filp, const char* bufSourceData, size_t bufCount, loff_t* curOffset){
	/* envía informacion del usuario al kernel */
	/* copy_from_user (destino, fuente, cantidad) */

	printk(KERN_INFO "navcoll(encrypter): escribiendo al dispositivo\n");

	for(i = 0;i<bufCount && i<BUF_LEN;i++){
		copy_from_user(msj, bufSourceData, bufCount);
	}
   	for(i = 0;i<bufCount && i<BUF_LEN;i++){		/* encripto el mensaje sumandole un 1 */
        	msj[i] = msj[i] + 1;
    	}

	return 0;
}
EXPORT_SYMBOL(msj);		/* se exporta la variable que contiene el mensaje encriptado para que otros modulos lo utilicen */

/*
 *  funcion llamada cuando el usuario cierra
 */
int device_close(struct inode *inode, struct file *filp){
	/* al ser llamada, es lo opuesto al primer llamado del semaforo, se libera la exclusión mutua  */
	/* otro proceso podrá tomar el dispositivo ahora */
	up(&virtual_device.sem);
	printk(KERN_INFO "navcoll(encrypter): dispositivo cerrado\n");
	
	return 0;
}

/*
 *  indica al kernel que funciones llamar cuando el usuario opera en el archivo del dispositivo
 */
struct file_operations fops = {
	.owner = THIS_MODULE,		/* previene de descargar el modulo cuando las operaciones están en uso */
	.open = device_open,		/* apunta al metodo a llamar cuando se abre el dispositivo */
	.release = device_close,	/* apunta al metodo a llamar cuando se cierra el dispositivo */
	.write = device_write,		/* apunta al metodo a llamar cuando se escribe en el dispositivo */
	.read = device_read		/* apunta al metodo a llamar cuando se lee del dispositivo */
};




//!
//! PUNTO DE PARTIDA DEL DISPOSITIVO
//!
static int driver_entry(void){
	/* TERCERO. Se registra el dispositivo al sistema en dos pasos: */
	/* (1º) se usa la alocación dinamica para asignarle al dispositivo 
	un major number-- alloc_chdrev_region(dev_t*, uint fminor, uint count, char* name) */
	ret = alloc_chrdev_region(&dev_num,0,1,DEVICE_NAME);
		/* en la estructura 'dev_num' se almacena el major y minor number, se comienza con un major 
		number de 0 y crea un maximo de 1 minor number, y se llamará segun el macro DEVICE_NAME */
	if(ret < 0) { /* si retorna un numero negativo hubo un error */
		printk(KERN_ALERT "navcoll(encrypter): falló al alocar major number");
		return ret; /* el error */
	}
	
	major_number = MAJOR(dev_num); /* se extrae el major number de la estructura dev_num (que contiene tanto el major como el minor number) y se lo almacena en la variable */
	printk(KERN_INFO "navcoll(encrypter): major number es %d. \tusar \"mknod /dev/%s c %d 0\" para archivo de dispositivo\n", 
		major_number, DEVICE_NAME, major_number); /* instruye al usuario que utilice '$ dmesg' dándole el comando que debe insertarse ahora que se sabe el major number */
	
	/*(2º) de los dos pasos para registrar el dispositivo */
	/* aloca la estructura del disp de caracteres y lo inicializa apropiadamente */
	mcdev = cdev_alloc();
	mcdev->ops = &fops;	/* struct file_operations */
	mcdev->owner = THIS_MODULE;
	/* ahora que está creado cdev, hay que añadirlo al kernel */
	/* int cdev_add(struct cdev* dev, dev_t num, unsigned int count) */
	ret = cdev_add(mcdev, dev_num, 1); /* mcdev es el disp de car. creado previamente, dev_num es el major number y '1' el minor numb  */
	if(ret < 0) { /* por si hay algun error */
		printk(KERN_ALERT "navcoll(encrypter): error añadiendo cdev al kernel");
		return ret; /* el error */
	}
	
	/* CUARTO. Se inicaliza el semaforo.  */
	sema_init(&virtual_device.sem,1);	/* valor inicial de 1 */

	return 0;
}

//!
//! FUNCION DE SALIDA. REVIERTE TODO LO HECHO 
//! 
static void driver_exit(void){
	/* QUINTO. Deshacer todo en el orden inverso. */
	cdev_del(mcdev); /* quita el dispositivo de caracteres del sistema */

	unregister_chrdev_region(dev_num, 1); /* borra el disp de caracteres registrado en el paso TERCERO */
	printk(KERN_ALERT "navcoll(encrypter): unloaded module");
}

/*
 *  se le indica al kernel donde comienza y donde termina con el modulo
 */
module_init(driver_entry);
module_exit(driver_exit);



/*
 * Instalar los headers con apt:
 * 	'$ sudo apt install linux-headers-4.15.0-43-generic'
 *
 * Luego del '$ make' ejecutar '$ sudo insmod encrypter_navcoll.ko'
 *
 * Mediante '$ lsmod |head' se puede ver el modulo cargado
 *
 * El log se corre mediante '$ tail -n 1 /var/log/kern.log'.
 *
 * La creacion del disp de caracteres: '$ mknod /dev/[nombre-del-modulo] [c/b] [major_number] [major_number]' y se verifica '$ ls /dev'
 * 
 * Para descargar el modulo se ejecuta 'sudo rmmod encrypter_navcoll' y 'sudo rm /dev/encrypter_navcoll'
 *
 */
