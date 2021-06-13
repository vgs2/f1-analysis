-- Classificação do campeonado de pilotos
SELECT id_piloto, SUM(pontuacao + ponto_extra) as pontuacao_piloto_temporada FROM resultado
JOIN gp on resultado.id_gp = gp.id_gp
JOIN piloto on resultado.id_piloto = piloto.id_piloto
JOIN colocacao on resultado.colocacao = colocacao.colocacao
GROUP BY temporada, id_piloto
ORDER BY SUM(pontuacao + ponto_extra)

-- Classificação do campeonado de contrutores
SELECT id_construtor, SUM(pontuacao + ponto_extra) as pontuacao_construtor_temporada FROM resultado
JOIN gp on resultado.id_gp = gp.id_gp
JOIN piloto on resultado.id_piloto = piloto.id_piloto
JOIN colocacao on resultado.colocacao = colocacao.colocacao
JOIN construtor_piloto ON piloto.id_piloto = construtor_piloto.id_piloto 
                        AND construtor_piloto.temporada = gp.temporada
GROUP BY temporada, id_construtor
SUM(pontuacao + ponto_extra)

-- Pilotos com mais pódios
SELECT id_piloto, COUNT(podio) FROM resultado
JOIN colocacao ON resultado.colocacao = colocacao.colocacao
WHERE podio = TRUE
GROUP BY id_piloto 
ORDER BY COUNT(podio)

-- Pilotos com mais poles (primeiro lugar no treino classificatório)
SELECT id_piloto, COUNT(posicao) as n_de_poles FROM classificatoria
WHERE posicao = 1
GROUP BY id_piloto
ORDER BY COUNT(posicao) LIMIT 10