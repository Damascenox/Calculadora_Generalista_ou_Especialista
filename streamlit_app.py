import streamlit as st
import re
import pandas as pd

def limpar_texto(texto):
    """Função para limpar texto"""
    if texto is None or pd.isna(texto):
        return ""
    return str(texto).lower().strip()

def classificar_perfil(dados):
    """Função principal de classificação"""
    pontos_especialista = 0
    pontos_generalista = 0
    
    # 1. Função de atuação
    funcao = limpar_texto(dados.get('funcao_atuacao', ''))
    if funcao in ["engenharia de dados", "ciência de dados"]:
        pontos_especialista += 2
    elif funcao in ["análise de dados", "bi"]:
        pontos_generalista += 3
    
    # 2. Cargo atual
    cargo = limpar_texto(dados.get('cargo_atual', ''))
    if cargo:
        palavras_esp = {
            "cientista de dados": 1.5,
            "data scientist": 1.5,
            "engenheiro de dados": 1.5,
            "data engineer": 1.5,
            "arquiteto de dados": 1.5,
            "data architect": 1.5,
            "machine learning": 1.5,
            "ml engineer": 1.5,
            "ai engineer": 1.5,
            "analytics engineer": 1.5,
            "estatístico": 1.5,
            "professor": 2,
            "pesquisador": 2,
            "desenvolvedor": 1.5,
            "engenheiro de software": 1.5,
            "analista de sistemas": 1.5,
            "outras engenharias": 1.5
        }
        
        palavras_gen = {
            "analista de dados": 2.5,
            "data analyst": 2.5,
            "analista de bi": 2.5,
            "bi analyst": 2.5,
            "business intelligence": 2.5,
            "business analyst": 2.5,
            "analista de negócios": 2.5,
            "product manager": 2.5,
            "data product manager": 2.5,
            "analista de suporte": 2.5,
            "analista técnico": 2.5
        }
        
        pontuacao_aplicada = False
        for palavra, pontos in palavras_esp.items():
            if palavra in cargo:
                pontos_especialista += pontos
                pontuacao_aplicada = True
                break
        
        if not pontuacao_aplicada:
            for palavra, pontos in palavras_gen.items():
                if palavra in cargo:
                    pontos_generalista += pontos
                    break
    
    # 3. Quantidade de atividades diárias
    atividades_diarias = dados.get('atividades_diarias', 0)
    if atividades_diarias >= 6:
        pontos_generalista += 2.5
        pontos_especialista -= 1
    elif atividades_diarias >= 3:
        pontos_generalista += 1.5
    elif atividades_diarias <= 2:
        pontos_especialista += 1
    
    # 4. Formação
    formacao = limpar_texto(dados.get('area_formacao', ''))
    formacoes_especialista = {
        "computação": 1.5,
        "engenharia de software": 1.5,
        "sistemas de informação": 2,
        "ti": 1.5,
        "estatística": 2,
        "matemática": 1.5,
        "matemática computacional": 1.5,
        "ciências atuariais": 2,
        "outras engenharias": 1.5,
        "engenharia": 1.5,
        "química": 1,
        "física": 1
    }
    
    formacoes_generalista = {
        "economia": 2,
        "administração": 2.5,
        "contabilidade": 2.5,
        "finanças": 2,
        "negócios": 2.5,
        "business": 2.5,
        "marketing": 2,
        "publicidade": 2,
        "comunicação": 2,
        "jornalismo": 2,
        "ciências sociais": 2
    }
    
    formacoes_neutras = {
        "ciências biológicas": 1,
        "farmácia": 1,
        "medicina": 1,
        "área da saúde": 1
    }
    
    for area, pontos in formacoes_especialista.items():
        if area in formacao:
            pontos_especialista += pontos
            break
    else:
        for area, pontos in formacoes_generalista.items():
            if area in formacao:
                pontos_generalista += pontos
                break
        else:
            for area, pontos in formacoes_neutras.items():
                if area in formacao:
                    pontos_especialista += pontos * 0.5
                    pontos_generalista += pontos * 0.5
                    break
    
    # 5. Nível de ensino
    nivel_ensino = limpar_texto(dados.get('nivel_ensino', ''))
    if nivel_ensino in ["doutorado", "phd", "doutorado ou phd"]:
        pontos_especialista += 2
    elif nivel_ensino == "mestrado":
        pontos_especialista += 1.5
    elif nivel_ensino == "pós-graduação":
        pontos_especialista += 0.5
    elif nivel_ensino == "estudante de graduação":
        pontos_generalista += 0.5
    
    # 6. Posição de gestão
    eh_gestor = dados.get('eh_gestor', False)
    if eh_gestor:
        pontos_generalista += 2
    
    # 7. Cálculo final
    diferenca = abs(pontos_especialista - pontos_generalista)
    total_pontos = pontos_especialista + pontos_generalista
    
    if diferenca >= 4 and total_pontos >= 4:
        if pontos_especialista > pontos_generalista:
            resultado = "Especialista_Alta_Confianca"
        else:
            resultado = "Generalista_Alta_Confianca"
    elif diferenca >= 2.5 and total_pontos >= 3:
        if pontos_especialista > pontos_generalista:
            resultado = "Especialista_Média_Confianca"
        else:
            resultado = "Generalista_Média_Confianca"
    elif diferenca >= 1.5 and total_pontos >= 1.5:
        if pontos_especialista > pontos_generalista:
            resultado = "Especialista_Baixa_Confianca"
        else:
            resultado = "Generalista_Baixa_Confianca"
    else:
        resultado = "Ambiguo"
    
    return resultado, round(pontos_especialista, 1), round(pontos_generalista, 1)

