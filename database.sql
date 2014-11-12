drop table if exists pkings;
drop table if exists rounds;
/*
drop table if exists words;

CREATE TABLE words(
    id integer PRIMARY KEY,
    name text not null default 'gre',
    eword text not null,
    cword text not null
);
*/

CREATE TABLE pkings(
    id integer PRIMARY KEY,
    roundname text NOT NULL,
    homename text NOT NULL,
    awayname text NOT NULL,
    hometiming integer NOT NULL,
    awaytiming integer NOT NULL,
    times integer NOT NULL,
    homescore integer NOT NULL,
    awayscore integer NOT NULL,
    pktime timestamp not null default (datetime('now','localtime'))
);

create table rounds(
    id integer PRIMARY KEY,
    roundname text NOT NULL,
    wordid integer NOT NULL,
    eword text NOT NULL,
    ca text NOT NULL,
    cb text NOT NULL,
    cc text NOT NULL,
    cd text NOT NULL,
    answer text NOT NULL
);
