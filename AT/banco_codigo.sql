CREATE TABLE Atletas (
    ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Sex CHAR(1),
    Age INT,
    Height INT,
    Weight INT
);

CREATE TABLE Paises (
    NOC CHAR(3) PRIMARY KEY,
    Team VARCHAR(255)
);

CREATE TABLE JogosOlimpicos (
    Games VARCHAR(50) PRIMARY KEY,
    Year INT,
    Season VARCHAR(10),
    City VARCHAR(255)
);

CREATE TABLE Esportes (
    Sport VARCHAR(255) PRIMARY KEY
);

CREATE TABLE Eventos (
    Event VARCHAR(255) PRIMARY KEY,
    Sport VARCHAR(255) REFERENCES Esportes(Sport)
);

CREATE TABLE Medalhas (
    ID_Atleta INT REFERENCES Atletas(ID),
    Games VARCHAR(50) REFERENCES JogosOlimpicos(Games),
    Event VARCHAR(255) REFERENCES Eventos(Event),
    Medal VARCHAR(50),
    PRIMARY KEY (ID_Atleta, Games, Event)
);
