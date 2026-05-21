"""Agent factory."""

from langchain.agents import create_agent

from app.agent.model import get_model
from app.agent.system_prompt import system_prompt
from app.agent.tools import available_tools


def get_agent():
    model = get_model()
    return create_agent(
        model=model,
        tools=available_tools,
        system_prompt=system_prompt,
    )
