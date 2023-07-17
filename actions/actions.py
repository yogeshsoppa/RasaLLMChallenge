# This files contains your custom actions which can be used to run

# custom Python code.

#

# See this guide on how to implement these action:

# https://rasa.com/docs/rasa/custom-actions





# This is a simple example for a custom action which utters "Hello World!"




# from typing import Any, Text, Dict, List

#

# from rasa_sdk import Action, Tracker

# from rasa_sdk.executor import CollectingDispatcher

#




# class ActionHelloWorld(Action):




#     def name(self) -> Text:

#         return "action_hello_world"




#     def run(self, dispatcher: CollectingDispatcher,

#             tracker: Tracker,

#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:




#         dispatcher.utter_message(text="Hello World!")




#         return []





from typing import Any, Text, Dict, List




from rasa_sdk import Action, Tracker

from rasa_sdk.events import UserUtteranceReverted

from rasa_sdk.executor import CollectingDispatcher

import os

import openai




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

        prompt= f"Please tell the user that ${last_message} is unavailable and give basic explanation on the input"

        openai.api_key =  os.getenv("OPENAI_API_KEY")

        output = openai.Completion.create(

        model="text-davinci-003",

        prompt= prompt,

        max_tokens=7,

        temperature=0)

        dispatcher.utter_message(text= output["choices"][0]["text"])

        # dispatcher.utter_message("this is test message from actions for fallback")

        # Revert user message which led to fallback.

        return []