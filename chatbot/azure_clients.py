"""
Azure AI Foundry clients: the embedding function (Cohere embed-v-4-0, via the
Azure AI Inference API) used by both ingest.py and app.py.

Endpoint note: the Foundry resource exposes two different hostnames for the
same resource - `<name>.cognitiveservices.azure.com` (native per-service APIs,
e.g. Azure OpenAI chat deployments) and `<name>.services.ai.azure.com/models`
(the unified Azure AI model-inference route, which is what catalog models
like this Cohere embedding model are actually served from). Confirmed by
testing directly against the real endpoint - the cognitiveservices.azure.com
host 404s for /embeddings; the services.ai.azure.com/models host works.
"""
import os
import time

from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from chromadb import Documents, EmbeddingFunction, Embeddings

EMBED_BATCH_SIZE = 16
MAX_RETRIES = 6


def _inference_endpoint() -> str:
    base = os.environ["AZURE_AI_ENDPOINT"].rstrip("/")
    # base looks like https://<resource>.cognitiveservices.azure.com
    resource = base.split("//", 1)[1].split(".", 1)[0]
    return f"https://{resource}.services.ai.azure.com/models"


class AzureFoundryEmbeddingFunction(EmbeddingFunction[Documents]):
    """Cohere embed-v-4-0 via Azure AI Foundry. Uses Cohere's asymmetric
    input_type: documents are embedded differently than queries for better
    retrieval - this is why embed_query is overridden separately."""

    def __init__(self, deployment: str | None = None):
        self.deployment = deployment or os.environ["AZURE_EMBED_DEPLOYMENT"]
        self._client = EmbeddingsClient(
            endpoint=_inference_endpoint(),
            credential=AzureKeyCredential(os.environ["AZURE_AI_API_KEY"]),
        )

    def _embed_batch_with_retry(self, batch: list, input_type: str):
        for attempt in range(MAX_RETRIES):
            try:
                return self._client.embed(input=batch, model=self.deployment, input_type=input_type)
            except HttpResponseError as e:
                if e.status_code != 429 or attempt == MAX_RETRIES - 1:
                    raise
                retry_after = int(e.response.headers.get("Retry-After", 60)) if e.response else 60
                print(f"  rate limited, waiting {retry_after}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                time.sleep(retry_after)

    def _embed(self, texts: list, input_type: str) -> Embeddings:
        out = []
        for i in range(0, len(texts), EMBED_BATCH_SIZE):
            batch = texts[i : i + EMBED_BATCH_SIZE]
            resp = self._embed_batch_with_retry(batch, input_type)
            out.extend(item.embedding for item in resp.data)
            time.sleep(1)  # stay comfortably under the S0 tier's rate limit between batches
        return out

    def __call__(self, input: Documents) -> Embeddings:
        return self._embed(list(input), input_type="document")

    def embed_query(self, input: Documents) -> Embeddings:
        return self._embed(list(input), input_type="query")

    @staticmethod
    def name() -> str:
        return "azure_foundry_cohere"

    def default_space(self):
        return "cosine"

    def get_config(self) -> dict:
        return {"deployment": self.deployment}

    @staticmethod
    def build_from_config(config: dict) -> "AzureFoundryEmbeddingFunction":
        return AzureFoundryEmbeddingFunction(deployment=config.get("deployment"))
