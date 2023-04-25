from tkinter import *
from functools import partial

class Enroll:
    loginScreen = Tk()  
    loginScreen.geometry('1000x500')  
    loginScreen.title('Enrollment')

    center_label = Label(loginScreen)
    center_label.grid(row=1, column=0)

    imgfile = "Images/cppplogo.png"
    image = PhotoImage(file = imgfile)
    image = image.zoom(4,4)
    image = image.subsample(2,2)
    imageLabel = Label(loginScreen, image=image)

    imageLabel.grid(row = 0, column=0, columnspan=2, padx=10, pady=10)

    usernameLabel = Label(center_label, text="Username: ").grid(row = 1, column = 0,sticky="e",padx=5, pady=5)
    username = StringVar()
    usernameEntry = Entry(center_label, textvariable = username).grid(row = 1, column = 1,sticky="w",padx=5, pady=5)  

    passwordLabel = Label(center_label,text = "Password: ").grid(row = 2, column = 0,sticky="e",padx=5, pady=5)  
    password = StringVar()
    passwordEntry = Entry(center_label, textvariable = password, show = '*').grid(row = 2, column = 1,sticky="w",padx=5, pady=5)  


    loginButton = Button(center_label, text = "Login",).grid(row = 3, column = 0,columnspan=2,padx=5, pady=5)  

    loginScreen.update_idletasks()
    width = loginScreen.winfo_width()
    height = loginScreen.winfo_height()
    x = (loginScreen.winfo_screenwidth() // 2) - (width //2 )
    y = (loginScreen.winfo_screenheight() // 2) - (height //2 )

    loginScreen.eval('tk::PlaceWindow . center')
    loginScreen.grid_rowconfigure(0,weight=1)
    loginScreen.grid_columnconfigure(0, weight=1)

    loginScreen.mainloop()

############################## home page #########################
class Homepage:
    homeScreen = Tk()
    homeScreen.geometry('1000x500')  
    homeScreen.title('Home')

    homeScreen.mainloop()


############################## search page #########################


############################## search result page #########################

class Results:
    searchResults = Tk()
    searchResults.geometry('1000x500')  
    searchResults.title('Search Results')

    searchResults.mainloop()

############################## enroll page #########################

class Enroll:
    enrollScreen = Tk()
    enrollScreen.geometry('1000x500')  
    enrollScreen.title('Enrollment')

    enrollScreen.mainloop()


