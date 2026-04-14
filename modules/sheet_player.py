import streamlit as st

def renderizar_hud(dados):
    st.markdown("""
        <style>
        .label-hp { color: #ff4b4b; font-weight: bold; }
        .label-pc { color: #00f2ff; font-weight: bold; }
        .label-pl { color: #8a2be2; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        if dados['imagem']: st.image(dados['imagem'], use_column_width=True)
        else: st.warning("Sem Imagem")
    with col2:
        st.markdown(f"### 🛡️ {dados['nome']}")
        st.write(f"**Classe:** {dados['classe']}")
        st.markdown(f"<span class='label-hp'>❤️ PV:</span> {dados['pv']}", unsafe_allow_html=True)
        st.markdown(f"<span class='label-pc'>🔷 PC:</span> {dados['pc']}", unsafe_allow_html=True)
        st.markdown(f"<span class='label-pl'>✨ PL:</span> {dados['pl']}", unsafe_allow_html=True)
