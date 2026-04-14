#Implementar Console de Dados Nexus com Multi-Dados e Regras 3D&T
#Adição do sistema de rolagem para D4, D6, D8, D10, D12, D20 e D100. 
#Inclui lógica de 'Destino Selado' (+/- 7), cálculo automático de crítico para 3D&T (6 vira 12) 
#e correção de persistência na soma dos resultados.


import streamlit as st
import random
import time

def rolar_dado_nexus():
    st.subheader("🎲 Console de Dados Nexus")
    
    # Seleção do Arsenal
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        tipo_dado = st.selectbox("Escolha o Dado:", [4, 6, 8, 10, 12, 20, 100], format_func=lambda x: f"D{x}")
        qtd_dados = st.number_input("Quantidade:", min_value=1, max_value=10, value=1)
    
    with col_config2:
        modificador = st.select_slider("Ajuste de Rota:", options=list(range(-7, 8)), value=0)
        modo_combate = st.checkbox("Modo Combate (3D&T)", value=False) if tipo_dado == 6 else False

    # Lógica de Destino Selado
    if modificador >= 7:
        st.success("✨ **DESTINO SELADO: SUCESSO ABSOLUTO**")
        return
    elif modificador <= -7:
        st.error("💀 **DESTINO SELADO: FALHA ABSOLUTA**")
        return

    if st.button("⚡ LANÇAR"):
        resultados = []
        placeholder = st.empty()
        
        # Animação de rolagem
        for _ in range(8):
            simulacao = [random.randint(1, tipo_dado) for _ in range(qtd_dados)]
            placeholder.write(f"⏳ Rolando: {', '.join(map(str, simulacao))}")
            time.sleep(0.05)
        
        # Rolagem Real
        for _ in range(qtd_dados):
            dado = random.randint(1, tipo_dado)
            # Regra de Crítico 3D&T para D6
            if tipo_dado == 6 and modo_combate and dado == 6:
                resultados.append(12)
            else:
                resultados.append(dado)
        
        soma_dados = sum(resultados)
        total_final = soma_dados + modificador
        
        # Exibição dos Resultados
        st.markdown("---")
        st.write(f"🔢 **Valores Individuais:** {', '.join(map(str, resultados))}")
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("SOMA DOS DADOS", value=soma_dados)
        col_res2.metric("TOTAL FINAL (C/ AJUSTE)", value=total_final, delta=modificador if modificador != 0 else None)

        # Alertas de Crítico (Apenas para 1 dado para não poluir)
        if qtd_dados == 1 and tipo_dado == 6:
            if not modo_combate:
                if resultados[0] == 1: st.success("🌟 SUCESSO CRÍTICO!")
                elif resultados[0] == 6: st.error("💀 FALHA CRÍTICA!")
            elif resultados[0] == 12:
                st.error("🔥 DANO CRÍTICO (6x2=12)")

