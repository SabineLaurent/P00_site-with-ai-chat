import dotenv
import os

dotenv.load_dotenv()

endpoint = os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
api_key = os.getenv("AZURE_AI_INFERENCE_API_KEY")
model_name = os.getenv("AZURE_AI_INFERENCE_MODEL")

if not endpoint or not api_key or not model_name:
    raise ValueError(
        "Missing required environment variables"
    )