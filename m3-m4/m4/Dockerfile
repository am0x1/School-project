# MP4

# base image 
FROM hovedbilde 
RUN apk add curl 
COPY *.cgi /usr/local/apache2/cgi-bin/
# Fikser problemet med å kjøre cgi skriptet. 
COPY dbrettigheter.sh /usr/local/apache2/
# Kjører skriptet. 
RUN ["./dbrettigheter.sh"]

EXPOSE 80 