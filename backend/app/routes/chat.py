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

from fastapi import APIRouter
from pydantic import BaseModel # C quoi ??
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.agents import create_agent

import os 
import dotenv
from app.store import list_recipes, create_recipe, delete_recipe, RecipeCreate

dotenv.load_dotenv()


# Sans passer par dotenv, est-ce que ca convient @elbby

## dangereux de passer par environ  car getter et setter
_endpoint = os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
_credential=os.getenv("AZURE_AI_INFERENCE_API_KEY")
_model_name=os.getenv("AZURE_AI_INFERENCE_MODEL")


llm = AzureAIChatCompletionsModel(
    endpoint=_endpoint,
    credential=_credential,
    model=_model_name
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):  ## je ne comprend pas encore ??
    message: str


class ChatResponse(BaseModel):
    reply: str

@tool
def list_recipes_tools() -> str:
    """Retourne la liste des recettes actuelles."""
    return str(list_recipes())

@tool
def create_recipe_tools(name: str, ingredients: list[str]) -> str:
    """Crée une nouvelle recette avec le nom et les ingrédients donnés."""
    return str(create_recipe(RecipeCreate(name=name, ingredients=ingredients)))

@tool
def delete_recipe_tools(recipe_id: int) -> str:
    """Supprime la recette avec l'ID donné."""
    return str(delete_recipe(recipe_id))

tools = [list_recipes_tools, create_recipe_tools, delete_recipe_tools]

system_prompt = "Tu es un assistant culinaire. Réponds en français et utilise les tools quand nécessaire."
    
agent = create_agent(llm, tools, system_prompt=system_prompt)


@router.post("", response_model=ChatResponse) # un decorateur qui indique que cette fonction gère les requetes POST sur le endpoint /chat, et que la reponse doit etre du type ChatResponse
def chat(request: ChatRequest) -> ChatResponse:

    
    result = agent.invoke({"messages": [
        {"type": "user", "content": request.message}
    ]})
    return ChatResponse(reply=result["messages"][-1].content)
