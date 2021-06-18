create table constructors(
    constructorId int PRIMARY KEY,
    constructorRef varchar(20),
    name varchar(30),
    nationality varchar(30),
    url varchar(100)

); 

create table fabricante(
    id_fabricante int primary key,
    nome_fabricante varchar(30)
);

create table drivers(
    driverId int primary key,
    driverRef varchar(20),
    number varchar(5),
    code varchar(5),
    forename varchar(30),
    surname varchar(30),
    dob date,
    nationality varchar(30),
    url varchar(100)
    
);

create table circuits(
    circuitId int PRIMARY KEY,
    circuitRef varchar(20),
    name varchar(50),
    location varchar(30),
    country varchar(20),
    lat varchar(20),
    lng varchar(20),
    alt int,
    url varchar(100)
);

create table races(
    raceId int primary key,
    year int,
    round int,
    circuitId int REFERENCES circuits,
    name varchar(30),
    date varchar(20),
    time varchar(20),
    url varchar(100)
);


CREATE TABLE qualifying(
    qualifyId int primary key,
    raceId int REFERENCES races,
    driverId int REFERENCES drivers,
    constructorId int,
    number varchar(5),
    position varchar(10),
    q1 varchar(30),
    q2 varchar(30),
    q3 varchar(30)
);

create table results
(
    resultId int primary key,
    raceId int REFERENCES races,
    driverId int REFERENCES drivers,
    constructorId int REFERENCES constructors,
    number varchar(5),
    grid varchar(5),
    position varchar (5),
    positionText varchar(3),
    positionOrder int,
    points float,
    laps int,
    time varchar(20),
    milliseconds varchar(20),
    fastestLap varchar(20),
    rank varchar(5),
    fastestLapTime varchar(20),
    fastestLapSpeed varchar(20),
    statusId int
);

create table lap_times(
    raceId int REFERENCES races,
    driverId int REFERENCES drivers,
    lap int,
    position int,
    time varchar(20),
    milliseconds int
);

create table pit_stops(
    raceId int references races,
    driverId int references drivers,
    stop int,
    lap int,
    time varchar(20),
    duration varchar(20),
    milliseconds int

);