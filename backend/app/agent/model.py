"""Azure AI model factory."""

from app import config
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel


def get_model() -> AzureAIChatCompletionsModel:
    return AzureAIChatCompletionsModel(
        endpoint=config.endpoint,
        credential=config.api_key,
        model=config.model_name,
    )
