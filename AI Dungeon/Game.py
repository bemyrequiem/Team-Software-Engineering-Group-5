'''
================================================
                    Game.py
================================================
Module for handling the main game loop
================================================
'''

from Models import TextModel, ImageModel

class Game(object):
    def __init__(self, intro_prompt):
        self._intro_prompt = intro_prompt
        self.text_model = TextModel(intro_prompt)
        self.image_model = ImageModel(intro_prompt)

    def generateText(self):
        self.text_model.generate(self._intro_prompt)

    def generateText(self, prompt):
        self.text_model.generate(prompt)

    def generateImage(self):
        self.image_model.generate(self.text_model.getPromptsList()[-1])
    