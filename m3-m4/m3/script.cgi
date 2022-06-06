#!/bin/sh

#echo REQUEST_URI:    $REQUEST_URI 
#echo REQUEST_METHOD: $REQUEST_METHOD
#echo
if [ "$REQUEST_METHOD" = "OPTIONS" ]; then 
    echo "Access-Control-Allow-Origin: http://localhost"
    echo "Access-Control-Allow-Credentials: true"
    echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
    echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
    #echo "Access-Control-Max-Age: 86400"
    echo 
fi 
 


  




if [ "$REQUEST_METHOD" = "GET" ]; then
    #echo "Content-type: text/plain; charset=utf-8"
    echo "Content-type: application/xml; charset=utf-8"
    echo "Access-Control-Allow-Origin: *"
    #echo "Access-Control-Allow-Credentials: true"
    #echo "Access-Control-Allow-Methods: GET"
    echo 
    hent=$(echo $REQUEST_URI | sed -e 's/\/.*\///g')
    if  [[ "$hent" =~ ^[0-9]+$ ]]; then 
        cat <<EOF
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="http://localhost:80/test.xsl"?>
<poems>
    <poem>
EOF
  echo -n "select * from poems where poemID=$hent;" | \
  sqlite3 /usr/local/apache2/poem.db -line | \
    sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<\1>\2 <\/\1>/' 
        cat <<EOF
    </poem>
</poems>
EOF
    else
        cat<<EOF
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="http://localhost:80/test.xsl"?>
<poems> 
EOF
        poem_ids=$(sqlite3 /usr/local/apache2/poem.db "SELECT poemID from poems;")
        for poem_id in $poem_ids
        do
        cat<<EOF
    <poem>
EOF
        echo -n "select * from poems where poemID=$poem_id;" | \
            sqlite3 /usr/local/apache2/poem.db -line | \
            sed 's/[[:blank:]]*\(.*\) = \(.*$\)/\t<\1>\2 <\/\1>/' 
        cat << EOF 
    </poem>
EOF
        done
        cat<<EOF
</poems>
EOF
    fi 
fi 

# test 
# Skriv ut en dikt i xml format (dikt 1 i dette tilfellet.)
# curl localhost:8081/poems/poem/1
# Skriv ut alle dikt i xml format
# curl localhost:8081/poems/poem/


