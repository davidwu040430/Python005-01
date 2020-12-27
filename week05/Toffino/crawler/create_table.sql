create table review (
    id int(11) NOT NULL AUTO_INCREMENT,
    author varchar(50),
    content text NOT NULL,
    rate float,
    created_on Date,
    PRIMARY KEY (id),
    FULLTEXT KEY content_fulltext(content)
);