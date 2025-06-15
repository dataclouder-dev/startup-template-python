import os

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from app.llm.classes import ChatMessageDict

api_key = os.environ["GEMINI_API_KEY"]


genai.configure(api_key=api_key)


def transform_to_gemini(messages_chatgpt: list[ChatMessageDict]) -> list[dict]:
    messages_gemini: list[dict] = []
    system_promt = ""
    for message in messages_chatgpt:
        if message["role"] == "system":
            system_promt += message["content"]
        elif message["role"] == "user":
            messages_gemini.append({"role": "user", "parts": [message["content"]]})
        elif message["role"] == "assistant":
            messages_gemini.append({"role": "model", "parts": [message["content"]]})
    if system_promt:
        if len(messages_gemini) == 0:
            messages_gemini.append({"role": "user", "parts": [system_promt]})
        else:
            messages_gemini[0]["parts"].insert(0, f"*{system_promt}*")
    return messages_gemini


def get_models() -> list[dict]:
    results = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name, m.display_name)
            results.append({"id": m.name, "name": m.display_name})

    return results


class GeminiLLM:
    """Wrapper for google.generativeai.GenerativeModel.

    models/gemini-1.5-flash
    gemini-1.5-pro-latest
    check models using method genai.list_models().
    """

    client = None

    def __init__(self, model_name: str = "models/gemini-1.5-flash") -> None:
        """Initialize the GeminiLLM client.

        Args:
            model_name: The name of the Gemini model to use.
                        Defaults to "models/gemini-1.5-flash".

        """
        self.model_name = model_name
        print("Creating with model ", self.model_name)
        self.client = genai.GenerativeModel(self.model_name)

    def chat(self, messages: list[ChatMessageDict], return_tokens: bool = False, return_json: bool = False) -> str:
        """Process a chat conversation with the Gemini model.

        Note: Gemini's conversation model differs from OpenAI's. It expects
        a strict user-model turn-by-turn interaction. This implementation
        adapts by potentially including the system prompt and the initial
        assistant interaction within the first model part if necessary.
        """
        messages = transform_to_gemini(messages)

        if return_json:
            generation_config = {"response_mime_type": "application/json"}
            response = self.client.generate_content(messages, generation_config=generation_config)
        else:
            response = self.client.generate_content(messages)

        if return_tokens:
            # Google no ofrece una forma nativa de contar los tokens.
            # TODO(@adamo): creo que puedo contar los de salida, con la función pero input se va a volver complicado iterar toda la conversación
            self.client.count_tokens(messages)
            return response.text, {"input": 0, "output": 0, "total": 0}

        return response.text

    def complete(self, message: str, return_json: bool = False) -> str:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        if return_json:
            generation_config = {"response_mime_type": "application/json"}
            response = self.client.generate_content(message, generation_config=generation_config)
        else:
            response = self.client.generate_content(message, safety_settings=safety_settings)

        return response.text
