from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
GREEN = "#78DEC7"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
               'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
               'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # here, first we chose an integer between 8-10, then the loop runs between suppose 0-8,
    # and random letters will be chosen 8 times
    # Same goes for symbols and numbers
    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbols_list = [choice(symbols) for _ in range(randint(2, 4))]
    numbers_list = [choice(numbers) for _ in range(randint(2, 4))]

    # combine all the letters, numbers and symbols into one single password
    password_list = letter_list + symbols_list + numbers_list

    # and then finally shuffle that password
    shuffle(password_list)

    # converts the password list into a string
    password = "".join(password_list)
    password_text.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    # Get hold of the data inside the entries using GET method
    website = website_text.get()
    email = email_text.get()
    password = password_text.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    # If any of the fields is empty, a pop up message will show up
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Please fill all the fields")

    else:
        try:
            # with the help of WITH keyword, the file gets closed on its own
            with open("data.json", "r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=3)
            print("file created")

        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=3)
            print("file has already been created")

        finally:
            # clear out the data inside entries after saving it so that the entry is ready
            # to take the next data
            website_text.delete(0, END)
            password_text.delete(0, END)
            website_text.focus()


def find_password():
    website = website_text.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No Such Data File Found")
    else:
        if website in data:
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=f"{website}", message=f"Email: {email} \n"
                                                            f"Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"no details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=GREEN)

canvas = Canvas(width=200, height=200, bg=GREEN, highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:", bg=GREEN)
website_label.grid(column=0, row=1)

email_label = Label(text="Email:", bg=GREEN)
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", bg=GREEN)
password_label.grid(column=0, row=4)

# Entries
website_text = Entry(width=40, highlightthickness=1)
website_text.config(highlightbackground="yellow", highlightcolor="yellow")
website_text.grid(column=1, row=1, padx=10, pady=10)
# This focus method will focus the cursor automatically whenever we run
# the program so that we dont have to put the cursor onto the first entry.
website_text.focus()

email_text = Entry(width=40, highlightthickness=1)
email_text.config(highlightbackground="yellow", highlightcolor="yellow")
email_text.place(x=69, y=240)
# This method will fill the email entry with our email so
# we dont have to fill our email id repeatedly
email_text.insert(0, "123@gmail.com")

password_text = Entry(width=40, highlightthickness=1)
password_text.config(highlightbackground="yellow", highlightcolor="yellow")
password_text.grid(row=4, column=1, pady=10)

# buttons
search_button = Button(text="Search", width=8, bg="white", command=find_password)
search_button.place(x=350, y=207)

password_button = Button(text="Generate Password", bg="white", width=15, command=generate_password)
password_button.grid(row=4, column=2)

add_button = Button(text="Add", width=15, bg="white", command=save)
add_button.grid(row=6, column=1, columnspan=3)

exit_button = Button(text="Exit", width=15, bg="white")
exit_button.place(x=70, y=303)


window.mainloop()
