# -*- coding: utf-8 -*-
"""
File: main.py
Description: main script.
"""
# from view import App

import util
import os, time
from model import Face, TextToSpeech
import config


class App:
    """The whole app."""

    def __init__(self):
        """initialize the app"""
        # init api connection
        util.init_subscription()

    def run(self):

        path_to_watch = r"/Users/Harry/Pictures/Photo Booth Library/Pictures"
        before = dict([(f, None) for f in os.listdir(path_to_watch)])

        while 1:
            time.sleep(10)
            after = dict([(f, None) for f in os.listdir(path_to_watch)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                print("Added: ", ", ".join(added))

                faces = App.detect(App, os.path.join(path_to_watch, added[0]))

                if faces:
                    for face in faces:
                        person = App.identify(App, face["faceId"], config.GROUP_ID)
                        app = TextToSpeech(
                            config.SPEACH_API_KEY,
                            ("Hi, " + person["name"] + ". How are you?"),
                        )
                        app.get_token()
                        app.save_audio()
                        app.play_audio()
                else:
                    app = TextToSpeech(
                        config.SPEACH_API_KEY , ("Take another photo, you idiot")
                    )
                    app.get_token()
                    app.save_audio()
                    app.play_audio()

            before = after

    def detect(self, original_file_path):
        faces = False
        # ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # original_file_path = os.path.join(ROOT_DIR, url)
        try:
            faces = util.CF.face.detect(original_file_path)
        except:
            raise ("something is wrong")
        finally:
            return faces

    def identify(self, faceId, groupId):
        person = False
        try:
            id = util.CF.face.identify([faceId], groupId)
            if id[0]["candidates"]:
                person = util.CF.person.get(
                    config.GROUP_ID, id[0]["candidates"][0]["personId"]
                )
                print(f"Identified, it's {person['name']}")
            else:
                print("Not found")
        except:
            raise ("something is wrong")
        finally:
            return person


if __name__ == "__main__":
    app = App()
    app.run()
