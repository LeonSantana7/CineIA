import streamlit as st
from services.tmdb_service import buscar_filmes
from services.n8n_service import enviar_para_n8n
from services.filtro_service import filtrar_por_humor
from utils.arquivo_utils import salvar_busca, ler_historico  # noqa: F401

st.set_page_config(page_title="CineIA", page_icon="🎬", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {5
    background-color: #0a0a0a;
    color: #f0f0f0;
    font-family: 'Inter', sans-serif;
}

h1 { font-family: 'Bebas Neue', sans-serif; font-size: 3.5rem; letter-spacing: 4px; color: #e50914; margin-bottom: 0; }

.stSelectbox label { color: #aaa; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; }

.stButton > button {
    background: #e50914;
    color: white;
    border: none;
    padding: 0.6rem 2.5rem;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 2px;
    border-radius: 2px;
    cursor: pointer;
    width: 100%;
}

.stButton > button:hover { background: #ff1a1a; }

.filme-card {
    background: #141414;
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 3px solid #e50914;
}

.filme-titulo { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 1px; color: #fff; }
.filme-meta { color: #e50914; font-size: 0.8rem; font-weight: 500; margin-bottom: 0.4rem; }
.filme-sinopse { color: #888; font-size: 0.82rem; line-height: 1.5; }

.ia-box {
    background: linear-gradient(135deg, #1a0a0a, #1a1a1a);
    border: 1px solid #e50914;
    border-radius: 6px;
    padding: 1.2rem 1.5rem;
    margin-top: 1.5rem;
    font-size: 1rem;
    color: #fff;
    letter-spacing: 0.3px;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown("<h1>🎬 CineIA</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#666; letter-spacing:2px; font-size:0.8rem; margin-top:-10px;'>RECOMENDAÇÃO INTELIGENTE DE FILMES</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

col_a, col_b, col_c = st.columns([2, 2, 1])
with col_a:
    genero = st.selectbox(
        "GÊNERO",
        [
            "Ação",
            "Comédia",
            "Terror",
            "Romance",
            "Aventura",
            "Sci-Fi",
            "Animação",
            "Documentário",
            "Fantasia",
        ],
    )
with col_b:
    humor = st.selectbox(
        "COMO VOCÊ ESTÁ?",
        [
            "Relaxado",
            "Empolgado",
            "Feliz",
            "Triste",
            "Estressado",
            "Romântico",
            "Entediado",
            "Reflexivo",
        ],
    )
with col_c:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    recomendar = st.button("BUSCAR")

if recomendar:
    with st.spinner("Buscando filmes..."):
        filmes = buscar_filmes(genero.lower())
        filmes = filtrar_por_humor(filmes, humor)

    if filmes:
        st.markdown(
            f"<p style='color:#555; font-size:0.75rem; letter-spacing:2px; margin-top:1rem;'>RESULTADOS PARA {genero.upper()} • {len(filmes)} FILMES</p>",
            unsafe_allow_html=True,
        )

        cols = st.columns(5)
        for i, f in enumerate(filmes):
            with cols[i % 5]:
                if f["poster"]:
                    st.image(f["poster"], use_container_width=True)
                st.markdown(
                    f"""
                <div class='filme-card'>
                    <div class='filme-titulo'>{f["titulo"]}</div>
                    <div class='filme-meta'>⭐ {f["nota"]} &nbsp;|&nbsp; {f["ano"]}</div>
                    <div class='filme-sinopse'>{f["sinopse"][:120]}...</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        with st.spinner("Consultando IA..."):
            resposta = enviar_para_n8n(genero, humor, filmes)

        recomendacao = resposta.get("recomendacao", "Sem resposta.")
        salvar_busca(genero, humor, recomendacao)

        st.markdown(
            f"""
        <div class='ia-box'>
             &nbsp;<strong>Recomendação da IA:</strong> {recomendacao}
        </div>
        """,
            unsafe_allow_html=True,
        )

    else:
        st.error("Nenhum filme encontrado.")

st.markdown("---")
st.markdown(
    "<p style='color:#555; font-size:0.75rem; letter-spacing:2px;'>HISTÓRICO DE BUSCAS</p>",
    unsafe_allow_html=True,
)

historico = ler_historico()
buscas = [h for h in historico if h.get("tipo") != "catalogo"]

if not buscas:
    st.markdown(
        "<p style='color:#444; font-size:0.85rem;'>Nenhuma busca registrada ainda.</p>",
        unsafe_allow_html=True,
    )
else:
    for h in reversed(buscas[-10:]):
        st.markdown(
            f"""
            <div style='background:#141414; border-left:3px solid #333; padding:0.6rem 1rem;
                        margin-bottom:0.5rem; border-radius:4px;'>
                <span style='color:#555; font-size:1.20rem;'>{h.get("data", "")}</span>
                &nbsp;&nbsp;
                <span style='color:#e50914; font-size:1.20rem; font-weight:500;'>
                    {h.get("genero", "").upper()} · {h.get("humor", "").upper()}
                </span>
                <div style='color:#888; font-size:1.20rem; margin-top:0.3rem;'>
                    {h.get("recomendacao", "")[:120]}…
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
