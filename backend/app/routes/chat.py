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
from langchain.agents import create_agent
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel


router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@tool
def list_recipes() -> list[dict]:
    """Retourne la liste des recettes enregistrées."""
    return [recipe.model_dump() for recipe in store.list_recipes()]

@tool
def create_recipe(name: str, ingredients: list[str]) -> dict:
    """Crée une nouvelle recette."""
    recipe = store.create_recipe(store.RecipeCreate(name=name, ingredients=ingredients))
    return recipe.model_dump()

@tool
def delete_recipe(recipe_id: int) -> bool:
    """Supprime une recette par son ID."""
    return store.delete_recipe(recipe_id)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    model = AzureAIChatCompletionsModel(
        endpoint=config.endpoint,
        credential=config.api_key,
        model=config.model_name,
    )

    tools = [list_recipes, create_recipe, delete_recipe]

    agent = create_agent(model=model, tools=tools)

    result = agent.invoke({"messages": [HumanMessage(content=request.message)]})

    return ChatResponse(reply=result["messages"][-1].content)
