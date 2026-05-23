import requests
import os
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def enviar_para_n8n(genero, humor, filmes):
    payload = {
        "genero": genero,
        "humor": humor,
        "filmes": filmes,
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
        response.raise_for_status()
        dados = response.json()
        return {"recomendacao": dados.get("recomendacao", "Sem resposta.")}
    except requests.RequestException as e:
        return {"recomendacao": f"Erro ao consultar IA: {e}"}
