create table construtor(
    id_construtor int PRIMARY KEY,
    ref_construtor varchar(20),
    nome_construtor varchar(30),
    nacionalidade varchar(20),
    url1 varchar(100)
);

create table fabricante(
    id_fabricante int primary key,
    nome_fabricante varchar(30)
);

create table piloto(
    id_piloto int primary key,
    nome_piloto varchar(30)
);

create table circuito(
    id_circuito int PRIMARY KEY,
    nome_circuito varchar(30)
);

create table colocacao(
    colocacao int PRIMARY KEY,
    pontuacao int,
    podio boolean
);

create table fabricante_construtor(
    id_fabricante int REFERENCES fabricante,
    id_construtor int REFERENCES construtor,
    temporada int,
    PRIMARY KEY (id_construtor, temporada)
);

CREATE TABLE construtor_piloto(
    id_piloto int REFERENCES piloto,
    id_construtor int REFERENCES construtor,
    temporada int,
    PRIMARY KEY (temporada, id_piloto, id_construtor)    
);

create table gp(
    id_gp int primary key,
    id_circuito int REFERENCES circuito,
    temporada int
);

CREATE TABLE classificatoria(
    id_piloto int REFERENCES piloto,
    id_gp int REFERENCES gp,
    posicao int,
    PRIMARY KEY (id_piloto, id_gp)
);


create table resultado(
    id_piloto int REFERENCES piloto,
    colocacao int REFERENCES colocacao,
    id_gp int REFERENCES gp,
    ponto_extra int,
    PRIMARY KEY (id_piloto, id_gp)
);