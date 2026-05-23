from services.tmdb_service import buscar_filmes
from services.filtro_service import filtrar_por_humor
from services.n8n_service import enviar_para_n8n
from utils.arquivo_utils import salvar_busca, ler_historico, exportar_historico_txt

GENEROS = [
    "ação",
    "comédia",
    "terror",
    "romance",
    "aventura",
    "sci-fi",
    "animação",
    "documentário",
    "fantasia",
]
HUMORES = [
    "relaxado",
    "empolgado",
    "feliz",
    "triste",
    "estressado",
    "romântico",
    "entediado",
    "reflexivo",
]


def exibir_menu():
    print("\n🎬 Bem-vindo ao CineIA!")
    print("=" * 40)


def pedir_genero():
    print(f"\nGêneros disponíveis: {', '.join(GENEROS)}")
    while True:
        genero = input("Digite o gênero: ").strip().lower()
        if genero in GENEROS:
            return genero
        print("Gênero inválido. Tente novamente.")


def pedir_humor():
    print(f"\nHumores disponíveis: {', '.join(HUMORES)}")
    while True:
        humor = input("Como você está? ").strip().lower()
        if humor in HUMORES:
            return humor
        print("Humor inválido. Tente novamente.")


def exibir_filmes(filmes):
    print("\nFilmes encontrados:")
    print("-" * 40)
    for i, f in enumerate(filmes, 1):
        print(f"{i}. {f['titulo']} ({f['ano']}) — ⭐ {f['nota']}")
        print(f"   {f['sinopse'][:100]}...")
        print()


def main():
    exibir_menu()

    while True:
        print("\nO que deseja fazer?")
        print("1. Receber recomendação")
        print("2. Ver histórico")
        print("3. Exportar histórico (.txt)")
        print("4. Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            genero = pedir_genero()
            humor = pedir_humor()

            print("\nBuscando filmes...")
            filmes = buscar_filmes(genero)
            filmes = filtrar_por_humor(filmes, humor)

            if not filmes:
                print("Nenhum filme encontrado. Tente novamente.")
                continue

            exibir_filmes(filmes)

            print("Consultando IA...")
            resposta = enviar_para_n8n(genero, humor, filmes)
            recomendacao = resposta.get("recomendacao", "Sem resposta.")
            salvar_busca(genero, humor, recomendacao)
            print(f"\nIA recomenda: {recomendacao}")

        elif opcao == "2":
            historico = ler_historico()
            if not historico:
                print("\nNenhuma busca no histórico ainda.")
            else:
                print("\nHistórico de buscas:")
                for h in historico[-5:]:
                    rec = h.get("recomendacao", "")[:60]
                    print(f"• {h['data']} — {h['genero']} | {h['humor']} → {rec}...")

        elif opcao == "3":
            caminho = exportar_historico_txt()
            if caminho:
                print(f"\nHistórico exportado para {caminho}")
            else:
                print("\nNenhuma busca no histórico para exportar.")

        elif opcao == "4":
            print("\n Até logo!")
            break

        else:
            print(" Opção inválida.")


if __name__ == "__main__":
    main()
