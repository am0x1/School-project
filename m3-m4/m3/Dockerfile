# MP3 

# base image 
FROM hovedbilde 
# copy files required for the app to run 
RUN apk add sqlite
RUN apk add uuidgen
#RUN apk add --no-cache sqlite~=3.32.1-r0

COPY *.cgi /usr/local/apache2/cgi-bin/
#COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY makeDb.sh /usr/local/apache2/
COPY addStuff.sh /usr/local/apache2/
COPY dbrettigheter.sh /usr/local/apache2/




RUN ["./makeDb.sh"]
RUN ["./dbrettigheter.sh"]
RUN ["./addStuff.sh"]

EXPOSE 80
# build
# $ docker build -t <YOUR_USERNAME>/myfirstapp .

# run  port: 8888 on host and port 5000 in docker. 
# docker run -p 8888:5000 --name myfirstapp YOUR_USERNAME/myfirstapp



