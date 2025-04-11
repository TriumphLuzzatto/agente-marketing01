import os
import sys
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, WebSearchTool

# Desabilita o tracing do OpenAI
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "true"

# Carrega as variáveis do .env (caso esteja rodando localmente)
load_dotenv()

# Pega a chave da API do ambiente (funciona no Streamlit também)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY não encontrada. Verifique seus segredos no Streamlit Cloud.")

# Define a chave para o OpenAI
os.environ["OPENAI_API_KEY"] = api_key

# Função principal do agente
async def run_marketing_specialist(query: str):
    agent = Agent(
        name="Marketing Strategy Specialist",
        instructions=(
            "Você é um especialista em estratégia de marketing que ajuda os usuários "
            "a desenvolver campanhas eficazes. Seja claro, estratégico e use exemplos reais sempre que possível."
        ),
        model="gpt-4o",
        model_settings=ModelSettings(
            temperature=0.5,
            max_tokens=1024,
        ),
        tools=[WebSearchTool()]
    )

    print(f"\n🚀 Analisando com o especialista em Marketing: {query}")
    print("-" * 60)

    result = await Runner.run(agent, query)

    print("\n💡 Marketing Insights:")
    print("-" * 60)
    print(result.final_output)
    print("-" * 60)

    return result.final_output

# Se rodar como script principal
async def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Como criar uma campanha de Marketing para meu negócio?"
        print("Nenhuma query fornecida. Usando a query padrão.")

    await run_marketing_specialist(query)

if __name__ == "__main__":
    asyncio.run(main())
