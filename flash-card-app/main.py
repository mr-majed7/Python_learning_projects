from tkinter import *

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Language Flash")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
canvas = Canvas(width=800,height=526)

front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

canvas.create_image(400,263,image=front_image)
canvas.create_text(400,150,text="german",font=("Arial",40,"italic"))
canvas.create_text(400,263,text="word",font=("Arial",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)


known_button = Button(image=right_image,highlightthickness=0)
unknown_button = Button(image=wrong_image,highlightthickness=0)

known_button.grid(row=1,column=1)
unknown_button.grid(row=1,column=0)


window.mainloop()