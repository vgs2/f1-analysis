DROP TABLE IF EXISTS FATO_CORRIDA;

-- DIMENSÃO DO PILOTO


CREATE TABLE dim_piloto (
    id_piloto INT PRIMARY KEY,
    nome_piloto VARCHAR(255),
    ano_nasc_piloto INT,
    nacionalidade_piloto VARCHAR(255)
    
);
-- DIMENSÃO DO CONSTRUTOR
CREATE TABLE dim_construtor(
    id_construtor INT PRIMARY KEY,
    nome_construtor VARCHAR(255),
    nacionalidade_construtor VARCHAR(255)
);
-- DIMENSÃO DO TEMPO
CREATE TABLE dim_tempo(
    dataa date PRIMARY KEY,
    dia INT,
    mes INT,
    ano INT
);
--  DIMENSÃO DOS CIRCUITOS
CREATE TABLE dim_circuito(
    id_circuito INT PRIMARY KEY,
    nome_circuito VARCHAR(255),
    pais_circuito VARCHAR(255),
    latitude FLOAT,
    longitude FLOAT,
    altitude FLOAT

);

CREATE TABLE fato_corrida(
    id_resultado INT PRIMARY KEY,
    id_piloto INT,
    id_construtor INT,
    id_tempo INT,
    id_circuito INT,
    posicao_qualify INT,
    posicao_corrida INT,
    pontos FLOAT, 
    numero_voltas INT,
    volta_mais_rapida INT,
    maior_velocidade FLOAT,
    tempo_corrida DATE,
    quantidade_pits INT,
    soma_tempo_pits FLOAT,
    CONSTRAINT FK_PILOTO FOREIGN KEY (id_piloto) REFERENCES dim_piloto(id_piloto),
    CONSTRAINT FK_CONSTRUTOR FOREIGN KEY (id_construtor) REFERENCES dim_construtor(id_construtor),
    CONSTRAINT FK_TEMPO FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    CONSTRAINT FK_CIRCUITO FOREIGN KEY (id_circuito) REFERENCES dim_circuito(id_circuito)
    
);
