import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionFetchKnowledgeBase(Action):
    def name(self) -> Text:
        return "action_fetch_knowledge_base"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Path to your JSON file
        kb_path = "data/kb.json"

        # Load the JSON file
        try:
            with open(kb_path, "r", encoding="utf-8") as file:
                knowledge_base = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="Maaf, saya tidak dapat menemukan basis pengetahuan.")
            return []

        # Retrieve user intent and entities
        intent = tracker.latest_message["intent"]["name"]
        slot_value = tracker.get_slot("info_type")

        # Determine what to fetch based on intent
        if intent == "ask_about_faculties":
            faculties = knowledge_base.get("fakultas", [])
            response = "Berikut adalah fakultas yang tersedia:\n" + "\n".join(
                [f"- {faculty['nama']}" for faculty in faculties]
            )
            dispatcher.utter_message(text=response)

        elif intent == "ask_registration":
            registration_info = knowledge_base.get("pendaftaran", [])
            response = "Berikut adalah informasi pendafaran:\n" + "\n".join(
                [f"- {info['informasi']}" for info in registration_info[0]["informasi_pendaftaran"]]
            )
            dispatcher.utter_message(text=response)

        else:
            dispatcher.utter_message(text="Maaf, saya tidak dapat menemukan informasi tersebut.")

        return []
