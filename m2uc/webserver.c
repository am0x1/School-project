#include <arpa/inet.h>
#include <unistd.h> 
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <sys/file.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

#define LOCAL_PORT 80
#define QUE 10 // Størrelse på for kø ventende forespørsler 

char* content_type(char* extension);
int lagFil();
int checkIfFileExists();

int main () {
    
  struct sockaddr_in  server_address;
  int server_socket, client_socket;

  FILE *file_pointer_error; // file pointer 
  file_pointer_error = fopen("log/debug.log", "a"); // open error.log
  dup2(fileno(file_pointer_error), STDERR_FILENO); // STDERR written to error.log (redigere hit)
  fclose(file_pointer_error); // close file.
  lagFil();
  
  chroot("www"); // set root map.


  // Setter opp socket-strukturen, SOCK_STREAM:TCP, AV_INET IPv4,  IPROTO_TCP socker for ipv4.
  server_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

  // For at operativsystemet ikke skal holde porten reservert etter tjenerens død
  setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int));

  // Initierer lokal adresse
  server_address.sin_family      = AF_INET;
  // caster til u_short localport. 
  server_address.sin_port        = htons((u_short)LOCAL_PORT); 
  // INADDR_ANY spesifiserer IPV4 transport adresse. 
  server_address.sin_addr.s_addr = htonl(         INADDR_ANY);

  // Kobler sammen socket og lokal adresse
  int connect = bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address));
  if (connect == 0) { // connected. 
    fprintf(stderr, "Prosess %d er knyttet til port %d.\n", getpid(), LOCAL_PORT);
  }else{ // not connected. 
    fprintf(stderr, "Failed server socket binding.\n"); 
    exit(1);
  }


    // Demonisering 
    if(fork()) {  // background process.
        
        exit(0); // kill parent. 
    }

    setsid(); // session in child. 
    // Signals that are going to be ignored. 
    signal(SIGTTOU, SIG_IGN); //Terminal output for background process
    signal(SIGTTIN, SIG_IGN); // Terminal input for background process
    signal(SIGTSTP, SIG_IGN); // Stop typed at terminal
    signal(SIGCHLD, SIG_IGN); //Child stopped or terminated

    if(fork()) {
        exit(0); // kill parent. 
    }
    // The deamon has not the access to the terminal anymore.
    chdir("/"); // move current directory off mounted filesystem
    umask(0); // clear any inherited file mode creation mask 
    close(0); // close stdin 

    // dropp root priv
    if(getuid()==0) { // root
        int setgidresult = setgid(1234);
        if(setgidresult == -1) { // failed
            fprintf(stderr, "Dropping group priv failed.\n");
        }
        int setuidresult = setuid(1234);
        if(setuidresult == -1) {
            fprintf(stderr, "Dropping user priv failed.\n"); 
        }
    } else {
        fprintf(stderr, "Not root.\n");
    }

  // Venter på forespørsel om forbindelse
  listen(server_socket, QUE); 
  // Data from http request. Can be potentially 2-8KB, 1 char = 1 Byte. 
  char http_req[8192]; 
  char *file_path;  
  FILE *requested_file; 
  char http_res[BUFSIZ];
  char *bad_http_request = "HTTP/1.1 400 Bad Request\n\nFile not found!\n";
  char *file_type;
  char *http_not_supported = "HTTP/1.1 415 Unsupported Media Type\n\nFile type not supported!\n";
  struct stat filestat; 
    while(1){
    // Aksepterer mottatt forespørsel
    client_socket = accept(server_socket, NULL, NULL);    
    // incoming data stream from socket. 
    recv(client_socket, http_req, sizeof(http_req),0);
    // creating a chil process with fork()
    if(0==fork()) {
        strtok(http_req, " "); // Request type ex GET. 
        file_path = strtok(NULL, " "); // Next line where the file path is.
        if(checkIfFileExists(file_path) == 1) {
          // if . found (we know that is a file ending)
          file_type = strchr(file_path, '.');
          file_type++; // next index where the file type is
          strcpy(file_type, file_type); // file type
          // content type of file.
          char* ct = content_type(file_type);
          char* rct = "content-type: \r\n";
          
         
          // antall tegn etter content type skal settes inn i.
          int x = 13;
          char cth[BUFSIZ];
          strncpy(cth, rct, x);
          cth[x] = '\0';
          strcat(cth, ct);
          strcat(cth, rct + x);
          // test
          //fprintf(stderr, "%s\n", cth); 
    
            // hvis fil type er asis. (fra mp1)
          if(strcmp(file_type, "asis") == 0) {
              requested_file = fopen(file_path, "r");
              while(fgets(http_res, BUFSIZ, requested_file) != NULL) {
                  send(client_socket, http_res, strlen(http_res),0);
              }
              // hvis content typen ikke finnes i mime typer filen.
          } else if(strcmp(ct, "fail") == 0){
                send(client_socket, http_not_supported, strlen(http_not_supported), 0);
          } else {  // behandler bilder annerledes.  
              requested_file = fopen(file_path, "r");// r eller rb.
              if(requested_file != NULL) {
                  // Used to find size in bytes. 
                  fstat(fileno(requested_file), &filestat); 
                  // header (first part)
                  send(client_socket, "HTTP/1.1 200 OK\r\n", strlen("HTTP/1.1 200 OK\r\n"), 0);
                  
                  // cast from st_size(off_t) to char. 
                  char cl[8000000]; // 8mb 
                  sprintf(cl, "%zu", filestat.st_size); 
                  // set content length to the string. 
                  char* rcl = "content-length: \r\n";
                  char clh[BUFSIZ];
                  strncpy(clh, rcl, 15);
                  clh[15] = '\0';
                  strcat(clh, cl);
                  strcat(clh, rcl + 15);

                  // test
                  //fprintf(stderr, "%s\n", clh); 
                  
                  // header (last part)
                 // content length 
                  send(client_socket, clh, strlen(clh), 0) ;
            
                  // content type 
                  send(client_socket, cth, strlen(cth), 0);
                  // header end (empty line)
                  send(client_socket, "\r\n", strlen("\r\n"), 0); 
                  // body 
                  while(fread(http_res, 1, filestat.st_size, requested_file) != 0) {
                        send(client_socket, http_res, filestat.st_size, 0);
                    }
              }
          } 
        } else {
            send(client_socket, bad_http_request, strlen(bad_http_request), 0);
        }
        fclose(requested_file);
        fflush(stdout);
        shutdown(client_socket, SHUT_RDWR);
        exit(0);
    } else {
      close(client_socket);
    }
  }
  return 0;
}

