import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")


def extrair_nome_filme(texto):
    """Extrai nome de filme entre aspas duplas ou simples"""
    # Procura por padrões como: "Nome do Filme" ou 'Nome do Filme'
    match_duplas = re.search(r'"([^"]+)"', texto)
    match_simples = re.search(r"'([^']+)'", texto)
    
    if match_duplas:
        return match_duplas.group(1).strip()
    elif match_simples:
        return match_simples.group(1).strip()
    return None


def buscar_filme_por_nome(nome_filme, filmes):
    """Busca um filme na lista pelo nome com tolerância a variações"""
    if not nome_filme:
        return 0
    
    nome_lower = nome_filme.lower().strip()
    
    # Nível 1: Busca exata (case-insensitive)
    for i, f in enumerate(filmes):
        if f["titulo"].lower().strip() == nome_lower:
            return i
    
    # Nível 2: Busca parcial direta (contém o nome)
    for i, f in enumerate(filmes):
        titulo_lower = f["titulo"].lower().strip()
        if nome_lower in titulo_lower or titulo_lower in nome_lower:
            return i
    
    # Nível 3: Busca por palavras-chave principais
    palavras_chave = [p for p in nome_lower.split() if len(p) > 2]  # palavras com mais de 2 letras
    if palavras_chave:
        for i, f in enumerate(filmes):
            titulo_palavras = f["titulo"].lower().split()
            match_count = sum(1 for palavra in palavras_chave if any(palavra in tp for tp in titulo_palavras))
            if match_count >= len(palavras_chave) * 0.7:  # 70% de match
                return i
    
    # Nível 4: Busca fuzzy simples (primeira letra das palavras)
    palavras_nome = nome_lower.split()
    if palavras_nome:
        primeira_palavra = palavras_nome[0]
        for i, f in enumerate(filmes):
            if f["titulo"].lower().startswith(primeira_palavra):
                return i
    
    # Fallback: primeiro filme
    return 0


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
        recomendacao = dados.get("recomendacao", "Sem resposta.")
        
        # Extrair nome do filme do texto da recomendação (entre aspas)
        filme_nome = extrair_nome_filme(recomendacao)
        
        # Se não encontrou entre aspas, tentar obter do campo 'filme'
        if not filme_nome:
            filme_nome = dados.get("filme", None)
        
        # Buscar índice do filme com busca robusta
        filme_index = buscar_filme_por_nome(filme_nome, filmes)
        
        return {
            "recomendacao": recomendacao,
            "filme_index": filme_index,
            "filme_nome": filme_nome
        }
    except requests.RequestException as e:
        return {
            "recomendacao": f"Erro ao consultar IA: {e}",
            "filme_index": 0
        }