# Interface Streamlit
def main():
    st.set_page_config(
        page_title="Calculadora de Perfil Profissional",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Calculadora de Perfil Profissional")
    st.markdown("### Descubra se você tem um perfil mais **Especialista** ou **Generalista** em dados")
    
    # Sidebar com informações
    with st.sidebar:
        st.header("ℹ️ Como funciona?")
        st.markdown("""
        Esta calculadora analisa diferentes aspectos do seu perfil profissional:
        
        - **Função de atuação**
        - **Cargo atual**
        - **Quantidade de atividades**
        - **Área de formação**
        - **Nível de ensino**
        - **Posição de gestão**
        
        Com base nessas informações, o sistema calcula uma pontuação para determinar se você tem um perfil mais especialista ou generalista.
        """)
    
    # Formulário principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Informações Profissionais")
        
        funcao_atuacao = st.selectbox(
            "Função de atuação principal:",
            ["", "Engenharia de dados", "Ciência de dados", "Análise de dados", "BI", "Outra"]
        )
        
        cargo_atual = st.text_input(
            "Cargo atual:",
            placeholder="Ex: Analista de Dados, Data Scientist, etc."
        )
        
        atividades_diarias = st.slider(
            "Quantas atividades diferentes você realiza diariamente?",
            min_value=0,
            max_value=10,
            value=3,
            help="Considere tarefas como análise, modelagem, visualização, reuniões, etc."
        )
        
        # Nova pergunta sobre gestão
        eh_gestor = st.radio(
            "Você ocupa uma posição de gestão?",
            ["Não", "Sim"],
            help="Considera liderança de equipe, coordenação de projetos ou gestão de pessoas"
        )
    
    with col2:
        st.subheader("🎓 Formação Acadêmica")
        
        area_formacao = st.selectbox(
            "Área de formação:",
            ["", "Computação", "Engenharia de Software", "Sistemas de Informação", "TI", 
             "Estatística", "Matemática", "Matemática Computacional", "Ciências Atuariais",
             "Outras Engenharias", "Engenharia", "Química", "Física", "Economia",
             "Administração", "Contabilidade", "Finanças", "Negócios", "Business",
             "Marketing", "Publicidade", "Comunicação", "Jornalismo", "Ciências Sociais",
             "Ciências Biológicas", "Farmácia", "Medicina", "Área da Saúde", "Outra"]
        )
        
        nivel_ensino = st.selectbox(
            "Nível de ensino:",
            ["", "Estudante de graduação", "Graduação", "Pós-graduação", "Mestrado", "Doutorado", "PhD"]
        )
    
    # Botão de calcular
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    
    with col_btn2:
        calcular = st.button("🔍 Calcular Perfil", type="primary", use_container_width=True)
    
    if calcular:
        # Preparar dados
        dados = {
            'funcao_atuacao': funcao_atuacao.lower() if funcao_atuacao else '',
            'cargo_atual': cargo_atual,
            'atividades_diarias': atividades_diarias,
            'area_formacao': area_formacao.lower() if area_formacao else '',
            'nivel_ensino': nivel_ensino.lower() if nivel_ensino else '',
            'eh_gestor': eh_gestor == "Sim"
        }
        
        # Calcular resultado
        resultado, pontos_esp, pontos_gen = classificar_perfil(dados)
        
        # Exibir resultados
        st.markdown("---")
        st.subheader("📈 Resultado da Análise")
        
        # Métricas
        col_met1, col_met2, col_met3, col_met4 = st.columns(4)
        
        with col_met1:
            st.metric("Pontos Especialista", pontos_esp)
        
        with col_met2:
            st.metric("Pontos Generalista", pontos_gen)
        
        with col_met3:
            diferenca = abs(pontos_esp - pontos_gen)
            st.metric("Diferença", f"{diferenca:.1f}")
        
        with col_met4:
            if dados['eh_gestor']:
                st.metric("Bônus Gestão", "+2.0", delta="Generalista")
            else:
                st.metric("Bônus Gestão", "0.0")
        
        # Resultado principal
        st.markdown("### 🎯 Seu Perfil:")
        
        if "Especialista" in resultado:
            emoji = "🔬"
            cor = "blue"
            if "Alta_Confianca" in resultado:
                nivel = "Alta Confiança"
                descricao = "Você tem um perfil claramente **especialista**! Suas características indicam foco em áreas técnicas específicas e conhecimento aprofundado."
            elif "Media_Confianca" in resultado:
                nivel = "Média Confiança"
                descricao = "Você tende a ter um perfil **especialista**. Há indicações de especialização técnica, mas com alguns aspectos generalistas."
            else:
                nivel = "Baixa Confiança"
                descricao = "Você pode ter um perfil **especialista**, mas há sinais mistos em sua trajetória profissional."
        
        elif "Generalista" in resultado:
            emoji = "🎭"
            cor = "green"
            if "Alta_Confianca" in resultado:
                nivel = "Alta Confiança"
                descricao = "Você tem um perfil claramente **generalista**! Suas características indicam versatilidade e atuação em múltiplas áreas."
            elif "Media_Confianca" in resultado:
                nivel = "Média Confiança"
                descricao = "Você tende a ter um perfil generalista. Há indicações de versatilidade, mas com alguns aspectos de especialização."
            else:
                nivel = "Baixa Confiança"
                descricao = "Você pode ter um perfil generalista, mas há sinais mistos em sua trajetória profissional."
        
        else:
            emoji = "⚖️"
            cor = "orange"
            nivel = "Perfil Ambíguo"
            descricao = "Seu perfil apresenta características equilibradas entre especialista e generalista. Isso pode indicar uma transição de carreira ou um perfil híbrido."
        
        st.markdown(f"""
        <div style="
            padding: 20px; 
            border-radius: 10px; 
            background-color: rgba(0, 123, 255, 0.1); 
            border-left: 5px solid {'#007bff' if cor == 'blue' else '#28a745' if cor == 'green' else '#ffc107'};
            margin: 20px 0;
        ">
            <h2 style="margin: 0; color: {'#007bff' if cor == 'blue' else '#28a745' if cor == 'green' else '#ffc107'};">
                {emoji} {resultado.replace('_', ' ').title()}
            </h2>
            <h4 style="margin: 10px 0; color: #666;">Nível de Confiança: {nivel}</h4>
            <p style="margin: 15px 0; font-size: 16px; line-height: 1.6;">
                {descricao}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
       

if __name__ == "__main__":
    main()