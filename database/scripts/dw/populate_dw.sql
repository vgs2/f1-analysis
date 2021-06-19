INSERT INTO dim_piloto
SELECT driverId, (forename || ' ' || surname), date_part('year',dob), nationality
FROM drivers;

INSERT INTO dim_construtor
SELECT constructorId,name, nationality 
FROM constructors;

INSERT INTO dim_tempo
SELECT distinct(date), EXTRACT(day FROM  date(date)) as day, EXTRACT(month FROM  date(date)) as month, EXTRACT(year FROM  date(date)) as year
FROM races

INSERT INTO dim_circuito
SELECT circuitId,name, country,lat,lng,alt
FROM circuits;

SELECT distinct(date), EXTRACT(year FROM  date(date)) as year, EXTRACT(month FROM  date(date)) as month, 
EXTRACT(day FROM  date(date)) as day FROM races