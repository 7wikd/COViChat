# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset
import smtplib
import pandas as pd
import requests
import json

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


class ActionCoronaTracker(Action):
    def name(self) -> Text:
        return "action_corona_tracker"
    
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://api.covid19india.org/data.json").json()
        
        entities = tracker.latest_message['entities']
        state = tracker.get_slot("state")

        message = "Please enter correct state name: "

        if state == "India":
            state = "Total"
 
        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                if data["statenotes"] == "":
                    data["statenotes"] = "None"
                message = "Hello from COVID-tracker! Current conditions for {} are:\nAs of {}:\nActive: {} Confirmed: {} Recovered: {} Deaths: {}\nAdditional notes:\n{}"\
                    .format(state.title(),data['lastupdatedtime'],data['active'],data['confirmed'],data['recovered'],data['deaths'],data['statenotes'])
                
        
        dispatcher.utter_message(text=message)
    
        return []

def send_Email(emailid, name, body):
    s = stplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login("satwik.dalvi@gmail.com", "Itwillbeonyounowson1123")

    text = "Dear {},\n\n" "Hereby find the required details:\n" + body + "\n\nThanks and regards,\n --COViChat"

    subject = "COViChat request summary"
    message = 'Subject:{}\n\n{}'.format(subject,text)
    s.sendmail("satwik.dalvi@gmail.com",emailid,message)
    s.quit()