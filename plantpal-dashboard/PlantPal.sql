
-- ****************** SqlDBM: MySQL ******************;
-- ***************************************************;
CREATE TABLE IF NOT EXISTS PlantPal (
 PlantPalID   INTEGER PRIMARY KEY AUTOINCREMENT ,
 WaterVolume  REAL NOT NULL ,
 PlantID      INTEGER NOT NULL ,
 PlantPicture BLOB NULL ,

FOREIGN KEY (PlantID) REFERENCES Plant (PlantID)
);


CREATE TABLE IF NOT EXISTS WaterHistory (
 WaterAmount REAL NOT NULL ,
 PlantPalID  INTEGER NOT NULL ,
 WateredAt   INTEGER NOT NULL ,

FOREIGN KEY (PlantPalID) REFERENCES PlantPal (PlantPalID)
);


CREATE TABLE IF NOT EXISTS Plant (
 PlantID       INTEGER PRIMARY KEY AUTOINCREMENT ,
 Name          TEXT NOT NULL ,
 RequiredWater INTEGER NOT NULL ,
 RequiredLight INTEGER NULL
);


CREATE TABLE IF NOT EXISTS SensorData (
 DataID     INTEGER PRIMARY KEY AUTOINCREMENT,
 MeasuredAt TEXT NOT NULL ,
 PlantPalID INTEGER NOT NULL ,
 Data       REAL NOT NULL ,
 SensorName TEXT NOT NULL ,

FOREIGN KEY (PlantPalID) REFERENCES PlantPal (PlantPalID)
);
