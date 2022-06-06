#!/bin/sh 

sudo docker build -t m4image .
#sudo docker run --name cgiserverm4 -p 8080:80 m4image
# Kjører på cpu 0 (0-7) 25 prosent av kjernen. 
#sudo docker run --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m4image
# Dropper visse capabilities som vi ikke vil at conteineren skal bruke.
# Info: https://dockerlabs.collabnix.com/advanced/security/capabilities/
#sudo docker run --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m4image

# Dropper disse. 
# CHOWN (Make arbitrary changes to file UIDs and GIDs)
# MKNOD (MKNOD - Create special files using mknod(2))
# SETGID
# SETUID 

#sudo docker run --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 --cap-drop CHOWN MKNOD SETGID SETUID m4image

#sudo docker run --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8080:80 m4image
# Fjerner de rettighetene vi ikke trenger. (MKNOD)
#sudo docker run --cap-drop=MKNOD --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8080:80 m4image

sudo docker run --net prosjektnettverk --ip 172.20.0.20 --cap-drop=MKNOD --name cgiserverm4 --cpuset-cpus 0 --cpu-shares 256 -p 8080:80 m4image

#CHOWN,DAC_OVERRIDE,FSETID,FOWNER,MKNOD,NET_RAW,SETGID,SETUID,SETFCAP,SETPCAP,NET_BIND_SERVICE,SYS_CHROOT,KILL,AUDIT_WRITE

