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
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor, AgentOutputParser
from langchain import hub

import os 
import dotenv
from app.store import list_recipes, create_recipe, delete_recipe

dotenv.load_dotenv()


# Sans passer par dotenv, est-ce que ca convient @elbby

## dangereux de passer par environ  car getter et setter
_endpoint = os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
_credential=os.getenv("AZURE_AI_INFERENCE_API_KEY")
_model_name=os.getenv("AZURE_AI_INFERENCE_MODEL")


llm = AzureAIChatCompletionsModel(
    endpoint=_endpoint,
    credential=_credential,
    model_name=_model_name
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):  ## je ne comprend pas encore ??
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse) # un decorateur qui indique que cette fonction gère les requetes POST sur le endpoint /chat, et que la reponse doit etre du type ChatResponse
def chat(request: ChatRequest) -> ChatResponse:
    # LangChain attend une liste de messages.
    # SystemMessage = instructions données au modèle (son "rôle").
    # HumanMessage  = le message de l'utilisateur.
    messages = [
        SystemMessage(content="Tu es un assistant culinaire. Réponds en français."),
        HumanMessage(content=request.message),
    ] # formater grace à core.messages

    # invoke() envoie les messages au modèle et retourne un AIMessage.
    # .content contient le texte de la réponse.
    response = llm.invoke(messages)

    return ChatResponse(reply=response.content)
