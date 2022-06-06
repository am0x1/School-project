#!/bin/sh
sqlite3 poem.db <<EOF
PRAGMA foreign_keys = ON;
create table users (
  email TEXT PRIMARY KEY,
  psw TEXT,
  firstNAME TEXT,
  lastNAME TEXT
);
create table sessions (
  sessionID TEXT PRIMARY KEY,
  email TEXT,
  FOREIGN KEY (email)
    REFERENCES users (email)
);
create table poems (
  poemID INTEGER PRIMARY KEY NOT NULL,
  poemtext TEXT,
  email TEXT,
  FOREIGN KEY (email) REFERENCES users (email)
);
EOF