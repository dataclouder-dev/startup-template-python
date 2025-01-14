from typing import List, Optional
from pydantic import BaseModel
from pydantic_ai import Agent
# from app.conversations.conversation_models import CharacterCardData
from app.conversations.conversations_classes import LangCodeDescription
# from app.database.mongo import db
import json

# data = db.get_collection('conversations').find_one()

#NOTE GEMINI_API_KEY is in the .env file
class CharacterCardData(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    scenario: Optional[str] = None
    first_mes: Optional[str] = None
    creator_notes: Optional[str] = None
    mes_example: Optional[str] = None
    alternate_greetings: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    system_prompt: Optional[str] = None
    post_history_instructions: Optional[str] = None
    character_version: Optional[str] = None
    # extensions: Optional[Dict[str, Any]] = None
    appearance: Optional[str] = None
    
# NOTE: es mi primer agente, funciona pero creo que debería aprender a optimizarlo. 
async def translate_conversation(conversation_card: dict, current_lang: str, target_lang: str):
    current_data = json.dumps(conversation_card)

    current_lang_description = LangCodeDescription.get(current_lang)
    target_lang_description = LangCodeDescription.get(target_lang)

    conv_translator_agent = Agent(
        'gemini-1.5-pro',
        result_type=CharacterCardData,
        system_prompt='This is a character card for role playing, translate to the specified language all the attributes, return the same structure',  
    )
    result = await conv_translator_agent.run(f'translate the character card to {target_lang_description}: ' + current_data)

    return result
