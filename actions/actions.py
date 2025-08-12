from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Pre-registered participants
participants = [
    {"name": "Alice Johnson", "email": "alice.j@example.com", "phone": "9876543210"},
    {"name": "Bob Smith", "email": "bob.smith@gmail.com", "phone": "9123456789"},
    {"name": "Priya Sharma", "email": "priya.sharma@yahoo.com", "phone": "9001234567"},
    {"name": "Rahul Kumar", "email": "rahul.k@outlook.com", "phone": "9988776655"},
]

class ActionRegisterParticipant(Action):

    def name(self) -> Text:
        return "action_register_participant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot("name")
        user_email = tracker.get_slot("email")
        user_phone = tracker.get_slot("phone")

        # Save new participant
        participants.append({
            "name": user_name,
            "email": user_email,
            "phone": user_phone
        })

        # Confirmation message
        dispatcher.utter_message(
            text=f"✅ Registration successful!\n\nName: {user_name}\nEmail: {user_email}\nPhone: {user_phone}\nWe’ll send you event updates soon."
        )

        # Optional: show all registered users
        dispatcher.utter_message(text="📋 Current Registered Participants:")
        for p in participants:
            dispatcher.utter_message(text=f"- {p['name']} ({p['email']}, {p['phone']})")

        return []