/*
Tatt fra: https://www.delftstack.com/howto/c/c-check-if-file-exists/
Sjekker om filen eksisterer. 
*/
int checkIfFileExists(const char* filename){
    struct stat buffer;
    int exist = stat(filename,&buffer);
    if(exist == 0)
        return 1;
    else  
        return 0;
}

int lagFil() {
    char    *buf = NULL; // buffer for innlest linje
    char    *fel = NULL; // filendelser i linje
    char    *mtl = NULL; // mimetype i linje

    size_t   gln = 0;    // bufferlengde for getline
    int      ant = 0;    // antall lest med getline
    int      tln = 0;    // typelengde (antall tegn)

    // listeelement for filendelse og mimetype
    struct ende_og_type {
        char *ende;
        char *type;
        struct ende_og_type *neste;
    };

    // pekere for liste
    struct ende_og_type *l_hode = malloc(sizeof(struct ende_og_type));
    struct ende_og_type *l_pek  = l_hode;
    struct ende_og_type *l_end  = NULL; // siste element som har innhold

    // aapner mimetype-fila
    FILE *mimefil=fopen("/etc/mime.types", "r");


    while ( 0 < ( ant=getline( &buf, &gln, mimefil ) ) ) {

        if ( buf[0] == '#')  continue; // Hopper over kommentarer
        if ( ant < 2      )  continue; // Hopper over tomme linjer
        buf[ant-1]='\0';               // Fjerner linjeskift

        // Mimetypen (venstre kolonne)
        mtl = strtok(buf,  "\t ");
        tln = strlen(mtl);

        // Gjennomløper filendelsene
        while ( 0 != (fel = strtok(NULL, "\t ")) ) {

            // setter filendelse i liste-element
            l_pek->ende=malloc( strlen(fel) + sizeof('\0') );
            strcpy( l_pek->ende, fel );

            // setter mimetype i liste-element
            l_pek->type=malloc( tln + sizeof('\0') );
            strcpy( l_pek->type, mtl );

            // setter nytt tomt element i lista
            l_pek->neste=malloc(sizeof(struct ende_og_type));
            l_end=l_pek; // referanse til siste element med innhold
            l_pek=l_pek->neste;
        }
    }

    // Lukker fila
    fclose(mimefil);

    // Frigjør minne brukt av strtok
    free(buf);

    // Fjerner siste element (som er tomt)
    l_end->neste=NULL;
    free(l_pek);


    FILE *fptr;
    fptr = fopen("www/typer.txt", "w");
    // Skriver ut lista
    l_pek=l_hode;
    while(l_pek) {
        fprintf(fptr,"%s\t%s\n", l_pek->ende,l_pek->type);
        l_pek=l_pek->neste;
    }
    fclose(fptr);
    return 0;
}

char* content_type(char* extension) {
    FILE* fp;
    char line[1000];
    fp = fopen("typer.txt", "r");
    // problem: får ikke lest typer.txt.
    while(fgets(line, sizeof(line), fp) != NULL) {
        char *extension2 = strtok(line, "\t");
        char *type_and_subtype = strtok(NULL, "\t");
        //char *type = strtok(type_and_subtype, "/");
        //char *subtype = strtok(NULL, "/");
        // Da vet vi at det er samme filtype eks txt = txt
        if(strcmp(extension, extension2) == 0) {
            return type_and_subtype;
            
        }
    }
    // fant ikke
    char* r = "fail";
    return r;
}


