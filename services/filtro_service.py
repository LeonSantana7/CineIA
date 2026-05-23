import random

MAX = 5


def filtrar_por_humor(filmes, humor):
    humor = humor.lower()

    if humor == "relaxado":
        # Quer algo tranquilo e de qualidade, sem muita intensidade
        resultado = [f for f in filmes if f["nota"] >= 6.5]
        return sorted(resultado or filmes, key=lambda f: f["nota"], reverse=True)[:MAX]

    if humor == "empolgado":
        # Quer o melhor do gênero, filmes intensos e bem avaliados
        resultado = [f for f in filmes if f["nota"] >= 7.0]
        return sorted(resultado or filmes, key=lambda f: f["nota"], reverse=True)[:MAX]

    if humor == "triste":
        # Quer algo que ressoe emocionalmente — os mais bem avaliados do gênero
        return sorted(filmes, key=lambda f: f["nota"], reverse=True)[:MAX]

    if humor == "estressado":
        # Quer escapar da realidade sem esforço — seleção aleatória entre os bem avaliados
        pool = [f for f in filmes if f["nota"] >= 6.0] or filmes
        return random.sample(pool, min(MAX, len(pool)))

    if humor == "romântico":
        # Quer algo bonito e com boa história — prioriza nota e lançamentos mais recentes
        resultado = [f for f in filmes if f["nota"] >= 6.0]
        base = resultado or filmes
        return sorted(base, key=lambda f: (f["nota"], f["ano"]), reverse=True)[:MAX]

    if humor == "entediado":
        # Quer ser surpreendido — seleção aleatória sem filtro de nota
        return random.sample(filmes, min(MAX, len(filmes)))

    if humor == "reflexivo":
        # Quer algo profundo e significativo — exige nota mais alta
        resultado = [f for f in filmes if f["nota"] >= 7.5]
        return sorted(resultado or filmes, key=lambda f: f["nota"], reverse=True)[:MAX]

    if humor == "feliz":
        # Quer algo leve e divertido para aproveitar o bom humor
        resultado = [f for f in filmes if f["nota"] >= 6.5]
        return (resultado or filmes)[:MAX]

    return filmes[:MAX]
