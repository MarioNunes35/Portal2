# portal_final_v3.py
import streamlit as st

# --- Configuração Inicial da Página ---
st.set_page_config(page_title="Portal de Análises", layout="wide", initial_sidebar_state="collapsed")

# --- Estilo Visual (CSS do seu design) ---
PORTAL_STYLE_CSS = """
<style>
/* Fundo e Fonte Principal */
.stApp {
  background:
    radial-gradient(1200px 500px at 20% -10%, rgba(99,102,241,0.25), transparent 40%),
    radial-gradient(1000px 450px at 90% 10%, rgba(45,212,191,0.22), transparent 40%),
    linear-gradient(180deg, #121317 0%, #0f1116 100%) !important;
  color: #EAEAF1;
}

/* Header Fixo */
.nav { 
  position: sticky; top: 0; z-index: 20; padding: 14px 22px; margin: -1.2rem -1rem 1rem -1rem;
  backdrop-filter: blur(8px); background: rgba(255,255,255,0.06);
  border-bottom: 1px solid rgba(255,255,255,0.12); 
  display: flex; justify-content: space-between; align-items: center;
}
.brand { 
  font-weight: 700; font-size: 1.05rem; letter-spacing: .02em; 
  display: flex; align-items: center; gap: 12px;
}

/* Campo de Busca */
.stTextInput input {
  background: rgba(255,255,255,0.08) !important; 
  border: 1px solid rgba(255,255,255,0.20) !important;
  border-radius: 999px !important; 
  color: #fff !important;
  padding: 16px 20px !important;
  font-size: 16px !important;
  transition: all 0.2s;
}
.stTextInput input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* Cards dos Aplicativos */
.card{ 
  position: relative; overflow: hidden; padding: 28px 24px 22px 24px; border-radius: 20px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.18);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease; 
  margin-bottom: 28px; height: 320px; display: flex; flex-direction: column;
}
.card:hover{ 
  transform: translateY(-3px); 
  box-shadow: 0 16px 40px rgba(0,0,0,0.45); 
  border-color: rgba(255,255,255,0.28); 
}
.card .accent{ 
  position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
}
.icon{ 
  width: 72px; height: 72px; border-radius: 50%; display: flex; 
  align-items: center; justify-content: center;
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.20); 
  font-size: 32px; margin-bottom: 16px; 
}
.card h3{ 
  margin: 6px 0 8px 0; font-size: 1.25rem; color: #fff; font-weight: 600;
}
.card p{ 
  margin: 0 0 16px 0; color: #CBD5E1; line-height: 1.4; flex-grow: 1;
}
.actions .btn{ 
  padding: 12px 20px; border-radius: 12px; background: rgba(255,255,255,0.10);
  border: 1px solid rgba(255,255,255,0.22); color: #fff; text-decoration: none; 
  font-weight: 600; font-size: 14px;
  transition: all .15s ease; display: inline-block; text-align: center;
}
.actions .btn:hover{ 
  background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.32); transform: translateY(-1px); 
}

/* Títulos */
h1, h2, h3{ color: #fff; } 
.subtitle{ color: #CBD5E1; margin-top: -6px; }

/* Página de Login */
.login-container {
    display: flex; align-items: center; justify-content: center; min-height: 80vh;
}
.login-box {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.18);
    border-radius: 20px; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    backdrop-filter: blur(10px); width: min(450px, 90vw); text-align: center;
}
.login-box .stButton button {
    width: 100%; padding: 16px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border: none; border-radius: 12px; font-size: 16px;
    font-weight: 600; height: 56px; margin-top: 24px; transition: all 0.2s;
}
.login-box .stButton button:hover {
    transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
}
</style>
"""
st.markdown(PORTAL_STYLE_CSS, unsafe_allow_html=True)

