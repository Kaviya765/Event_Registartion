from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient

class ActionRegisterParticipant(Action):

    def __init__(self):
        # Connect once when the action server starts
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["event_db"]
        self.participants_collection = self.db["participants"]

    def name(self) -> Text:
        return "action_register_participant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot("name")
        user_email = tracker.get_slot("email")
        user_phone = tracker.get_slot("phone")

        # Insert new participant into MongoDB
        self.participants_collection.insert_one({
            "name": user_name,
            "email": user_email,
            "phone": user_phone
        })

        # Fetch all participants to display
        participants = list(self.participants_collection.find())

        # Confirmation message
        dispatcher.utter_message(
            text=f"✅ Registration successful!\n\nName: {user_name}\nEmail: {user_email}\nPhone: {user_phone}\nWe’ll send you event updates soon."
        )

        # Show all registered users
        dispatcher.utter_message(text="📋 Current Registered Participants:")
        for p in participants:
            dispatcher.utter_message(text=f"- {p['name']} ({p['email']}, {p['phone']})")

        return []
