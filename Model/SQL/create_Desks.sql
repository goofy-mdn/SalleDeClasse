CREATE TABLE Desks (
    IdDesk INTEGER PROMARY KEY,
    CoordX INTEGER,
    CoordY INTEGER,
    IdRoom INTEGER,
    FOREIGN KEY (IdRoom) REFERENCES Rooms(IdRoom)
);