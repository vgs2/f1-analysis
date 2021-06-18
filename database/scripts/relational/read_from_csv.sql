COPY drivers(driverId,driverRef,number,code,forename,surname,dob,nationality,url)
FROM '/csv/drivers.csv'
DELIMITER ','
CSV HEADER;

COPY constructors(constructorId,constructorRef,name,nationality,url)
FROM '/csv/constructors.csv'
DELIMITER ','
CSV HEADER;

COPY circuits(circuitId,circuitRef,name,location,country,lat,lng,alt,url)
FROM '/csv/circuits.csv'
DELIMITER ','
CSV HEADER;

COPY races(raceId,year,round,circuitId,name,date,time,url)
FROM '/csv/races.csv'
DELIMITER ','
CSV HEADER;

COPY qualifying(qualifyId,raceId,driverId,constructorId,number,position,q1,q2,q3)
FROM '/csv/qualifying.csv'
DELIMITER ','
CSV HEADER;

COPY results(resultId,raceId,driverId,constructorId,number,grid,position,positionText,positionOrder,points,laps,time,milliseconds,fastestLap,rank,fastestLapTime,fastestLapSpeed,statusId)
FROM '/csv/results.csv'
DELIMITER ','
CSV HEADER;

COPY lap_times(raceId,driverId,lap,position,time,milliseconds)
FROM '/csv/lap_times.csv'
DELIMITER ','
CSV HEADER;

COPY pit_stops(raceId,driverId,stop,lap,time,duration,milliseconds)
FROM '/csv/pit_stops.csv'
DELIMITER ','
CSV HEADER;
