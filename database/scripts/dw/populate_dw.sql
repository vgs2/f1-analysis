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
EXTRACT(day FROM  date(date)) as day FROM races;


CREATE OR REPLACE VIEW MAIN AS (
SELECT r.resultId, r.driverId, r.raceId, r.constructorId, races.date,
        q.position AS q_pos, r.position, r.points, r.laps, r.fastestLap,
        r.fastestLapSpeed, r.time
FROM results as r
join qualifying as q on (r.raceId = q.raceId and r.driverId = q.driverId)
join races on r.raceId = races.raceId);

CREATE OR REPLACE VIEW AUX AS (
  SELECT resultId, COUNT(*), SUM(pit_stops.milliseconds)
FROM results
JOIN pit_stops ON (results.raceId = pit_stops.raceId and results.driverId=pit_stops.driverId)
GROUP BY resultId
  );
 
 
select main.resultId, driverId, from MAIN 
full outer join AUX on AUX.resultId = MAIN.resultId