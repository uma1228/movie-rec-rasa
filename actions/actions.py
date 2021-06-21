# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker

# from rasa_sdk.executor import CollectingDispatcher
#
import pandas as pd
import random


class ActionMovieRecs(Action):
    def name(self):
        return "action_movieRecs"

    def run(self, dispatcher, tracker, domain):
        frame = pd.read_csv("movieData.csv")

        lang = tracker.get_slot("lang").lower()
        gen = tracker.get_slot("gen")

        langD = dict(iter(frame.groupby('lang')))  # sorts by language
        i = 0
        temp = []
        while i < len(langD[lang]):  # iterating through the movies of a specific language
            for w in langD[lang].iloc[i][1].split(','):  # going through each of the genres
                if w.casefold().strip() == gen.casefold().strip():  # genre match
                    temp.append(langD[lang].iloc[i])
            i += 1
        if len(temp) <1:
            dispatcher.utter_message(text="no results found in our database. Sorry :(")
        else:
            movie = random.choice(temp)
            toReturn = movie.iloc[0] + ' (' + str(movie.iloc[3]) + ')'
            dispatcher.utter_message(text=toReturn)
        return []

class ActionActorMovieRecs(Action):
    def name(self):
        return "action_movieRecsActor"
    def run(self,dispatcher, tracker, domain):
        act = tracker.get_slot("actor").lower()
        frame = pd.read_csv("movieData.csv")
        temp = []
        i = 0
        while i < len(frame):
            for name in frame.iloc[i][4].split(','):
                if name.lower().strip() == act.strip():
                    temp.append(frame.iloc[i])
            i += 1

        if len(temp)<1:
            dispatcher.utter_message(text="No results found in our database. Sorry :(")
        else:
            movie = random.choice(temp)
            toReturn = movie.iloc[0] + ' (' + str(movie.iloc[3]) + ')'
            dispatcher.utter_message(text=toReturn)
        return []


