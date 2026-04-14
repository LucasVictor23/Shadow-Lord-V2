import streamlit as st
import os
import sqlite3
from modules.sheet_player import renderizar_hud

# No topo do arquivo, adicione:
from modules.dice_roller import rolar_dado_nexus

# No meio do arquivo, atualize a linha das abas:
tab1, tab2, tab3 = st.tabs(["📊 STATUS", "🛠️ TRANSMIGRAR", "🎲 DADOS"])

# No final do arquivo, adicione:
with tab3:
    rolar_dado_nexus()


# Caminho do Banco na Nuvem
DB_PATH = "database/nexus_v2.db"

def init_db():
    if not os.path.exists('database'): os.makedirs('database')
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS herois (nome TEXT, classe TEXT, pv TEXT, pc TEXT, pl TEXT, imagem BLOB)')
    conn.commit()
    return conn

st.set_page_config(page_title="NEXUS V2", layout="wide")
st.title("👁️ NEXUS OS | V2.0")

tab1, tab2 = st.tabs(["📊 STATUS", "🛠️ TRANSMIGRAR"])

with tab1:
    nome_busca = st.text_input("👤 Buscar Herói:", "Alberto")
    conn = init_db()
    h = conn.execute("SELECT * FROM herois WHERE nome=?", (nome_busca,)).fetchone()
    if h:
        dados_h = {'nome': h[0], 'classe': h[1], 'pv': h[2], 'pc': h[3], 'pl': h[4], 'imagem': h[5]}
        renderizar_hud(dados_h)
    else:
        st.warning("Aguardando transmigração de dados...")

with tab2:
    st.subheader("Nova Transmigração")
    with st.form("add"):
        n = st.text_input("Nome:")
        cl = st.selectbox("Hierarquia:", ["Humano", "Sombra", "Lord Shadow"])
        pv = st.text_input("PV (Ex: 20/20)")
        pc = st.text_input("PC (Ex: 11/11)")
        pl = st.text_input("PL (Ex: 1500)")
        img = st.file_uploader("🖼️ Foto")
        if st.form_submit_button("🔥 Gravar no Nexus"):
            img_data = img.getvalue() if img else None
            conn = init_db()
            conn.execute("INSERT INTO herois VALUES (?,?,?,?,?,?)", (n, cl, pv, pc, pl, img_data))
            conn.commit()
            st.success("Dados transmigrados!")