# --- Lista de Aplicativos ---
APPS = [
    {
        "name": "TG/ADT Events", "desc": "Análise de eventos térmicos em TG/ADT com identificação automática de picos.",
        "emoji": "🔥", "url": "https://apptgadtgeventspy-hqeqt7yljzwra3r7nmdhju.streamlit.app/", "accent": "linear-gradient(180deg, #ef4444, #dc2626)",
    },
    {
        "name": "Stack Graph", "desc": "Criação de gráficos empilhados para visualização de dados multidimensionais.",
        "emoji": "📊", "url": "https://appstackgraphpy-ijew8pyut2jkc4x4pa7nbv.streamlit.app/", "accent": "linear-gradient(180deg, #3b82f6, #1d4ed8)",
    },
    {
        "name": "Rheology App", "desc": "Análise completa de dados de reologia com ajuste de modelos viscoelásticos.",
        "emoji": "🔄", "url": "https://apprheologyapppy-mbkr3wmbdb76t3ysvlfecr.streamlit.app/", "accent": "linear-gradient(180deg, #8b5cf6, #7c3aed)",
    },
    {
        "name": "Mechanical Properties", "desc": "Cálculo de propriedades mecânicas e análise de tensão-deformação.",
        "emoji": "⚙️", "url": "https://appmechanicalpropertiespy-79l8dejt9kfmmafantscut.streamlit.app/", "accent": "linear-gradient(180deg, #6b7280, #4b5563)",
    },
    {
        "name": "Baseline Smoothing", "desc": "Suavização de linha de base em gráficos com algoritmos avançados.",
        "emoji": "📈", "url": "https://appbaselinesmoothinglineplotpy-mvx5cnwr5szg4ghwpbx379.streamlit.app/", "accent": "linear-gradient(180deg, #10b981, #059669)",
    },
    {
        "name": "Isotherms App", "desc": "Análise de isotermas de adsorção com modelos de Langmuir e Freundlich.",
        "emoji": "🌡️", "url": "https://isothermsappfixedpy-ropmkqgbbxujhvkd6pfxgi.streamlit.app/", "accent": "linear-gradient(180deg, #f59e0b, #d97706)",
    },
    {
        "name": "Histograms", "desc": "Geração de histogramas customizados com análise estatística completa.",
        "emoji": "📶", "url": "https://apphistogramspy-b3kfy7atbdhgxx8udeduma.streamlit.app/", "accent": "linear-gradient(180deg, #ec4899, #db2777)",
    },
    {
        "name": "Column 3D Line", "desc": "Visualização de dados em 3D com projeções e rotação interativa.",
        "emoji": "🌐", "url": "https://column3dpyline2inmoduleimportdash-kdqhfwwyyhdtb48x4z3kkn.streamlit.app/", "accent": "linear-gradient(180deg, #06b6d4, #0891b2)",
    },
    {
        "name": "Crystallinity DSC/XRD", "desc": "Cálculo de cristalinidade por DSC e XRD com análise comparativa.",
        "emoji": "💎", "url": "https://appcrystallinitydscxrdpy-wqtymsdcco2nuem7fv3hve.streamlit.app/", "accent": "linear-gradient(180deg, #a855f7, #9333ea)",
    },
    {
        "name": "Column 3D", "desc": "Visualização de dados em colunas 3D com mapeamento de cores.",
        "emoji": "🏛️", "url": "https://column3dpy-cskafquxluvyv23hbnhxli.streamlit.app/", "accent": "linear-gradient(180deg, #84cc16, #65a30d)",
    },
    {
        "name": "Kinetic Models", "desc": "Ajuste de modelos cinéticos com otimização de parâmetros.",
        "emoji": "⚗️", "url": "https://kineticmodelsapppy-fz8qyt64fahje5acofqpcm.streamlit.app/", "accent": "linear-gradient(180deg, #f97316, #ea580c)",
    },
    {
        "name": "Python Launcher", "desc": "Executor de scripts Python online com ambiente isolado.",
        "emoji": "🐍", "url": "https://pythonlauncherfixedpy-yschqh6qwzl526xurdeoca.streamlit.app/", "accent": "linear-gradient(180deg, #facc15, #eab308)",
    },
]

# --- Funções de Permissão ---
def is_allowed(email: str) -> bool:
    """Verifica se um e-mail está na lista de permissões dos secrets."""
    auth_config = st.secrets.get("auth", {})
    allowed_emails = {str(e).strip().lower() for e in auth_config.get("allowed_emails", [])}
    if not allowed_emails:
        return True # Permite todos se a lista estiver vazia
    return email.strip().lower() in allowed_emails

# --- Funções de Interface ---
def render_portal():
    """Mostra o portal principal com os aplicativos."""
    st.markdown(f'''
        <div class="nav">
            <span class="brand">
                <span>🚀</span>
                <span>Portal de Análises</span>
            </span>
            <span style="text-align: right;">
                <small>Logado como:</small><br>
                <strong>{st.user.email}</strong>
            </span>
        </div>
    ''', unsafe_allow_html=True)

    with st.sidebar:
        st.write(f"Logado como: **{st.user.email}**")
        st.logout("Sair", use_container_width=True)

    st.markdown("### Seus aplicativos")
    st.markdown('<p class="subtitle">Acesse as ferramentas de análise de forma rápida e organizada</p>', unsafe_allow_html=True)
    search_query = st.text_input("Buscar", placeholder="🔍 Buscar aplicativos...", label_visibility="collapsed")
    
    query = search_query.lower().strip()
    filtered_apps = [app for app in APPS if query in app["name"].lower() or query in app["desc"].lower()]

    if filtered_apps:
        cols = st.columns(3)
        for i, app in enumerate(filtered_apps):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="card">
                    <div class="accent" style="background:{app['accent']};"></div>
                    <div class="icon">{app['emoji']}</div>
                    <h3>{app['name']}</h3>
                    <p>{app['desc']}</p>
                    <div class="actions">
                        <a class="btn" href="{app['url']}" target="_blank" rel="noopener noreferrer">Abrir aplicativo →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🔍 Nenhum aplicativo encontrado para o termo buscado.")

# --- Lógica Principal do Aplicativo ---
is_authenticated = getattr(st.user, "is_logged_in", False)

if not is_authenticated:
    render_login_page()
else:
    if is_allowed(st.user.email):
        render_portal()
    else:
        st.error(f"🚫 Acesso Negado. O e-mail **{st.user.email}** não tem permissão para acessar este portal.")
        st.warning("Por favor, contate o administrador para solicitar acesso.")
        if st.button("Sair"):
            st.logout()
            st.stop()
