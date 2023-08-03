from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Language Flash")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
canvas = Canvas(width=800,height=526)

front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

words = pd.read_csv("./data/german_words.csv")
to_learn = words.to_dict(orient="records")
word = {}
def next_card():
    global word,flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(to_learn)
    canvas.itemconfig(card_image,image=front_image)
    canvas.itemconfig(card_title,text="German",fill="black")
    canvas.itemconfig(card_word,text=word["german"],fill="black")
    flip_timer = window.after(3000,flip_card)

def flip_card():
    canvas.itemconfig(card_image,image=back_image)
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=word["english"],fill="white")

flip_timer = window.after(3000,flip_card)

card_image = canvas.create_image(400,263,image=front_image)
card_title = canvas.create_text(400,150,text="german",font=("Arial",40,"italic"))
card_word = canvas.create_text(400,263,text="word",font=("Arial",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)


known_button = Button(image=right_image,highlightthickness=0,command=next_card)
unknown_button = Button(image=wrong_image,highlightthickness=0,command=next_card)

known_button.grid(row=1,column=1)
unknown_button.grid(row=1,column=0)


next_card()

window.mainloop()