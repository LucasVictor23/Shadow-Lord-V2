import sqlite3
import os

# Define o caminho do banco de dados na estrutura da nuvem
DB_NAME = "database/nexus_v2.db"

def conectar_nexus():
    """Estabelece conexão com o banco de dados SQLite"""
    # Garante que a pasta database exista para não dar erro de caminho
    if not os.path.exists('database'):
        os.makedirs('database')
    return sqlite3.connect(DB_NAME)

def buscar_personagem(nome):
    """Busca os dados de um herói pelo nome no banco local"""
    conn = conectar_nexus()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM herois WHERE nome LIKE ?", (f"%{nome}%",))
        resultado = cursor.fetchone()
    except sqlite3.OperationalError:
        resultado = None
    finally:
        conn.close()
    return resultado

def salvar_heroi(dados):
    """Insere ou atualiza um herói no banco de dados"""
    conn = conectar_nexus()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO herois (nome, classe, pv, pc, pl, imagem)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (dados['nome'], dados['classe'], dados['pv'], dados['pc'], dados['pl'], dados['imagem']))
    conn.commit()
    conn.close()
    return True
