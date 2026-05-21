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
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from app.agent.agent import get_agent

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:

    agent = get_agent()
    result = agent.invoke({"messages": [HumanMessage(content=request.message)]})
    return ChatResponse(reply=result["messages"][-1].content)
