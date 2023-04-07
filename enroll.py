from tkinter import *
from functools import partial

loginScreen = Tk()  
loginScreen.geometry('1000x500')  
loginScreen.title('Enrollment')

usernameLabel = Label(loginScreen, text="Username: ").grid(row = 0, column = 0)
username = StringVar()
usernameEntry = Entry(loginScreen, textvariable = username).grid(row = 0, column = 1)  

passwordLabel = Label(loginScreen,text = "Password: ").grid(row = 1, column = 0)  
password = StringVar()
passwordEntry = Entry(loginScreen, textvariable = password, show = '*').grid(row = 1, column = 1)  


loginButton = Button(loginScreen, text = "Login",).grid(row = 4, column = 0)  

loginScreen.mainloop()