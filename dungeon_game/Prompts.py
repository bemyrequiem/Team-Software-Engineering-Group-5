'''
================================================
                    Prompts.py
================================================
Module for handling the way a prompt list
should be handled
================================================
'''

from typing import List

class Prompt(object):
    def __init__(self, text, who):
        self.__text = text
        self.__who = who

    def __str__(self):
        return self.__who + ": " + self.__text

    def getWho(self):
        return self.__who

    def getText(self):
        return self.__text

    def last(self):
        return self.__text[-1]

class PromptList(object):
    def __init__(self):
        self.__prompts:List[Prompt()] = []

    def __str__(self):
        return self.__prompts

    def getStory(self):
        story = ""
        for prompt in self.__prompts:
            story += prompt.getText()
        return story

    def getPrompts(self):
        prompts = ""
        for prompt in self.__prompts:
            prompts += prompt.getWho() + ": " + prompt.getText() + "\n"
        return prompts

    def addPrompt(self, prompt):
        self.__prompts.append(prompt)
