import streamlit as st
import time
from services.tmdb_service import buscar_filmes
from services.n8n_service import enviar_para_n8n
from utils.arquivo_utils import salvar_busca, ler_historico  # noqa: F401

st.set_page_config(page_title="CineIA", page_icon="🎬", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] {
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
    transition: all 0.3s ease;
}

.stButton > button:hover { background: #ff1a1a; transform: scale(1.05); }

.filme-card {
    background: #141414;
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 1rem;
    border-left: 3px solid #e50914;
    transition: all 0.3s ease;
}

.filme-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(229, 9, 20, 0.3);
}

.filme-titulo { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 1px; color: #fff; }
.filme-meta { color: #e50914; font-size: 0.8rem; font-weight: 500; margin-bottom: 0.4rem; }
.filme-sinopse { color: #888; font-size: 0.82rem; line-height: 1.5; }

/* Animação de Roleta */
@keyframes carousel-spin {
    0% { transform: translateX(0); opacity: 0.7; }
    50% { opacity: 1; }
    100% { transform: translateX(100vw); opacity: 0.3; }
}

@keyframes spin-wheel {
    0% { transform: rotateY(0deg) scale(1); }
    25% { transform: rotateY(90deg) scale(0.95); }
    50% { transform: rotateY(180deg) scale(1); }
    75% { transform: rotateY(270deg) scale(0.95); }
    100% { transform: rotateY(360deg) scale(1); }
}

@keyframes carousel-rotate {
    0% { transform: translateX(0px); }
    100% { transform: translateX(-1000px); }
}

@keyframes pulse-glow {
    0% { box-shadow: 0 0 10px rgba(229, 9, 20, 0.3); }
    50% { box-shadow: 0 0 30px rgba(229, 9, 20, 0.8); }
    100% { box-shadow: 0 0 10px rgba(229, 9, 20, 0.3); }
}

.filme-carrossel {
    animation: spin-wheel 0.8s infinite cubic-bezier(0.68, -0.55, 0.265, 1.55);
    transform-style: preserve-3d;
    perspective: 1000px;
}

.carousel-container {
    perspective: 1000px;
    height: 450px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(229, 9, 20, 0.15), rgba(20, 20, 20, 0.9));
    border-radius: 12px;
    border: 2px solid #e50914;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: inset 0 0 30px rgba(229, 9, 20, 0.1);
}

.carousel-wrapper {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.carousel-item {
    position: absolute;
    width: 150px;
    height: 240px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    transform-origin: center;
    animation: pulse-glow 2s infinite;
}

.carousel-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}

/* Filme Principal Destacado */
.filme-principal {
    background: linear-gradient(135deg, #1a0a0a, #2a1515);
    border: 2px solid #e50914;
    border-radius: 12px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 20px 60px rgba(229, 9, 20, 0.3);
    animation: slideInCenter 0.8s ease-out;
}

@keyframes slideInCenter {
    0% {
        opacity: 0;
        transform: scale(0.9);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

.filme-principal img {
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(229, 9, 20, 0.4);
    transition: transform 0.3s ease;
}

.filme-principal img:hover {
    transform: scale(1.05);
}

.filme-info-principal {
    color: #fff;
    margin-top: 1.5rem;
}

.titulo-principal {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    letter-spacing: 2px;
    color: #e50914;
    margin-bottom: 0.5rem;
}

.meta-principal {
    color: #aaa;
    font-size: 1rem;
    margin-bottom: 1rem;
    letter-spacing: 1px;
}

.sinopse-principal {
    color: #ddd;
    font-size: 1rem;
    line-height: 1.8;
    margin-bottom: 1.5rem;
}

.ia-box {
    background: linear-gradient(135deg, #1a0a0a 0%, #2a1515 100%);
    border: 2px solid #e50914;
    border-radius: 10px;
    padding: 2rem;
    margin: 2rem 0;
    font-size: 1rem;
    color: #fff;
    letter-spacing: 0.3px;
    box-shadow: 0 15px 50px rgba(229, 9, 20, 0.25);
    animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.loading-text {
    color: #e50914;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 2px;
    animation: blink 1.5s infinite;
}

@keyframes blink {
    0%, 50%, 100% { opacity: 1; }
    25%, 75% { opacity: 0.5; }
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
    # Buscar filmes
    with st.spinner("⏳ Buscando filmes inspiradores..."):
        filmes = buscar_filmes(genero.lower())

    if filmes:
        st.markdown(
            f"<p style='color:#555; font-size:0.75rem; letter-spacing:2px; margin-top:1rem;'>RESULTADOS PARA {genero.upper()} • {len(filmes)} FILMES</p>",
            unsafe_allow_html=True,
        )

        # Efeito de Roleta Girante enquanto aguarda a IA
        carousel_placeholder = st.empty()
        
        # Criar HTML com roleta girante
        carousel_html = "<div class='carousel-container'><div class='carousel-wrapper'>"
        
        # Posicionar filmes em círculo
        num_films = min(5, len(filmes))
        for i in range(num_films):
            angle = (i / num_films) * 360
            poster = filmes[i].get("poster", "")
            if poster:
                carousel_html += f"<div class='carousel-item' style='animation: spin-wheel 0.8s infinite; animation-delay: {i * 0.1}s; transform: rotate({angle}deg) translateX(120px) rotate(-{angle}deg);'><img src='{poster}' style='width:100%; height:100%; object-fit:cover;' /></div>"
        
        carousel_html += "<div style='text-align: center; z-index: 10;'><div class='loading-text'>🎬 ANALISANDO 🎬</div></div></div></div>"
        
        carousel_placeholder.markdown(carousel_html, unsafe_allow_html=True)

        # Consultar IA
        with st.spinner("🤖 IA analisando suas preferências..."):
            resposta = enviar_para_n8n(genero, humor, filmes)

        recomendacao = resposta.get("recomendacao", "Sem resposta.")
        filme_selecionado_idx = resposta.get("filme_index", 0)
        filme_nome_recomendado = resposta.get("filme_nome", "")
        
        # Validação extra: garantir índice válido
        try:
            filme_selecionado_idx = int(filme_selecionado_idx)
        except (ValueError, TypeError):
            filme_selecionado_idx = 0
        
        if filme_selecionado_idx < 0 or filme_selecionado_idx >= len(filmes):
            filme_selecionado_idx = 0
        
        filme_principal = filmes[filme_selecionado_idx]
        salvar_busca(genero, humor, recomendacao)

        # Limpar placeholder e mostrar resultado final
        carousel_placeholder.empty()

        # Exibir filme principal em destaque
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
        col_img, col_info = st.columns([0.9, 1.1])
        
        with col_img:
            if filme_principal.get("poster"):
                st.markdown(
                    f"<div style='text-align:center;'><img src='{filme_principal['poster']}' style='width:100%; max-width:280px; border-radius:12px; box-shadow: 0 10px 40px rgba(229, 9, 20, 0.4);'></div>",
                    unsafe_allow_html=True,
                )
        
        with col_info:
            st.markdown(
                f"""
                <div style='padding: 1.5rem;'>
                    <h2 style='color: #e50914; font-family: Bebas Neue; font-size: 2.2rem; letter-spacing: 2px; margin: 0 0 0.5rem 0;'>{filme_principal['titulo']}</h2>
                    <p style='color: #aaa; font-size: 1rem; margin: 0 0 1rem 0; letter-spacing: 1px;'>⭐ {filme_principal['nota']} | 📅 {filme_principal['ano']}</p>
                    <p style='color: #ddd; font-size: 0.95rem; line-height: 1.8; margin-bottom: 1.5rem;'>{filme_principal['sinopse']}</p>
                    <p style='color: #e50914; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; font-weight: 600;'>✨ 🎯 Escolha Inteligente da IA 🎯 ✨</p>
                    <p style='color: #666; font-size: 0.75rem; margin-top: 1rem;'>IA selecionou: {filme_nome_recomendado if filme_nome_recomendado else 'Automático'}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)

        # Exibir recomendação com destaque
        


        st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)

        # Exibir galeria de filmes com scroll
        st.markdown(
            "<p style='color:#666; font-size:0.75rem; letter-spacing:2px;'>GALERIA COMPLETA DE FILMES</p>",
            unsafe_allow_html=True,
        )
        
        cols = st.columns(5)
        for i, f in enumerate(filmes):
            with cols[i % 5]:
                if f["poster"]:
                    st.image(f["poster"], use_container_width=True)
                st.markdown(
                    f"""
                    <div style='background: #141414; border-left: 3px solid #e50914; padding: 0.8rem; border-radius: 4px; margin-top: 0.5rem;'>
                        <div style='font-family: Bebas Neue; font-size: 0.9rem; letter-spacing: 1px; color: #fff; margin-bottom: 0.3rem;'>{f["titulo"]}</div>
                        <div style='color: #e50914; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.4rem;'>⭐ {f["nota"]} &nbsp;|&nbsp; {f["ano"]}</div>
                        <div style='color: #888; font-size: 0.8rem; line-height: 1.4;'>{f["sinopse"][:80]}...</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:
        st.error("❌ Nenhum filme encontrado. Tente outro gênero!")

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
