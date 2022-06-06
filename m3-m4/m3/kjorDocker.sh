#!/bin/sh 

sudo docker build -t m3image .
# Kjører på cpu 0 (0-7) 25 prosent av kjerne.
#sudo docker run --name cgiserverm3 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m3image
#sudo docker run --name cgiserverm3 -p 8081:80 m3image
# Test for å se om vi kan slette filer.
#sudo docker run --name cgiserverm3 -p 8081:80 -it --rm -v /bin:/prosjekt/bin m3image /bin/sh

# Fjerner alle rettigheter og legger til de rettighetene vi trenger.
#sudo docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE --cap-add=SETUID --cap-add=SETGID --cap-add=SYS_CHROOT --name cgiserverm3 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m3image
#sudo docker run --cap-drop=MKNOD --name cgiserverm3 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m3image

sudo docker run --net prosjektnettverk --ip 172.20.0.15 --cap-drop=MKNOD --name cgiserverm3 --cpuset-cpus 0 --cpu-shares 256 -p 8081:80 m3image



