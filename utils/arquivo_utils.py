import json
import os
from datetime import datetime

HISTORICO_PATH = "data/historico.json"


def salvar_busca(genero, humor, recomendacao):
    historico = ler_historico()
    historico.append(
        {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "genero": genero,
            "humor": humor,
            "recomendacao": recomendacao,
        }
    )
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


def ler_historico():
    if not os.path.exists(HISTORICO_PATH):
        return []
    with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_historico(historico):
    os.makedirs(os.path.dirname(HISTORICO_PATH), exist_ok=True)
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)


def exportar_historico_txt(caminho="data/historico.txt"):
    historico = ler_historico()
    if not historico:
        return False

    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("HISTÓRICO DE RECOMENDAÇÕES — CineIA\n")
        f.write("=" * 40 + "\n\n")
        for h in historico:
            f.write(f"Data:        {h.get('data', '')}\n")
            f.write(f"Gênero:      {h.get('genero', '')}\n")
            f.write(f"Humor:       {h.get('humor', '')}\n")
            f.write(f"Recomendação:{h.get('recomendacao', '')}\n")
            f.write("-" * 40 + "\n")

    return caminho
