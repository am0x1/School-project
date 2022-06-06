#!/bin/sh 

sudo docker stop cgiserverm3  
sudo docker stop cgiserverm3 & sudo docker rm -f cgiserverm3 
#docker rmi 
sudo docker rmi m3image:latest 
