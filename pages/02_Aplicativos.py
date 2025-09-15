# pages/02_Aplicativos.py - Portal de Aplicativos Corrigido
import streamlit as st
import time

# --- Configuração Inicial da Página ---
st.set_page_config(page_title="Portal de Análises", layout="wide", initial_sidebar_state="collapsed")

# --- Estilo Visual (CSS) ---
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

/* Estado de carregamento */
.loading-spinner {
    display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%; border-top-color: #667eea; animation: spin 1s ease-in-out infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Botões melhorados */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border: none; border-radius: 12px; padding: 12px 24px;
    font-weight: 600; text-decoration: none; display: inline-block;
    transition: all 0.2s; text-align: center; width: 100%;
}
.btn-primary:hover {
    transform: translateY(-2px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    color: white; text-decoration: none;
}

.btn-secondary {
    background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.3);
    border-radius: 12px; padding: 12px 24px; font-weight: 600; text-decoration: none;
    display: inline-block; transition: all 0.2s; text-align: center; width: 100%;
    margin-top: 0.5rem;
}
.btn-secondary:hover {
    background: rgba(255,255,255,0.15); transform: translateY(-1px);
    color: white; text-decoration: none;
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
        "emoji": "🔶", "url": "https://apphistogramspy-b3kfy7atbdhgxx8udeduma.streamlit.app/", "accent": "linear-gradient(180deg, #ec4899, #db2777)",
    },
    {
        "name": "Column 3D Line", "desc": "Visualização de dados em 3D com projeções e rotação interativa.",
        "emoji": "🌍", "url": "https://column3dpyline2inmoduleimportdash-kdqhfwwyyhdtb48x4z3kkn.streamlit.app/", "accent": "linear-gradient(180deg, #06b6d4, #0891b2)",
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

# --- Funções de Utilidade ---
def debug_auth_state():
    """Função para debug do estado de autenticação."""
    debug_info = {
        "hasattr_st_context": hasattr(st, 'context'),
        "hasattr_st_user": hasattr(st, 'user'),
        "session_state_keys": list(st.session_state.keys()),
    }
    
    # Verifica st.context.user
    if hasattr(st, 'context') and hasattr(st.context, 'user'):
        try:
            user = st.context.user
            debug_info["context_user_type"] = type(user).__name__
            debug_info["context_user_bool"] = bool(user)
            if user:
                debug_info["context_user_attributes"] = [attr for attr in dir(user) if not attr.startswith('_')]
        except Exception as e:
            debug_info["context_user_error"] = str(e)
    
    # Verifica st.user
    if hasattr(st, 'user'):
        try:
            user = st.user
            debug_info["st_user_type"] = type(user).__name__
            debug_info["st_user_bool"] = bool(user)
            if user:
                debug_info["st_user_attributes"] = [attr for attr in dir(user) if not attr.startswith('_')]
        except Exception as e:
            debug_info["st_user_error"] = str(e)
    
    return debug_info

def get_user_email() -> str:
    """Obtém o email do usuário logado com debug melhorado."""
    try:
        # Método moderno (st.context.user)
        if hasattr(st, 'context') and hasattr(st.context, 'user') and st.context.user:
            user = st.context.user
            for key in ("email", "primaryEmail", "preferred_username"):
                if hasattr(user, key):
                    email = getattr(user, key)
                    if email:
                        return str(email)
                elif isinstance(user, dict) and key in user:
                    email = user[key]
                    if email:
                        return str(email)
        
        # Método legado (st.user)
        if hasattr(st, 'user') and st.user:
            if hasattr(st.user, 'email') and st.user.email:
                return str(st.user.email)
            elif hasattr(st.user, 'primaryEmail') and st.user.primaryEmail:
                return str(st.user.primaryEmail)
        
        # Fallback para session_state
        for key in ("user_email", "email", "oidc_email"):
            if key in st.session_state and st.session_state[key]:
                return str(st.session_state[key])
                
    except Exception:
        pass
    
    return ""

def is_authenticated() -> bool:
    """Verifica se o usuário está autenticado com verificação mais robusta."""
    try:
        # Verifica st.context.user primeiro
        if hasattr(st, 'context') and hasattr(st.context, 'user') and st.context.user:
            return True
        
        # Verifica st.user (método legado)
        if hasattr(st, 'user') and st.user:
            # Alguns campos indicam autenticação
            if hasattr(st.user, 'is_logged_in'):
                return getattr(st.user, 'is_logged_in', False)
            if hasattr(st.user, 'email') and st.user.email:
                return True
        
        # Verifica session_state
        for key in ("authenticated", "user_email", "email", "oidc_email"):
            if key in st.session_state and st.session_state[key]:
                return True
                
    except Exception:
        pass
    
    return False

def is_allowed(email: str) -> bool:
    """Verifica se um e-mail está na lista de permissões dos secrets."""
    if not email:
        return False
        
    try:
        auth_config = st.secrets.get("auth", {})
        allowed_emails = set(str(e).strip().lower() for e in auth_config.get("allowed_emails", []))
        allowed_domains = set(str(d).strip().lower() for d in auth_config.get("allowed_domains", []))
        
        # Se não há lista de permissões, permite todos os usuários autenticados
        if not allowed_emails and not allowed_domains:
            return True
            
        email = email.strip().lower()
        domain = email.split("@")[-1] if "@" in email else ""
        
        return email in allowed_emails or domain in allowed_domains
    except Exception:
        # Em caso de erro, permite o acesso (fallback seguro para desenvolvimento)
        return True

def render_debug_page():
    """Renderiza uma página de debug para entender o estado de autenticação."""
    st.markdown('''
        <div class="login-container">
            <div class="login-box">
                <h1>🔍 Portal de Análises - Debug</h1>
                <p style="color: #666; margin-bottom: 2rem;">Analisando estado de autenticação...</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Informações de debug
    debug_info = debug_auth_state()
    
    st.subheader("🛠️ Debug da Autenticação")
    st.json(debug_info)
    
    # Estado de autenticação
    is_auth = is_authenticated()
    user_email = get_user_email()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Autenticado", "✅ Sim" if is_auth else "❌ Não")
    with col2:
        st.metric("Email", user_email or "Não encontrado")
    
    # Informações dos secrets
    st.subheader("🔐 Configuração de Autenticação")
    try:
        auth_config = st.secrets.get("auth", {})
        allowed_emails = auth_config.get("allowed_emails", [])
        allowed_domains = auth_config.get("allowed_domains", [])
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Emails permitidos:**")
            if allowed_emails:
                for email in allowed_emails:
                    st.write(f"- {email}")
            else:
                st.write("Nenhum configurado")
        
        with col2:
            st.write("**Domínios permitidos:**")
            if allowed_domains:
                for domain in allowed_domains:
                    st.write(f"- {domain}")
            else:
                st.write("Nenhum configurado")
    except Exception as e:
        st.error(f"Erro ao ler configuração: {e}")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Recarregar Página", type="primary", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("🚀 Tentar Acessar Portal", use_container_width=True):
            st.session_state["force_access"] = True
            st.rerun()

def render_login_page():
    """Renderiza a página de login sem redirecionamento automático."""
    st.markdown('''
        <div class="login-container">
            <div class="login-box">
                <h1>🚀 Portal de Análises</h1>
                <p style="color: #666; margin-bottom: 2rem;">Você precisa fazer login para acessar seus aplicativos</p>
                
                <div style="background: rgba(255,193,7,0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 1.5rem;">
                    <p style="color: #856404; margin: 0;">
                        <strong>🔒 Como fazer login:</strong><br>
                        • Acesse a página principal do portal<br>
                        • Faça login com sua conta Google<br>
                        • Retorne a esta página
                    </p>
                </div>
                
                <div style="background: rgba(23,162,184,0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #17a2b8;">
                    <p style="color: #0c5460; margin: 0;">
                        <strong>💡 Dica:</strong><br>
                        Se você já fez login e ainda está vendo esta página, tente recarregar ou ativar o modo debug abaixo.
                    </p>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Botões de ação sem redirecionamento automático
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <a href="https://f4iu25yf4y6qdhjisk6bqy.streamlit.app" target="_blank" class="btn-primary" style="margin-bottom: 0.5rem;">
           🔐 Abrir Página de Login (Nova Aba)
        </a>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Recarregar Esta Página", use_container_width=True):
            st.rerun()
        
        if st.button("🛠️ Modo Debug", use_container_width=True):
            st.session_state["debug_mode"] = True
            st.rerun()

def render_portal():
    """Mostra o portal principal com os aplicativos."""
    user_email = get_user_email()
    
    st.markdown(f'''
        <div class="nav">
            <span class="brand">
                <span>🚀</span>
                <span>Portal de Análises</span>
            </span>
            <span style="text-align: right;">
                <small>Logado como:</small><br>
                <strong>{user_email or "Usuário"}</strong>
            </span>
        </div>
    ''', unsafe_allow_html=True)

    # Sidebar com informações do usuário
    with st.sidebar:
        st.write(f"**Usuário:** {user_email or 'Não identificado'}")
        st.write(f"**Autenticado:** {'✅' if is_authenticated() else '❌'}")
        
        if st.button("🛠️ Debug", use_container_width=True):
            st.session_state["debug_mode"] = True
            st.rerun()
        
        if st.button("🚪 Sair", use_container_width=True):
            # Limpa apenas as chaves relacionadas à autenticação
            keys_to_clear = ["force_access", "debug_mode", "user_email", "email", "authenticated"]
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.success("Logout realizado com sucesso!")
            time.sleep(1)
            st.rerun()

    st.markdown("### Seus aplicativos")
    st.markdown('<p class="subtitle">Acesse as ferramentas de análise de forma rápida e organizada</p>', unsafe_allow_html=True)
    
    # Campo de busca
    search_query = st.text_input("Buscar", placeholder="🔍 Buscar aplicativos...", label_visibility="collapsed")
    
    # Filtrar aplicativos baseado na busca
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

# --- Lógica Principal ---
def main():
    """Função principal da página de aplicativos."""
    try:
        # Modo debug
        if st.session_state.get("debug_mode", False):
            render_debug_page()
            return
        
        # Acesso forçado (para debug)
        force_access = st.session_state.get("force_access", False)
        
        # Verifica se o usuário está autenticado
        if not force_access and not is_authenticated():
            render_login_page()
            return
        
        # Obtém o email do usuário
        user_email = get_user_email()
        
        # Verifica permissões (exceto em modo de acesso forçado)
        if not force_access and user_email and not is_allowed(user_email):
            st.error("🚫 **Acesso Negado**")
            st.warning(f"O e-mail **{user_email}** não tem permissão para acessar este portal.")
            st.info("💡 Entre em contato com o administrador para solicitar acesso.")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 Tentar Novamente", type="primary", use_container_width=True):
                    st.rerun()
                
                if st.button("🛠️ Modo Debug", use_container_width=True):
                    st.session_state["debug_mode"] = True
                    st.rerun()
            return
        
        # Usuário autorizado - mostra o portal
        render_portal()
        
    except Exception as e:
        st.error("⚠️ **Erro inesperado na aplicação**")
        st.exception(e)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Tentar Novamente", type="primary", use_container_width=True):
                st.rerun()
            
            if st.button("🛠️ Modo Debug", use_container_width=True):
                st.session_state["debug_mode"] = True
                st.rerun()

# Executa a função principal
if __name__ == "__main__":
    main()
