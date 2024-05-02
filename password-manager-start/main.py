from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_num = [choice(numbers) for _ in range(randint(2, 4))]
    password_sym = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = password_sym + password_num + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # Add password to clipboard for easy pasting
    pyperclip.copy(password)

# ---------------------------- SEARCH PASSWORD ---------------------------- #
def search():
    searched_web = web_entry.get().title()

    try:
        with open("data.json", mode="r") as data:
            json_data = json.load(data)
    except FileNotFoundError:
        messagebox.showwarning(title="Not Found", message="No passwords have been stored")
    else:
        if searched_web in json_data:
            email = json_data[searched_web]["email"]
            password = json_data[searched_web]["password"]
            messagebox.showinfo(title=f"Password Retrieved", message=f"{searched_web}\n"
                                                                         f"Email: {email}\n"
                                                                         f"Password: {password}")
        else:
            messagebox.showwarning(title="Not Found", message=f"No password was found for {searched_web}")

    finally:
        web_entry.delete(0, END)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    webpage = web_entry.get()
    credentials = log_in_entry.get()
    password = password_entry.get()
    new_data = {
        webpage: {
            "email": credentials,
            "password": password,
        }
    }

    if webpage and password:
        # is_ok = messagebox.askokcancel(title=webpage, message=f"Here are the details to be entered: \nEmail: {credentials}"
        #                                f"\nPassword: {password} \nProceed with saving?")
        # if is_ok:
        try:
            with open("data.json", mode="r") as data:
                # Read old data
                json_data = json.load(data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data:
                json.dump(new_data, data, indent=4)
        else:
            # Updating old data with new data
            json_data.update(new_data)
            with open("data.json", mode="w") as data:
                # Saving updated data
                json.dump(json_data, data, indent=4)
        finally:
                web_entry.delete(0, END)
                password_entry.delete(0, END)
    else:
        messagebox.showerror(title="Missing Information", message="You cannot leave any fields blank")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)


# Label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
log_in_label = Label(text="Email/Username:")
log_in_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Button
gen_pass_btn = Button(text="Generate Password", command=gen_password)
gen_pass_btn.grid(column=2, row=3)
add_btn = Button(text="Add", width=44, command=save)
add_btn.grid(column=1, columnspan=2, row=4)
search_btn = Button(text="Search", width=14, command=search)
search_btn.grid(column=2, row=1)

# Entry
web_entry = Entry(width=34)
web_entry.grid(column=1, row=1)
web_entry.focus()  # Starting cursor
log_in_entry = Entry(width=52)
log_in_entry.grid(column=1, columnspan=2, row=2)
log_in_entry.insert(0, "example@gmail.com")  # Placeholder text
password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)


window.mainloop()
