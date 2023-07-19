from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ActionDefaultFallback(Action):

    """Executes the fallback action and goes back to the previous state
    of the dialogue"""
    def name(self) -> Text:
        return "action_default_fallback"

    # action_default_fallback
    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        
        last_message = tracker.latest_message.get("text", "")

        openai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Find a way to rephrase: I don't know about" + last_message + "but I can tell you about pizza"}],
            max_tokens=200,
            temperature=0,
        )["choices"][0]["message"]["content"]

        dispatcher.utter_message(text=f"That's out of my scope. {openai_response}")
        # Revert user message which led to fallback.

        return
