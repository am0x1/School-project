#!/bin/sh

# qs="<poem><poemID>15</poemID><poemtext>poem15</poemtext><email>15@15.com</email></poem>"


# poemid=$(echo $qs |cut -d"<" -f3); 
# poemidverdi=$(echo $poemid |cut -d">" -f2); echo $poemidverdi
# poemtext=$(echo $qs |cut -d"<" -f5); 
# poemtextverdi=$(echo $poemtext |cut -d">" -f2); echo $poemtextverdi
# email=$(echo $qs |cut -d"<" -f7);  
# emailverdi=$(echo $email |cut -d">" -f2); echo $emailverdi 

#qs="<poem><poemtext>endretTilDette</poemtext><email>mailendret@endret.com</email></poem>"
#poemtext=$(echo $qs |cut -d"<" -f3); 
#poemtextverdi=$(echo $poemtext |cut -d">" -f2); echo $poemtextverdi
#email=$(echo $qs |cut -d"<" -f5);  
#emailverdi=$(echo $email |cut -d">" -f2); echo $emailverdi 

#qs="/poems/poem/"
#poemcheck=$(echo $qs |cut -d"/" -f3); echo $poemcheck
#logincheck=$(echo $$REQUEST_URI |cut -d"/" -f2); 

#sessionID=$(uuidgen -r) 
#echo $t 

#passordx="test123"
#passordx=$(echo -n passordx | md5sum)
#echo $passordx

#cookie="sessionid=xyz"
#c=$(echo $cookie |cut -d"=" -f2); echo $c; 

#chekcIfSessionIDExist=$(sqlite3 poem.db "SELECT CASE WHEN EXISTS (SELECT * FROM users WHERE sessionID = '1') THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END;")
#echo $chekcIfSessionIDExist

#sessionIDC=$(echo "" |cut -d"=" -f2); 
#echo $sessionIDC

# test="<login><epost>test@test.com</epost><passord>d0940609ced831ffb84f864ed523d91c</passord></login>"

# epost=$(echo $test |cut -d"<" -f3); 
# epostx=$(echo $epost |cut -d">" -f2); 
# passord=$(echo $test |cut -d"<" -f5);  
# passordx=$(echo $passord |cut -d">" -f2); 

# echo $passordx
# echo $epostx

# POST_BODY="id=&poem_text=&request=GET" 
# idpair=$(echo $POST_BODY |cut -d"&" -f1);
# id=$(echo $idpair |cut -d"=" -f2);
# echo $id 


# POST_BODY="id=22&email=22%4022.com&poem_text=22+22+22+22+22&request=POST"

# poemtextpair=$(echo $POST_BODY |cut -d"&" -f3);
# poemtextpair=$(sed '/(\+)+/' $poemtextpair)
# echo -e $poemtextpair | awk '/(\+)+/'
# poemtext=$(echo $poemtextpair | awk '{gsub(/\+/," ");}1')
# poemtext=$(echo $poemtextpair |cut -d"=" -f2);
# echo $poemtext

# s=$(echo $poemtextpair | awk -F'+' '{print $1}') echo $s; 

# s=$(echo $poemtextpair | sed -E 's/(*+*) .+/\1 hello world/') echo $s

# emailpair=$(echo $POST_BODY |cut -d"&" -f2); 
# email=$(echo $emailpair |cut -d"=" -f2); 
# email=$(echo "${email}" | sed 's/%40/@/')
# echo $email

# kropp="<poem><poemtext>poem15</poemtext><email>15@15.com</email></poem>"

# poemtext=$(echo $kropp |cut -d"<" -f3); 
# poemtextverdi=$(echo $poemtext |cut -d">" -f2); echo $poemtextverdi
# email=$(echo $kropp |cut -d"<" -f5);  
# emailverdi=$(echo $email |cut -d">" -f2); echo $emailverdi 

# POST_BODY="id=1&email=lol%40lol.om&poem_text=endre+til+dette&request=PUT"
# # Gir ID
# idpair=$(echo $POST_BODY |cut -d"&" -f1);
# id=$(echo $idpair |cut -d"=" -f2); echo $id 

# emailpair=$(echo $POST_BODY |cut -d"&" -f2); 
# email=$(echo $emailpair |cut -d"=" -f2); 
# email=$(echo "${email}" | sed 's/%40/@/')
# echo $email

# # poemtextpair=$(echo $POST_BODY |cut -d"&" -f3);
# # poemtext=$(echo $poemtextpair | awk '{gsub(/\+/," ");}1')
# # poemtext=$(echo $poemtextpair |cut -d"=" -f2);
# # echo $poemtext


# # Gets poemtextpair from the body.
# poemtextpair=$(echo $POST_BODY |cut -d"&" -f3);
# # Adds space instead of +.
# poemtext=$(echo $poemtextpair | awk '{gsub(/\+/," ");}1')
# poemtext=$(echo $poemtext |cut -d"=" -f2);
# echo $poemtext


s="sesjonsid=1d50aac2-8a2c-4b85-be14-67ce36aa16e2; sesjonsid=97f467b5-eb8c-405b-a330-10a05f5dd92e"
t=$(echo "$s" | awk -F'[:;=]' {'print $2'})
echo $t