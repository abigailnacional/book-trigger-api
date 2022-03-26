SET sql_safe_updates = FALSE;

USE defaultdb;
DROP DATABASE IF EXISTS booktrigs CASCADE;
DROP DATABASE IF EXISTS booktriggers CASCADE;
CREATE DATABASE IF NOT EXISTS booktrigs;

USE booktrigs;

/* Authors, genres, and triggers are all strings that need to
be serialized and then deserialized since we can't include lists
in a SQL table. Age group is optional, so the default is set to null. */
CREATE TABLE books(
    id UUID PRIMARY KEY,
    title varchar(255) NOT NULL,
    authors varchar(255) NOT NULL,
    genres varchar(255) NOT NULL,
    triggers varchar(255) NOT NULL,
    age_group varchar(255),
    published varchar(255),
    publisher varchar(255)
);