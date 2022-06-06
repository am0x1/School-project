#!/bin/bash

ROTFS=$PWD/milp2c

cd       $ROTFS/bin/
cp       /bin/busybox .

for P in $(./busybox --list | grep -v busybox); do ln busybox $P; done;

echo "::once:/bin/webserver" >  $ROTFS/etc/inittab

sudo PATH=/bin unshare -f -p --mount-proc /usr/sbin/chroot $ROTFS bin/init

#  # Inspisere:
#  pstree -p UNSHARE_PID
#  ps -o pid,ppid,uid,tty,cmd PID1 PID2 ...

#  # teste: 
#  curl localhost:8080/hallo.txt

#  # Starte et shell med (alle) samme naverom som PID
#  sudo nsenter -t PID -a
