import tkinter as tk
from tkinter import font
import json
import string
import os
from tkinter import messagebox

Questions = [
    {"Question":"what is 5 + 5","Answers":["10","35","55","44"],"Correct Answer":"10"}, #1
    {"Question":"who wrote the play Romeo and Juliet","Answers":["martin luther king","george washington","muhammad ali","william shakespeare"],"Correct Answer":"william shakespeare"}, #2
    {"Question":"who was the first President of the United States?","Answers":["martin luther king","george washington","barack obama","donald trump"],"Correct Answer":"george washington"}, #3
    {"Question":"what is the 24th letter in the alphabet","Answers":["a","z","x","i"],"Correct Answer":"x"}, #4
    {"Question":"how many hours are in a day","Answers":["1444","24","12","11"],"Correct Answer":"24"}, #5
    {"Question":"can you have multiple toppings on a burger","Answers":["yes","no"],"Correct Answer":"yes"}, #6
    {"Question":"what day does Christmas start","Answers":["december 21st","december 19th","december 24th","december 28th","december 25th"],"Correct Answer":"december 25th"}, #7
    {"Question":"did You Enjoy The Question game","Answers":["yes","no","maybe","obsolutely!","it was horrible","i don't know i just want to sleep"],"Correct Answer":"_ANY_"} #8
]

TotalQuestions = len(Questions)

Root = tk.Tk()
Root.title("Amazing Quiz Game!")
Root.geometry("1280x720")

ChosenOption = tk.StringVar(Root)
SavedUI = []

try:
      with open("Highest Score.json","r") as File:
            Data = json.load(File)
            LastHighestScore = Data["Last Highest Score"]
            Page = Data["Page"]
            CorrectAnswers = Data["Correct Answers"]
except FileNotFoundError:
         LastHighestScore = 0
         Page = 0
         CorrectAnswers = 0

def CheckAnswer(Answer):
      global Page
      global CorrectAnswers
      CorrectAnswer = Questions[Page-1]["Correct Answer"]
      if Answer == CorrectAnswer or CorrectAnswer == "_ANY_":
            print("Got the right answer")
            CorrectAnswers += 1
      else:
            print("Got the wrong answer")


def ShowResults():
      global LastHighestScore
      HighestScore = round(CorrectAnswers/TotalQuestions*100)
      if HighestScore > LastHighestScore:
            LastHighestScore = HighestScore
      for AnswerUI in SavedUI:
          AnswerUI.destroy()
      SavedUI.clear()
      ResultsLabel = tk.Label(Root,text=f"You got {HighestScore}%!",font=("Georgia", 80))
      ResultsLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
      ResetButton = tk.Button(Root,text="Reset",command=lambda:Reset([ResultsLabel,ResetButton]),width=30,height=2,borderwidth=3)
      ResetButton.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

def Reset(TempUI=None):
      global Page
      global CorrectAnswers
      global LastHighestScore
      Page = 0
      CorrectAnswers = 0
      Answer = messagebox.askyesno("Reset High Score?","Would you like to reset your high score too?")
      if Answer:
            LastHighestScore = 0
      if TempUI:
            for Button in TempUI: Button.destroy()
      UpdateUI(True)

def Save_Data():
      SavedData = {
      "Last Highest Score":LastHighestScore,
      "Page":Page,
      "Correct Answers":CorrectAnswers
    }     
      with open("Highest Score.json","w") as File:
            json.dump(SavedData,File)

def UpdateUI(Start=False):
    global Page
    global LastHighestScore
    if not Start:
      Page += 1
      CheckAnswer(ChosenOption.get()) 
    Save_Data()
    if Page == TotalQuestions:
          ShowResults()
          return
    ChosenOption.set("NONE")
    QuestionLabel = tk.Label(Root,text=string.capwords(Questions[Page]["Question"]),font=("Georgia",25,"italic"))
    QuestionLabel.grid(row=0,column=1)
    for AnswerUI in SavedUI:
          AnswerUI.destroy()
    SavedUI.clear()
    for Position,Answer in enumerate(Questions[Page]["Answers"]):
            AnswerUI = tk.Radiobutton(Root,text=string.capwords(Answer),variable=ChosenOption,value=Answer)
            AnswerUI.grid(row=Position+2,column=1)
            SavedUI.append(AnswerUI)
    ResetButton = tk.Button(Root,text="Reset",command=Reset,width=25,borderwidth=2)
    ResetButton.grid(row=Position+4,column=1)
    AnswerButton = tk.Button(Root,text="Submit",command=UpdateUI,width=25,borderwidth=2)
    AnswerButton.grid(row=Position+5,column=1,pady=5)
    QuestionCount = tk.Label(Root,text=f"Question: {Page+1}/{TotalQuestions}",font=("Arial",14))
    QuestionCount.grid(row=1,column=1)
    HighestScoreLabel = tk.Label(Root,text=f"Highest Score: {LastHighestScore}%")
    HighestScoreLabel.grid(row=Position+3,column=1)
    SavedUI.append(QuestionLabel)
    SavedUI.append(AnswerButton)
    SavedUI.append(QuestionCount)
    SavedUI.append(HighestScoreLabel)
    SavedUI.append(ResetButton)

Root.grid_columnconfigure(0, weight=1)
Root.grid_columnconfigure(1, weight=1)
Root.grid_columnconfigure(2, weight=1)

UpdateUI(True)

#print(Questions)

Root.mainloop()


