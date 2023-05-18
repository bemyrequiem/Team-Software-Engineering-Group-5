'''
================================================
                     UI.py
================================================
Module for handling the user interface
================================================
'''

import tkinter as tk
from gtts import gTTS
from pygame import mixer
import os
from PIL import ImageTk, Image

from Game import Game
from Prompts import Prompt

class UI:
    userMessage = ""
    generatedMessage = ""

    def __init__(self):
        ######## General Setup ########
        self.game = Game("You enter a dungeon in a fantasy world.")
        self.window = tk.Tk()
        self.window.geometry("1200x900")
        self.window.title("Dungeon AI")
        self.window.configure(bg='#0A2239')
        self.path = os.getcwd()

                ######## Setting up frame for use of grid layout ########
        self.entryFrame = tk.Frame(self.window)
        self.entryFrame.configure(bg='#0A2239')
        self.entryFrame.columnconfigure(0, weight=1)
        self.entryFrame.columnconfigure(1, weight=600)
        #self.entryFrame.columnconfigure(2, weight=1)

        ######## Title Text ########
        self.titleText = tk.Label(self.entryFrame, text="Dungeon AI", fg="grey", font= ('Arial', 18), anchor="center")
        self.titleText.configure(bg='#0A2239')
        self.titleText.grid(row=0, column=1, padx=5, pady=10, sticky="we")

        ######## Show Generated Image (by image name 'image.jpg') ########
        self.showImage()

        ######## Show Generated Message Text ########
        self.label = tk.Label(self.entryFrame, text="", font= ('Arial', 12), fg="white", wraplength=900, justify="left", anchor="center")
        self.label.configure(bg='#30332E')
        self.label.config(text="You enter a dungeon in a fantasy world.")
        self.label.grid(row=2, column=1, padx=30, pady=20, sticky="we")

        ######## User Text Entry ########
        self.entryBox = tk.Entry(self.entryFrame, fg="white", font=('Arial', 16))
        self.entryBox.bind("<KeyPress>", self.shortcut)
        self.entryBox.configure(bg='#30332B')
        self.entryBox.grid(row=3, column=0, padx=50, columnspan=2, sticky="we")


        ######## Send Message Button ########
        self.sendButton = tk.Button(self.entryFrame, text=">", font=('Arial', 18), command=self.outputGen)
        self.sendButton.grid(row=3, column=1, padx=5, sticky="e")
        
        ######## TTS Button ########
        self.speechButton = tk.Button(self.entryFrame, text="🔊", font=('Arial', 18), justify="center", command=self.speak)
        self.speechButton.grid(row=3, column=2, padx=5, sticky="e")

        
        ######## Output ########
        #self.entryFrame.pack(fill="x")

        self.entryFrame.place(relx=0.5, rely=0.5, anchor="center")

        self.window.mainloop()

    ######## Enter Shortcut for Text Box ######## 
    def shortcut(self, event):
        if  event.keysym == "Return":
            self.outputGen()

    def showImage(self):
        self.img = ImageTk.PhotoImage(Image.open(self.path + "\\src\\generated-image.png"))
        self.panel = tk.Label(self.entryFrame, image = self.img)
        self.panel.configure(bg='#0A2239')
        self.panel.grid(row=1, column=1, padx=5, pady=20, sticky="we")

    def outputGen(self):
        prompt = self.entryBox.get()
        self.game.generateImage(prompt)
        self.showImage()
        self.game.generateText(prompt)
        #self.speak(input_text)          
        self.userMessage = ''
        self.label.config(text=self.game.text_model.getPrompts())
        self.entryBox.delete(0, 'end')

    def speak(self):
        input_text = self.label.cget("text")
        tts = gTTS(text=input_text, lang='en')

        # Save the speech audio file

        if not os.path.isdir(self.path + "\\src"):
            os.makedirs(self.path + "\\src")
        tts.save(self.path + "\\src\\output.mp3")

        mixer.init()

        # Load the MP3 file
        mixer.music.load(self.path + "\\src\\output.mp3")

        # Play the MP3 file
        mixer.music.play()

        # Wait for the audio to finish playing
        while mixer.music.get_busy():
            continue

        # Clean up
        mixer.quit()
'''
    def updateLabel(self, text):
        existing_text = self.label.cget("text")
        self.userMessage += text[:len(existing_text) + 1]
        self.label.config(text=self.userMessage)
        self.window.after(25, self.updateLabel, text[len(existing_text) - 1:])'''



        #self.textbox = tk.Text(self.window, height=5, font=('Arial', 16))
        #self.textbox.bind("<KeyPress>", self.shortcut)
        #self.textbox.pack(padx=10, pady=10)
        #self.entryBox.grid(row=0, column=0, sticky="we")