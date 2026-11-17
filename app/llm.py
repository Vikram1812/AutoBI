from langchain_openai import ChatOpenAI

def get_local_llm(temperature: float = 0.0) -> ChatOpenAI:
    """
    Initializes a client pointed to LM Studio's local OpenAI-compatible endpoint.
    Default endpoint: http://localhost:1234/v1
    """
    return ChatOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        model="local-model",
        temperature=temperature,
        timeout=120
    )
