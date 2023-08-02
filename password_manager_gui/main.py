from tkinter import *

window = Tk()
window.title("Password Manager")
# window.minsize(width=450,height=500)
window.config(padx=20, pady=20)
canvas = Canvas(width=200,height=200)

logo = PhotoImage(file="logo.png")
canvas.create_image(100 ,100, image=logo)
canvas.grid(row=0, column=1)

site_label = Label(text="Site")
email_label = Label(text="Email/Username")
password_label = Label(text="Password")

site_label.grid(row=1,column=0 )
email_label.grid(row=2, column=0)
password_label.grid(row=3,column=0)

site_entry = Entry(width=35)
email_entry = Entry(width=35)
password_entry = Entry(width=18)

site_entry.grid(row=1, column=1, columnspan=2)
email_entry.grid(row=2,column=1, columnspan=2)
password_entry.grid(row=3,column=1)

password_generate = Button(text="Generate password")
add_button = Button(text="Add",width=36)

password_generate.grid(row=3,column=2)
add_button.grid(row=4,column=1,columnspan=2)

window.mainloop()