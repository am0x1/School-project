#!/bin/sh 

sudo docker stop cgiserverm4
sudo docker stop cgiserverm4 & sudo docker rm -f cgiserverm4
#docker rmi 
sudo docker rmi m4image:latest 


