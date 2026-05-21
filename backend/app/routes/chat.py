"""Endpoint de chat — STUB à implémenter par l'étudiant.

Étape 1 : remplacer la réponse 'TODO' par un appel direct à Kimi-K2.6 via
          AzureAIChatCompletionsModel (langchain-azure-ai), sans outils,
          qui renvoie la réponse du modèle.

Étape 2 : transformer ça en agent LangChain avec 3 outils branchés sur app/store.py :
          - list_recipes  → retourne la liste actuelle
          - create_recipe → crée une nouvelle recette
          - delete_recipe → supprime par id
          (voir langchain.agents.create_agent)

Étape 3 (stretch) : mémoire conversationnelle pour suivre une session de chat.
"""


from app import config, store
from fastapi import APIRouter
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@tool
def list_recipes() -> list[str]:
    """Retourne la liste des recettes enregistrées."""
    return store.list_recipes()

@tool
def create_recipe(name: str, ingredients: list[str]) -> str:
    """Crée une nouvelle recette."""
    return store.create_recipe(name, ingredients)

@tool
def delete_recipe(id: str) -> bool:
    """Supprime une recette par son ID."""
    return store.delete_recipe(id)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    model = AzureAIChatCompletionsModel(
        endpoint=config.endpoint,
        credential=config.api_key,
        model=config.model_name,
    )
    response = model.invoke([HumanMessage(content=request.message)])


    return ChatResponse(reply=response.content)
