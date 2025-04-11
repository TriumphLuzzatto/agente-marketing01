import streamlit as st
import asyncio
from agente_openai import run_marketing_specialist  # seu script importado

st.title("🤖 Especialista em Marketing com IA")
query = st.text_input("Digite sua pergunta de marketing:")

if st.button("Executar"):
    with st.spinner("Analisando com o especialista..."):
        result = asyncio.run(run_marketing_specialist(query))
        st.markdown("### 💡 Resposta do Especialista:")
        st.write(result)