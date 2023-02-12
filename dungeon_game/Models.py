'''
================================================
                    Models.py
================================================
Module for handling the main functionality of
the machine learning model from bloom
================================================
'''

# Importing necessary modules for the models to work
import torch
from transformers import BloomForCausalLM, BloomTokenizerFast
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

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
        self.__inputs = self.__tokenizer(self.getStory(), return_tensors="pt")
        self.__result_length = 50

    def generate(self):
        self._prompts.addPrompt(Prompt(prompt, "You"))
        response = self.__samplingSearch()
        response.replace(self.getStory(), '')
        self._prompts.addPrompt(Prompt(response, "Computer"))
    
    def generate(self, prompt):
        self._prompts.addPrompt(Prompt(prompt, "You"))
        self.__inputs = self.__tokenizer(self.__getInputs(), return_tensors="pt")
        response = self.__samplingSearch()
        response = self.__cleanResponse(response)
        self._prompts.addPrompt(Prompt(response, "Computer"))

    def __getInputs(self):
        if len(self.getStory()) < 50 + len(self._intro_prompt.getText()):
            return self.getStory()
        return self._intro_prompt.getText() + self.getStory()[-self.__result_length::]

    def __cleanResponse(self, response):
        response = response.replace(self.__getInputs(), '', 1)
        head, sep, tail = response.split('.!?')[0]
        return head

    def __samplingSearch(self):
        return self.__tokenizer.decode(self._model.generate(self.__inputs["input_ids"],\
        max_length=self.__result_length, do_sample=True, top_k=50 + len(self._intro_prompt.getText()), top_p=0.9)[0])

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
        self._model = "stabilityai/stable-diffusion-2-1"
        self.__pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
        self.__pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        self.__pipe = pipe.to("cuda")

    def generate(self):
        return
    
    def generate(self, prompt):
        return
