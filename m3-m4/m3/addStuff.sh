#!/bin/sh
sqlite3 poem.db <<EOF
INSERT INTO users VALUES ('test@test.com', '0bee89b07a248e27c83fc3d5951213c1', 'testnavn', 'testetternavn');
INSERT INTO sessions VALUES ('1', 'test@test.com');
INSERT INTO poems (poemtext,email) VALUES('ha1 ha2 ha3','test@test.com');


INSERT INTO users VALUES ('test2@test2.com', 'test2', 'testnavn2', 'testetternavn2');
INSERT INTO sessions VALUES ('2', 'test2@test2.com');
INSERT INTO poems (poemtext,email) VALUES('ha2 ha2 ha2', 'test2@test2.com');

INSERT INTO users VALUES ('test10@test10.com', 'test10', 'testnavn10', 'testetternavn10');
INSERT INTO sessions VALUES ('10', 'test10@test10.com');
INSERT INTO poems (poemtext,email) VALUES('ha10 ha10 ha10', 'test10@test10.com');

INSERT INTO users VALUES ('15@15.com', 'test10', 'testnavn10', 'testetternavn10');
INSERT INTO users VALUES ('mailendret@daniel.com', 'abc', 'testnavn10ere', 'testettererernavn10');
EOF


