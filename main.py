import requests
import json

print("\n====== BEM VINDO AO CINEIA ======")
print("=== TEU RECOMENDADOR DE FILMES ===")


def exibir_menu():
    print("\nO que deseja fazer?")
    print("1. Receber recomendação")
    print("2. Ver histórico")
    print("3. Sair")

exibir_menu()
opcao = input("Digite o número da opção desejada: ")
if opcao == "1":
    genero = input("Digite o gênero do filme (ex: ação, comédia, drama): ")
    resposta = requests.get(f"http://localhost:5000/recomendar?genero={genero}")
    if resposta.status_code == 200:
        filme = resposta.json()
        print(f"\nRecomendação: {filme['titulo']} ({filme['ano']}) - {filme['genero']}")
    else:
        print("Erro ao obter recomendação.")
elif opcao == "2":
    resposta = requests.get("http://localhost:5000/historico")
    if resposta.status_code == 200:
        historico = resposta.json()
        print("\nHistórico de Recomendações:")
        for item in historico:
            print(f"- {item['titulo']} ({item['ano']}) - {item['genero']}")
    else:
        print("Erro ao obter histórico.")            
exibir_menu()
