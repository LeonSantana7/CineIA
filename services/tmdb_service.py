import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_URL = "https://api.themoviedb.org/3/discover/movie"

GENEROS = {
    "ação": 28,
    "comédia": 35,
    "terror": 27,
    "romance": 10749,
    "aventura": 12,
    "sci-fi": 878,
    "animação": 16,
    "documentário": 99,
    "fantasia": 14,
}


HEADERS = {
    "User-Agent": "CineIA/1.0",
    "Accept": "application/json",
}


def buscar_filmes(genero, quantidade=10):
    genero_id = GENEROS.get(genero.lower())
    if not genero_id:
        return []

    pagina = random.randint(1, 10)

    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genero_id,
        "language": "pt-BR",
        "sort_by": "popularity.desc",
        "page": pagina,
    }

    for tentativa in range(3):
        try:
            response = requests.get(
                TMDB_URL, params=params, headers=HEADERS, timeout=15
            )
            response.raise_for_status()
            filmes = response.json().get("results", [])[:quantidade]
            break
        except requests.RequestException as e:
            if tentativa == 2:
                print(f"[TMDB] Falha após 3 tentativas: {e}")
                return []

    return [
        {
            "titulo": f.get("title", "Sem título"),
            "nota": f.get("vote_average", 0),
            "ano": (f.get("release_date") or "")[:4] or "N/A",
            "sinopse": f.get("overview") or "Sinopse não disponível.",
            "poster": f"https://image.tmdb.org/t/p/w300{f['poster_path']}"
            if f.get("poster_path")
            else None,
        }
        for f in filmes
    ]
