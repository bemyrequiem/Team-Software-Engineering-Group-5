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
        #self.image_model = ImageModel(intro_prompt)

    def generateImageAndText(self):
        self.text_model.generate(self._intro_prompt)
        #self.image_model.generate(self._intro_prompt)

    def generateImageAndText(self, prompt):
        self.text_model.generate(prompt)
        #self.image_model.generate(prompt)
    