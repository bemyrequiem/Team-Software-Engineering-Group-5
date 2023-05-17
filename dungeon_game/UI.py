import tkinter as tk
from gtts import gTTS
from pygame import mixer
import os
from PIL import ImageTk, Image

class UI:
    userMessage = ""
    generatedMessage = ""

    def __init__(self):
        ######## General Setup ########
        self.window = tk.Tk()
        self.window.geometry("1200x900")
        self.window.title("Dungeon AI")
        self.window.configure(bg='#0A2239')
        self.path = os.getcwd() + "\\src\\image.jpg"

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
        self.showImage(self.path)

        ######## Show Generated Message Text ########
        self.label = tk.Label(self.entryFrame, text="", font= ('Arial', 12), fg="white", wraplength=900, justify="left", anchor="center")
        self.label.configure(bg='#30332E')
        self.label.grid(row=2, column=1, padx=30, pady=20, sticky="we")

        ######## User Text Entry ########
        self.entryBox = tk.Entry(self.entryFrame, fg="white", font=('Arial', 16))
        self.entryBox.bind("<KeyPress>", self.shortcut)
        self.entryBox.configure(bg='#30332B')
        self.entryBox.grid(row=3, column=0, padx=50, columnspan=2, sticky="we")


        ######## Send Message Button ########
        self.sendbtn = tk.Button(self.entryFrame, text=">", font=('Arial', 18), command=self.outputGen)
        self.sendbtn.grid(row=3, column=1, padx=5, sticky="e")
        
        ######## TTS Button ########
        self.speachbtn = tk.Button(self.entryFrame, text="🔊", font=('Arial', 18), justify="center", command=self.speak)
        self.speachbtn.grid(row=3, column=2, padx=5, sticky="e")

        
        ######## Output ########
        #self.entryFrame.pack(fill="x")

        self.entryFrame.place(relx=0.5, rely=0.5, anchor="center")

        self.window.mainloop()

    ######## Enter Shortcut for Text Box ######## 
    def shortcut(self, event):
        if  event.keysym == "Return":
            self.outputGen()

    def showImage(self, path):
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.panel = tk.Label(self.entryFrame, image = self.img)
        self.panel.configure(bg='#0A2239')
        self.panel.grid(row=1, column=1, padx=5, pady=20, sticky="we")

    def outputGen(self):
        input_text = self.entryBox.get()
        self.imageGen(input_text)
        generatedStory = self.textGen(input_text)
        self.generatedMessage = generatedStory
        #self.speak(input_text)
        if input_text:
            if input_text.endswith('?'):
                pass
            elif input_text.endswith('!'):
                pass
            elif not input_text.endswith('.'):
                input_text += '.'
            
            input_text += ' '
            self.userMessage = ''
            self.label.config(text=generatedStory)
            #self.updateLabel(generatedStory)
            self.entryBox.delete(0, 'end')

    def speak(self):
        input_text = self.label.cget("text")
        tts = gTTS(text=input_text, lang='en')

        # Save the speech audio file
        tts.save("output.mp3")

        mixer.init()

        # Load the MP3 file
        mixer.music.load("output.mp3")

        # Play the MP3 file
        mixer.music.play()

        # Wait for the audio to finish playing
        while mixer.music.get_busy():
            continue

        # Clean up
        mixer.quit()

    def updateLabel(self, text):
        if text:
            self.userMessage += text[0]
            self.label.config(text=self.userMessage)
            self.window.after(25, self.updateLabel, text[1:])


UI()



        #self.textbox = tk.Text(self.window, height=5, font=('Arial', 16))
        #self.textbox.bind("<KeyPress>", self.shortcut)
        #self.textbox.pack(padx=10, pady=10)
        #self.entryBox.grid(row=0, column=0, sticky="we")