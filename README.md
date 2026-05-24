# CineIA

Recomendador inteligente de filmes que combina a API do TMDB com IA via n8n para sugerir filmes com base no gênero e no humor do usuário. Disponível em interface web (Streamlit) e linha de comando (CLI).

## Como funciona

1. O usuário escolhe um **gênero** e como está se sentindo (**humor**)
2. A aplicação busca filmes na API do TMDB filtrados pelo gênero
3. A lista de filmes é enviada para um webhook no n8n, onde a IA considera o humor e retorna uma recomendação personalizada
4. A recomendação e a busca são salvas no histórico local (`data/historico.json`)

## Pré-requisitos

- Python 3.11+
- Conta no [TMDB](https://www.themoviedb.org/) para obter a API Key
- Webhook no [n8n](https://n8n.io/) configurado para receber o payload e retornar a recomendação da IA

## Instalação

```bash
git clone https://github.com/LeonSantana7/CineIA.git
cd CineIA
pip install -r requirements.txt
```

## Configuração

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
TMDB_API_KEY=sua_chave_aqui
N8N_WEBHOOK_URL=https://seu-usuario.app.n8n.cloud/webhook/seu-id
```

### Obtendo a TMDB API Key

1. Crie uma conta em [themoviedb.org](https://www.themoviedb.org/)
2. Acesse **Configurações → API**
3. Solicite uma chave de API (tipo "Developer")
4. Copie o valor de **API Key (v3 auth)**

### Configurando o Webhook no n8n

O n8n precisa receber um POST com o seguinte payload:

```json
{
  "genero": "ação",
  "humor": "empolgado",
  "filmes": [
    {
      "titulo": "Nome do Filme",
      "nota": 7.8,
      "ano": "2023",
      "sinopse": "...",
      "poster": "https://..."
    }
  ]
}
```

E retornar:

```json
{
  "recomendacao": "Texto com a recomendação da IA"
}
```

## Executando

### Interface Web (Streamlit) — recomendado

```bash
streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

### Terminal (CLI)

```bash
python main.py
```

### Docker

```bash
docker-compose up --build
```

Acesse `http://localhost:8501` no navegador.

## Funcionalidades

### Recomendação de filmes

Selecione um gênero e como você está se sentindo. O sistema busca filmes no TMDB, filtra conforme o humor e envia para a IA no n8n gerar uma recomendação personalizada.

### Histórico de buscas

Todas as recomendações são salvas automaticamente em `data/historico.json`. Na interface web, o histórico aparece na parte inferior da página. No CLI, escolha a opção **2** no menu.

### Exportar histórico em `.txt`

Disponível no CLI pela opção **3** do menu. Gera o arquivo `data/historico.txt` com todas as buscas formatadas de forma legível.


## Gêneros disponíveis

`Ação` · `Comédia` · `Terror` · `Romance` · `Aventura` · `Sci-Fi` · `Animação` · `Documentário` · `Fantasia`

## Humores disponíveis

`Relaxado` · `Empolgado` · `Feliz` · `Triste` · `Estressado` · `Romântico` · `Entediado` · `Reflexivo`

O humor é enviado para a IA no n8n, que considera o estado emocional do usuário para personalizar a recomendação.

## Estrutura do projeto

```
CineIA/
├── app.py                   # Interface web (Streamlit)
├── main.py                  # Interface CLI
├── services/
│   ├── tmdb_service.py      # Busca filmes na API do TMDB
│   └── n8n_service.py       # Envia dados ao webhook n8n e recebe recomendação
├── utils/
│   └── arquivo_utils.py     # Leitura, gravação e exportação do histórico
├── data/
│   ├── historico.json       # Histórico de buscas (gerado automaticamente)
│   └── historico.txt        # Exportação do histórico (gerado sob demanda)
├── .env.example             # Modelo de variáveis de ambiente
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
