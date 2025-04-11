import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, WebSearchTool
import asyncio
import sys

# Desabilitando traces
os.environ["OPENAI_AGENTS_DISABLE_TRACING"] = "true"

# Carrega as variáveis do .env
load_dotenv()

# Pega a chave da API do .env
api_key = os.getenv("OPENAI_API_KEY")

# ⚠️ TESTE: mostra se a chave foi lida corretamente
print("Chave da API lida do .env:", api_key)

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY não encontrada nos segredos (Secrets) do Streamlit Cloud")

# Define a chave no ambiente para o cliente OpenAI funcionar
os.environ["OPENAI_API_KEY"] = api_key

async def run_marketing_specialist(query: str):
    """Executa o especialista em estratégia de Marketing"""
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

async def main():
    """Processa a requisição"""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Como criar uma campanha de Marketing para meu negócio?"
        print("Nenhuma query fornecida. Usando a query padrão.")

    await run_marketing_specialist(query)

if __name__ == "__main__":
    asyncio.run(main())