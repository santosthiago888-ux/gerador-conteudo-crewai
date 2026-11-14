import os
import streamlit as st
import json
import re
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Carrega as variáveis do arquivo .env (para rodar localmente)
load_dotenv()

# Repassa a chave do Streamlit Cloud (Secrets) para o ambiente do CrewAI
try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

def ler_jsonc(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()
    # Remove os comentários // do arquivo .jsonc
    texto_limpo = re.sub(r'//.*', '', texto)
    return json.loads(texto_limpo)

st.title("🤖 Minha Equipe CrewAI")
tema = st.text_input("Sobre qual tema você quer gerar o conteúdo?", "Automação com IA")

if st.button("Gerar Conteúdo"):
    with st.spinner("Os agentes estão trabalhando..."):
        # Lê a configuração do seu agente e da sua tarefa direto dos arquivos .jsonc
        cfg_agente = ler_jsonc("agents/pesquisar_de_tendencia_de_tecn.jsonc")
        cfg_crew = ler_jsonc("crew.jsonc")
        
        agente = Agent(
            role=cfg_agente["role"],
            goal=cfg_agente["goal"],
            backstory=cfg_agente["backstory"],
            llm=cfg_agente["llm"]
        )
        
        tarefa_info = cfg_crew["tasks"][0]
        tarefa = Task(
            description=tarefa_info["description"],
            expected_output=tarefa_info["expected_output"],
            agent=agente
        )
        
        crew = Crew(agents=[agente], tasks=[tarefa])
        resultado = crew.kickoff(inputs={"topic": tema})
        
    st.success("Concluído!")
    st.markdown(resultado.raw)
