PRAGMA foreign_keys = ON;

INSERT INTO users(username, name, bio, filename, password)
VALUES ('jjjtm', 'JJJTM', 'collecting cool stuff', 'peacock.png', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8');

INSERT INTO collections(collectionname, owner, filename)
VALUES ('Sonny Angels', 'jjjtm', 'animals.jpg');

INSERT INTO item(itemname, itemseries, filename, description, condition, owner, collectionid)
VALUES ('Frog', 'Animal', 'frog.jpg', 'cute green frog', 'Like New', 'jjjtm', 1);

INSERT INTO item(itemname, itemseries, filename, description, condition, owner, collectionid)
VALUES ('Koala', 'Animal', 'koala.jpg', 'cute green frog', 'Brand New', 'jjjtm', 1);