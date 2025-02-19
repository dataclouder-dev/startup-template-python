import os

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

from app.llm.classes import ChatMessageDict

api_key = os.environ["GEMINI_API_KEY"]


genai.configure(api_key=api_key)


def transform_to_gemini(messages_chatgpt: list[ChatMessageDict]):
    messages_gemini = []
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


def get_models():
    results = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            print(m.name, m.display_name)
            results.append({"id": m.name, "name": m.display_name})

    return results


# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)


class GeminiLLM:
    """Wrapper for google.generativeai.GenerativeModel
    models/gemini-1.5-flash
    gemini-1.5-pro-latest
    check models using method genai.list_models()
    """

    client = None

    def __init__(self, model_name="models/gemini-1.5-flash"):
        # self.model_name = model_name if model_name in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro'] else 'models/gemini-1.5-flash'
        self.model_name = model_name or "models/gemini-1.5-flash"
        print("Creating with model ", self.model_name)
        self.client = genai.GenerativeModel(self.model_name)

    def chat(self, messages: list[ChatMessageDict], return_tokens: bool = False, return_json: bool = False):
        """Entender: no funciona como OpenAI, la conversación solo va uno y uno model y user, por eso en el primer model incluyo 2 partes, system promp y primer assistant interaction"""
        messages = transform_to_gemini(messages)

        # model = genai.GenerativeModel('gemini-1.0-pro-latest')
        if return_json:
            generationConfig = {"response_mime_type": "application/json"}
            response = self.client.generate_content(messages, generation_config=generationConfig)
        else:
            response = self.client.generate_content(messages)

        if return_tokens:
            # Google no ofrece una forma nativa de contar los tokens.
            # TODO: creo que puedo contar los de salida, con la función pero input se va a volver complicado iterar toda la conversación
            self.client.count_tokens(messages)
            return response.text, {"input": 0, "output": 0, "total": 0}

        return response.text

    def complete(self, message: str, return_json: bool = False):
        # messages = transform_to_gemini(messages)
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            # HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }
        if return_json:
            generationConfig = {"response_mime_type": "application/json"}
            response = self.client.generate_content(message, generation_config=generationConfig)
        else:
            response = self.client.generate_content(message, safety_settings=safety_settings)

        return response.text
