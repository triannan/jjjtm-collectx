PRAGMA foreign_keys = ON;
CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  'filename' VARCHAR(40),
  'name' VARCHAR(20),
  'password' VARCHAR(40) NOT NULL,
  'bio' VARCHAR(256),
  PRIMARY KEY(username)
);

CREATE TABLE collections(
  collectionid INTEGER PRIMARY KEY AUTOINCREMENT,
  collectionname VARCHAR(40) NOT NULL,
  'owner' VARCHAR(20),
  'filename' VARCHAR(64) NOT NULL,
  FOREIGN KEY('owner') REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE item(
  itemid INTEGER PRIMARY KEY AUTOINCREMENT,
  itemname VARCHAR(20) NOT NULL,
  itemseries VARCHAR(20) NOT NULL,
  'filename' VARCHAR(64) NOT NULL,
  'description' VARCHAR(256) NOT NULL,
  'condition' VARCHAR(32) NOT NULL,
  'owner' VARCHAR(20),
  created DATETIME DEFAULT CURRENT_TIMESTAMP,
  collectionid INTEGER NOT NULL,
  FOREIGN KEY('owner') REFERENCES users(username) ON DELETE CASCADE,
  FOREIGN KEY(collectionid) REFERENCES collections(collectionid) ON DELETE CASCADE
);