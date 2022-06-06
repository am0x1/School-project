#!/bin/sh 

# Henter ut variabler av en POST request
# Alt er POST request utenom første gangen man henter siden (GET)
if [ "$REQUEST_METHOD" = "POST" ] ; then
  if [ "$CONTENT_LENGTH" -gt 0 ] ; then
    # legger til kroppen (post) i var kropp. 
      read -n $CONTENT_LENGTH kropp <&0
  fi
fi

# ACTION TYPE kommer fra bodyen. Blir satt i html-form request=ACTION TYPE
type=$(echo $kropp | awk -F "request=" '{print $2}')
# Hvis login. 
if [ "$type" = "LOGIN" ] ; then 
  # Henter ut epost fra kroppen. 
  epostkropp=$(echo $kropp | awk -F'[=&]' {'print $2'})
  # replacer %40 med @
  epostkropp=$(echo "${epostkropp}" | sed 's/%40/@/')
  password=$(echo $kropp | awk -F'[=&]' {'print $4'})
  resp=$(curl -v -X POST --cookie "$HTTP_COOKIE" -H 'Content-type: text/xml' -d "<login><epost>$epostkropp</epost><passord>$password</passord></login>" "http://172.20.0.15:80/login/" 2>&1| grep Set-cookie)
  # Henter cookie fra login.  
  cookie=$(echo "$resp" | awk -F'[:;]' {'print $2'})
  #HTML-Header
  echo "Set-cookie: $cookie"        
fi
# LOGOUT
if [ "$type" = "LOGOUT" ] ; then
  #curl --request DELETE --cookie "$HTTP_cookie" --url "http://172.20.0.15:80/logout/" denne funker ikke. 
  resp=$(curl --cookie "$HTTP_COOKIE" -X "DELETE" "http://172.20.0.15:80/logout/")

  #curl --cookie "sesjonsid=1" -X "DELETE" 'localhost:8081/logout/'
fi

# Header (slutten)
echo "Content-type:text/html;charset=utf-8"
echo "Access-Control-Allow-Origin: *"
echo "Access-Control-Allow-Credentials: true"
echo 

#HTML-BODY
cat << EOF
<!doctype html>
<html>
<head>
<title>Web-grensesnitt</title>
<link rel="stylesheet" href="http://localhost:80/styleweb.css">
</head>
<body>
  <h1>The Big DB of full of Poems</h1>
<form method=POST>
  <div class="container">
    <input type="text" placeholder="email" name="uname">
    <input type="password" placeholder="password" name="psw">
    <button type="submit" name="request" value="LOGIN">Login</button>
    <button type="submit" name="request" value="LOGOUT">Logout</button>
  </div>
</form>
  <div id="form">
    <form method=POST>
      <input type="text" placeholder="Poem ID" name="id"><br>
      <input type="text" placeholder="email" name="email"><br>
      <textarea placeholder="Poem text" name="poem_text" rows="4" cols="50"></textarea><br>
      <input type="radio" name="request" value="GET"> Hent ut ett bestemt dikt / Hent alle dikt<br>
      <input type="radio" name="request" value="POST"> Legg til nytt dikt<br>
      <input type="radio" name="request" value="PUT"> Endre egen dikt<br>
      <input type="radio" name="request" value="DELETE"> Slett eget dikt (gitt dikt id)<br>
      <input type="radio" name="request" value="DELETEALL"> Slett alle egne dikt<br><br>
      <button type="submit">SEND</button>
    </form>
  <a href="http://localhost:80/webside.html">Hjemmeside</a>
  </div>
</div>
</body>
</html>
EOF

# id
idpair=$(echo $kropp |cut -d"&" -f1);
id=$(echo $idpair |cut -d"=" -f2);

# poemtext
poemtextpair=$(echo $kropp |cut -d"&" -f2);
poemtext=$(echo $poemtextpair |cut -d"=" -f2);


if [ "$type" = "GET" ] ; then
  resp=$(curl --request GET "http://172.20.0.15:80/poems/poem/$id")
fi

# Gets poemtextpair from the body.
poemtextpair=$(echo $kropp |cut -d"&" -f3);
# Adds space instead of +.
poemtext=$(echo $poemtextpair | awk '{gsub(/\+/," ");}1')
poemtext=$(echo $poemtext |cut -d"=" -f2);


emailpair=$(echo $kropp |cut -d"&" -f2); 
email=$(echo $emailpair |cut -d"=" -f2); 
email=$(echo "${email}" | sed 's/%40/@/')

# legge til ny dikt
if [ "$type" = "POST" ] ; then
  resp=$(curl --cookie "sesjonsid=$HTTP_COOKIE" -X POST -H 'Content-type: text/xml' -d "<poem><poemtext>$poemtext</poemtext><email>$email</email></poem>"  "http://172.20.0.15:80/poems/poem/")
fi

# endre eksisterende dikt 
if [ "$type" = "PUT" ] ;  then 
  resp=$(curl --cookie "sesjonsid=$HTTP_COOKIE" -X PUT "http://172.20.0.15/poems/poem/$id" -H "Content-Type: application/xml" -H "Accept: application/xml" -d "<poem><poemtext>$poemtext</poemtext><email>$email</email></poem>")
fi

if [ "$type" = "DELETE" ] ;  then 
  resp=$(curl --cookie "$HTTP_COOKIE" -X "DELETE" "http://172.20.0.15/poems/poem/$id")
fi

if [ "$type" = "DELETEALL" ] ;  then 
  resp=$(curl --cookie "$HTTP_COOKIE" -X "DELETE" "http://172.20.0.15/poems/poem")
fi

finnes=$(curl --cookie "$HTTP_COOKIE" -X "DELETE" "http://172.20.0.15:80/check/")

if [ "$type" = "LOGIN" ]; then 
  if ! [ -z $cookie ]; then 
    echo '<br>'
    echo "Logget inn."
    echo '<br>'
  else 
    echo '<br>'
    echo "Feil."
    echo '<br>'
  fi
elif [ -z $type ]; then 
  echo '<br>'
  echo  $resp
  echo '<br>'
elif [ "$type" = "LOGOUT" ]; then 
  echo '<br>'
  echo  $resp
  echo '<br>'
elif [ $finnes = "finnes" ]; then
  echo '<br>'
  echo "Logget inn."
  echo '<br>'
  echo '<br>'
  echo  $resp
  echo '<br>'
else 
    echo '<br>'
    echo  $resp
    echo '<br>'
fi 