# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("Actions.py")
        dispatcher.utter_message(text="Hello World! First Python action")
    
        return []

class ActionSearchRestaurant(Action):
    def name(self) -> Text:
        return "action_search_restaurant"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        print(entities)

        for e in entities:
            if e['entity'] == 'hotel':
                name = e['value']
            if name == 'indian':
                message = "Indian1, Indian2, Indian3"
            if name == 'chinese':
                message = "Chi1, Chi2, Chi3"
            if name == 'Thai':
                message = "T1, T2, T3"
            
        print("Actions.py")
        dispatcher.utter_message(text=message)
    
        return []

class ActionCoronaTracker(Action):
    def name(self) -> Text:
        return "action_corona_tracker"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://api.covid19india.org/data.json").json()
        
        entities = tracker.latest_message['entities']
        #print("Last message now...", entities)
        state = None

        for e in entities:
            if e['entity'] == 'state':
                state = e['value']
        message = "Please enter correct state name: "

        if state == "India":
            state = "Total"

        for data in response["statewise"]:
            if data["state"] == state.title() or data["statecode"]==state.title():
                print(data)
                if data["statenotes"] == "":
                    data["statenotes"] = "None"
                message = "As of {}:\nActive: {} Confirmed: {} Recovered: {} Deaths: {}\nAdditional notes:\n{}".format(data['lastupdatedtime'],data['active'],data['confirmed'],data['recovered'],data['deaths'],data['statenotes'])
        
        dispatcher.utter_message(text=f"Hello from COVID-tracker! Current conditions for {state.title()} are:\n" + message)
    
        return []
