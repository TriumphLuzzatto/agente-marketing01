from typing import List, Optional
from openai import OpenAI
import asyncio
import os

class ModelSettings:
    def __init__(self, temperature=0.7, max_tokens=1024):
        self.temperature = temperature
        self.max_tokens = max_tokens

class WebSearchTool:
    def __init__(self):
        pass

    def search(self, query: str) -> str:
        return f"Resultado simulado da busca para: {query}"

class Agent:
    def __init__(self, name: str, instructions: str, model: str, model_settings: ModelSettings, tools: Optional[List[object]] = None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.model_settings = model_settings
        self.tools = tools if tools else []

    def process_query(self, query: str) -> str:
        tool_output = ""
        for tool in self.tools:
            if isinstance(tool, WebSearchTool):
                tool_output += tool.search(query) + "\n"

        prompt = f"{self.instructions}\n\n{tool_output}\nUsuário: {query}\nEspecialista:"

        # Cria o cliente OpenAI com a chave da API
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.model_settings.temperature,
            max_tokens=self.model_settings.max_tokens
        )

        return response.choices[0].message.content

class Runner:
    @staticmethod
    async def run(agent: Agent, query: str):
        class Result:
            final_output: str
        result = Result()
        result.final_output = await asyncio.to_thread(agent.process_query, query)
        return result