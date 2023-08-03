from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

window = Tk()
window.title("Password Manager")
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

site_entry = Entry(width=21)
email_entry = Entry(width=35)
password_entry = Entry(width=18)

site_entry.grid(row=1, column=1)
email_entry.grid(row=2,column=1, columnspan=2)
password_entry.grid(row=3,column=1)

password_generate = Button(text="Generate password")
add_button = Button(text="Add",width=36)
search_button = Button(text="Search",width=13)

password_generate.grid(row=3,column=2)
add_button.grid(row=4,column=1,columnspan=2)
search_button.grid(row=1,column=2)

def saveData():
    if len(site_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
        return
    is_ok = messagebox.askokcancel(title=site_entry.get(), message=f"These are the details entered: \nEmail: {email_entry.get()}\nPassword: {password_entry.get()}\nSave informations?")
    if is_ok:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                data.update({
                    site_entry.get():{
                        "email":email_entry.get(),
                        "password":password_entry.get()
                    }
                })
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                data = {
                site_entry.get():{
                    "email":email_entry.get(),
                    "password":password_entry.get()
                }
            }
                json.dump(data, data_file, indent=4)
        else:
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            site_entry.delete(0,END)
            password_entry.delete(0,END)
add_button.config(command=saveData)


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

password_generate.config(command=generate_password)

def search():
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Saved Data Found")
    else:
        if site_entry.get() in data:
            email = data[site_entry.get()]["email"]
            password = data[site_entry.get()]["password"]
            messagebox.showinfo(title=site_entry.get(), message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists")

search_button.config(command=search)
site_entry.focus()



window.mainloop()