# BODY=$(timeout 3 head -c $CONTENT_LENGTH) (kropp) Kanskje vi har bruk for denne (usikker.)
# Hvor vi er. 
if [ "$REQUEST_METHOD" = "POST" ]; then
    
    kropp=$(head -c $CONTENT_LENGTH)
    # Dette er bare test data, må hente data fra xml kropp i $kropp. Må vite XML struktur først. 
    #epostx="test@test.comx"
    #passordx="abc"

    epost=$(echo $kropp |cut -d"<" -f3); 
    epostx=$(echo $epost |cut -d">" -f2); 
    passord=$(echo $kropp |cut -d"<" -f5);  
    passordx=$(echo $passord |cut -d">" -f2); 
    
    
    #passordx=$(echo -n passordx | md5sum) Brukes ikke, men la den ligge her. 
    # gjør om til hash, fjerner "-" på slutten. 
    passordx=$(echo $passordx | md5sum | grep -o '^\S\+') 
    poemcheck=$(echo $REQUEST_URI |cut -d"/" -f3);
    logincheck=$(echo $REQUEST_URI |cut -d"/" -f2); 
    if  [ $logincheck = "login" ]; then 
        # sjekker om bruker eksisterer epost og passord. 
        chekcIfUserExist=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM users WHERE (email = '$epostx' AND psw = '$passordx')) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
        if [ $chekcIfUserExist -eq 1 ]; then 
            # lager session id var "sesjonsid" og setter det som cookie
            sessionID=$(uuidgen -r)
            sessionID=$(echo $sessionID)
            loginSucess="Du har logget inn."
            contentLength=$(echo ${#loginSucess})
            echo "Content-type: text/plain; charset=utf-8"
            echo "Content-Length: $contentLength"
            #echo "Set-cookie: sesjonsid=$sessionID; SameSite=Lax; Expires=Mon, 2 May 2022 07:28:00 GMT;" 
            echo "Set-cookie: sesjonsid=$sessionID; Path=/; SameSite=None; Secure" 
            echo "Access-Control-Allow-Credentials: true"
            echo "Access-Control-Allow-Origin: http://localhost"
            echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
            echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
            echo 
            # setter inn session i databasen. 
            # sessionID vil ikke gå inn her pga sessionID er integer. Så må endre til TEXT.
            sqlite3 /usr/local/apache2/poem.db "INSERT INTO sessions(sessionID,email) VALUES('$sessionID','$epostx');"
            echo $loginSucess
        else 
            # Da har bruker tastet noe feil, eller at bruker ikke eksisterer.
            feil="Feil passord/Bruker eksisterer ikke!"
            contentLength=$(echo ${#feil})
            echo "Content-type: text/plain; charset=utf-8"
            echo "Content-Length: $contentLength"
            echo "Access-Control-Allow-Credentials: true"
            echo "Access-Control-Allow-Origin: *"
            echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
            echo "Access-Control-Allow-Headers: *"
            echo 
            echo $feil
        fi 
    fi 
    
    # henter ut verdiene fra xml. 
    poemtext=$(echo $kropp |cut -d"<" -f3); 
    poemtextverdi=$(echo $poemtext |cut -d">" -f2); #echo $poemtextverdi
    email=$(echo $kropp |cut -d"<" -f5);  
    emailverdi=$(echo $email |cut -d">" -f2); #echo $emailverdi 


    # sjekker om session id fra cookie eksisterer i datbase tabell "sessions"
    #sessionIDC=$(echo $HTTP_COOKIE |cut -d"=" -f2); 
    sessionIDC=$(echo "$HTTP_COOKIE" | awk -F'[:;=]' {'print $2'})
    
    # Sjekker om bruker kan legge til diktet.
    checkPost=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions where sessionID = '$sessionIDC' and email='$emailverdi') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    #chekcIfSessionIDExist=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions WHERE sessionID = '$sessionIDC') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    if [ $poemcheck = "poem" ] && [ $checkPost -eq 1 ]; then 
        sattInn="Dikt er settet inn."
        contentLength=$(echo ${#sattInn})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        #echo "Set-cookie: sesjonsid=$sessionIDC"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo 
        #echo $kropp
    
    

        sqlite3 /usr/local/apache2/poem.db "INSERT INTO poems(poemtext,email) VALUES('$poemtextverdi','$emailverdi');"

        echo $sattInn   
    else 
        # Da har bruker tastet noe feil, eller at bruker ikke eksisterer.
        feil="feil."
        contentLength=$(echo ${#feil})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo 
        echo $feil 
    fi

fi
# Test for å legge inn dikt. (Vil ikke funke på grunn av at if statement sjekker sessionID, bruk den siste testen.)
#curl -X POST -H 'Content-type: text/xml' -d "<poem><poemID>15</poemID><poemtext>poem15</poemtext><email>15@15.com</email></poem>"  localhost:8081/poems/poem/

# test for login 
# curl -X POST -H 'Content-type: text/xml' -d "<login><epost>test@test.com</epost><passord>abc</passord></login>"  localhost:8081/login/ 

# Test for login med full utskrift
# curl -v -X POST -H 'Content-type: text/xml' -d "<login><epost>test@test.com</epost><passord>abc</passord></login>"  localhost:8081/login/

# Test for å legge inn dikt med sessionID. 
#curl --cookie "sesjonsid=1" -X POST -H 'Content-type: text/xml' -d "<poem><poemtext>poem15</poemtext><email>test@test.com</email></poem>"  localhost:8081/poems/poem/

# Vi er her.
if [ "$REQUEST_METHOD" = "PUT" ]; then
    
    kropp=$(head -c $CONTENT_LENGTH)
    
    hentpoemID=$(echo $REQUEST_URI | sed -e 's/\/.*\///g')
    poemtext=$(echo $kropp |cut -d"<" -f3); 
    poemtextverdi=$(echo $poemtext |cut -d">" -f2); #echo $poemtextverdi
    email=$(echo $kropp |cut -d"<" -f5);  
    emailverdi=$(echo $email |cut -d">" -f2); #echo $emailverdi 
    
    # henter sessionID fra cookie. 
    sessionIDC=$(echo $HTTP_COOKIE |cut -d"=" -f2);
    # Sjekker om sessionID er eier av diktet. 1 ja 0 nei.
    checkOwner=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions s INNER JOIN poems p ON s.email = p.email WHERE s.sessionID = '$sessionIDC' AND p.poemID = '$hentpoemID') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    if [ $checkOwner = "1" ]; then
        diktendret="Du har nå endret diktet ditt."
        contentLength=$(echo ${#diktendret})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Set-cookie: sesjonsid=$sessionIDC"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo 
        sqlite3 /usr/local/apache2/poem.db "UPDATE poems SET poemtext = '$poemtextverdi', email = '$emailverdi' WHERE poemID = '$hentpoemID';"
        echo $diktendret
    else 
        diktikkeendret="Du har ikke tilgang til dette diktet."
        contentLength=$(echo ${#diktikkeendret})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo 
        echo $diktikkeendret
    fi 
fi   

#login med utskrift
#curl -v -X POST -H 'Content-type: text/xml' -d "<login><epost>test@test.com</epost><passord>d0940609ced831ffb84f864ed523d91c</passord></login>"  localhost:8081/login/
# siste element blir id, oppdater verdien utifra det (poemID)
# curl -X PUT localhost:8081/poems/poem/1 -H "Content-Type: application/xml" -H "Accept: application/xml" -d "<poem><poemtext>endretTilDette</poemtext><email>mailendret@daniel.com</email></poem>"
# med cookie
#curl --cookie "sesjonsid=762c4adf-f0f8-4f98-8aa2-d012dd889a82" -X PUT localhost:8081/poems/poem/1 -H "Content-Type: application/xml" -H "Accept: application/xml" -d "<poem><poemtext>endretTilDette</poemtext><email>mailendret@daniel.com</email></poem>"

if [ "$REQUEST_METHOD" = "DELETE" ]; then
    # henter sessionID fra cookie. 
    #sessionIDC=$(echo $HTTP_COOKIE |cut -d"=" -f3);
    sessionIDC=$(echo "$HTTP_COOKIE" | awk -F'[:;=]' {'print $2'})
     
    #henter dikt id som skal slettes
    poemid=$(echo $REQUEST_URI | sed -e 's/\/.*\///g')
    #Da vet vi at alle dikt skal slettes 
    poemcheck=$(echo $REQUEST_URI |cut -d"/" -f3);
    #Sjekker om sessionID er eier av diktet. 1 ja 0 nei.
    checkOwner=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions s INNER JOIN poems p ON s.email = p.email WHERE s.sessionID = '$sessionIDC' AND p.poemID = '$poemid') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    if [ $checkOwner -eq 1 ] && [[ "$poemid" =~ ^[0-9]+$ ]]; then 
        diktSlettet="Diktet er slettet."
        contentLength=$(echo ${#diktSlettet})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo
        sqlite3 /usr/local/apache2/poem.db "DELETE FROM poems WHERE poemID='$poemid';"
        echo $diktSlettet 
    fi

    #Da vet vi at alle dikt skal slettes. 
    checkSession=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions s INNER JOIN poems p ON s.email = p.email WHERE s.sessionID = '$sessionIDC') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    if [ $checkSession -eq 1 ] && [ $poemcheck = "poem" ]; then 
        alleDiktSlettet="Alle dine dikt er slettet."
        contentLength=$(echo ${#alleDiktSlettet})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo

        # henter ut epost utifra sessionID.  
        epostforklient=$(sqlite3 /usr/local/apache2/poem.db "SELECT email from sessions where sessionID = '$sessionIDC';") 
        # sletter alle dikt klienten eier. 
        sqlite3 /usr/local/apache2/poem.db "DELETE FROM poems WHERE email = '$epostforklient';"
        echo $alleDiktSlettet 
    fi

    # For å sjekke om bruker er logget inn, for mp4.  
    cs=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions WHERE sessionID = '$sessionIDC') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    csi=$(echo $REQUEST_URI |cut -d"/" -f2); 
    if [ $csi = "check" ] && [ $cs -eq 1 ]; then 
        finnes="finnes"
        contentLength=$(echo ${#finnes})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo 
        echo $finnes 
    fi



    checkSession=$(sqlite3 /usr/local/apache2/poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM sessions WHERE sessionID = '$sessionIDC') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
    logoutcheck=$(echo $REQUEST_URI |cut -d"/" -f2); 
    if [ $logoutcheck = "logout" ] && [ $checkSession -eq 1 ]; then 
        logoutsucess="Du har logget deg ut"
        contentLength=$(echo ${#logoutsucess})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo
        # slett session 
        sqlite3 /usr/local/apache2/poem.db "DELETE FROM sessions WHERE sessionID = '$sessionIDC';"
        echo $logoutsucess
    else 
        feil="feil"
        contentLength=$(echo ${#feil})
        echo "Content-type: text/plain; charset=utf-8"
        echo "Content-Length: $contentLength"
        echo "Access-Control-Allow-Credentials: true"
        echo "Access-Control-Allow-Origin: http://localhost"
        echo "Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS"
        echo "Access-Control-Allow-Headers: Content-type, Content-Length, Set-cookie"
        echo
        echo $feil
    fi 
fi  

#login med utskrift
#curl -v -X POST -H 'Content-type: text/xml' -d "<login><epost>test@test.com</epost><passord>d0940609ced831ffb84f864ed523d91c</passord></login>"  localhost:8081/login/

# Slett med sesjonsid (en gitt dikt). 
# curl --cookie "sesjonsid=1" -X "DELETE" 'localhost:8081/poems/poem/1'
# slett alle dikt 
#curl --cookie "sesjonsid=1" -X "DELETE" 'localhost:8081/poems/poem'
# logge ut 
# curl --cookie "sesjonsid=1" -X "DELETE" 'localhost:8081/logout/'
