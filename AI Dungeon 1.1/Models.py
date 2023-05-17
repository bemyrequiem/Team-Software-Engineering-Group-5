'''
================================================
                    Models.py
================================================
Module for handling the main functionality of
the machine learning model from bloom
================================================
'''

# Importing necessary modules for the text model to work
from transformers import BloomForCausalLM, BloomTokenizerFast

# Importing necessary modules for the image model to work
import torch
torch.cuda.empty_cache()
from torch import autocast
from torchvision import transforms as tfms
from diffusers import StableDiffusionPipeline
from datetime import datetime
import os

# Importing local modules
from Prompts import Prompt, PromptList

# Parent class for the different model types
class Model(object):
    def __init__(self, intro_prompt):
        self._model = None
        self._intro_prompt = Prompt(intro_prompt, "Intro")
        self._prompts = PromptList()
        self._prompts.addPrompt(self._intro_prompt)

    def __str__(self):
        return self.promptsToString()

    def getStory(self):
        return self._prompts.getStory()

    def getPrompts(self):
        return self._prompts.getPrompts()
    
    def getPromptsList(self):
        return self._prompts.getPromptsList()

    # Abstract reply method
    def generate(self):
        return
    
    # Abstract reply method
    def generate(self, prompt):
        return

# Child of the Model class
# Responsible for handling the text generation model being used
class TextModel(Model):
    def __init__(self, intro_prompt):
        Model.__init__(self, intro_prompt)
        self._model = BloomForCausalLM.from_pretrained("bigscience/bloom-1b7")
        self.__tokenizer = BloomTokenizerFast.from_pretrained("bigscience/bloom-1b7")
        self.__max_length = 300
        self.__response_length = 180
        self.__inputs = self.__tokenizer(self._intro_prompt.getText(), return_tensors="pt")

    def generate(self):
        response = self.__samplingSearch()
        response.replace(self.getStory(), '')
        self._prompts.addPrompt(Prompt(response, "Computer"))
    
    def generate(self, prompt):
        prompt = prompt + " "
        self._prompts.addPrompt(Prompt(prompt, "You"))
        self.__inputs = self.__tokenizer(self.__getInputs(), return_tensors="pt")
        response = self.__samplingSearch()
        response = self.__cleanResponse(response)
        self._prompts.addPrompt(Prompt(response, "Computer"))

    def __getInputs(self):
        if len(self.getStory()) > 400:
            return self.getStory()[::-400]
        return self.getStory()

    def __cleanResponse(self, response):
        response = response.replace(self.__getInputs(), '', 1)

        if len(response) > self.__response_length: 
            response = response[:self.__response_length - 1]
        response = response.replace("\n", " ")

        while len(response) > 0:
            if response[-1] == "." or response[-1] == "!" or response[-1] == "?":
                break
            if "." not in response and "!" not in response and "?" not in response:
                while response[-1] != " ":
                    response = response[:-1]
                response = response[:-1]
                break
            response = response[:-1]
        return " " + response + " "

    def __samplingSearch(self):
        return self.__tokenizer.decode(self._model.generate(self.__inputs["input_ids"],\
        max_length=self.__max_length, do_sample=True, top_k=50 + len(self._intro_prompt.getText()), top_p=0.9)[0])

    # def __greedySearch(self):
    #     return self.__tokenizer.decode(self._model.generate(self.__inputs["input_ids"],\
    #     max_length=self.__result_length)[0])

    # def __beamSearch(self):
    #     return self.__tokenizer.decode(self._model.generate(self.__inputs["input_ids"],\
    #     max_length=self.__result_length, num_beams=2, no_repeat_ngram_size=2, early_stopping=True)[0])

# Child of the Model class
# Responsible for handling the image generation model being used
class ImageModel(Model):
    def __init__(self, intro_prompt):
        Model.__init__(self, intro_prompt)
        self._model = "CompVis/stable-diffusion-v1-4"
        self.__pipe = StableDiffusionPipeline.from_pretrained(self._model, torch_dtype=torch.float16)
        self.__torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__pipe = self.__pipe.to(self.__torch_device)
        self.__width = 256
        self.__height = 256
        self.__style = "fantasy style"

        with autocast("cuda"):
            self.__image = self.__pipe(self._intro_prompt.getText(), width=self.__width, height=self.__height).images[0]
        self.__saveImage()
    
    def generate(self, prompt):
        torch.cuda.empty_cache()
        prompt = prompt.getText() + self.__style

        with autocast("cuda"):
            self.__image = self.__pipe(prompt, width=self.__width, height=self.__height).images[0]
        self.__saveImage()

    def __saveImage(self):
        path = os.getcwd()
        current_datetime_string = str(datetime.now())
        current_datetime_string = current_datetime_string.replace(":", "").replace(".", "").replace(" ", "_")

        if not os.path.isdir(path + "\\images"):
            os.makedirs(path + "\\images")
        if not os.path.isdir(path + "\\src"):
            os.makedirs(path + "\\src")
        
        self.__image.save(path + "\\images\\IMG_" + current_datetime_string + ".png")
        self.__image.save(path + "\\src\\generated-image.png")