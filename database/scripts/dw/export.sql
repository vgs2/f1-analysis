COPY dim_piloto TO 'database/csv/DIM_piloto.csv' DELIMITER ',' CSV HEADER;
COPY dim_construtor TO 'database/csv/DIM_construtor.csv' DELIMITER ',' CSV HEADER;
COPY dim_tempo TO 'database/csv/DIM_tempo.csv' DELIMITER ',' CSV HEADER;
COPY dim_circuito TO 'database/csv/DIM_circuito.csv' DELIMITER ',' CSV HEADER;
COPY fato_corrida TO 'database/csv/FATO_corrida.csv' DELIMITER ',' CSV HEADER;