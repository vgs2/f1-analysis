-- Classificação do campeonado de pilotos
-- Classificação do campeonado de contrutores
-- Pilotos com mais pódios
-- Pilotos com mais poles (primeiro lugar no treino classificatório)

SELECT id_piloto, SUM(pontuacao + ponto_extra) FROM resultado
JOIN gp on resultado.id_gp = gp.id_gp
JOIN piloto on resultado.id_piloto = piloto.id_piloto
JOIN colocacao on resultado.colocacao = colocacao.colocacao
GROUP BY id_piloto, temporada