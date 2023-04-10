from tkinter import *
from functools import partial

searchScreen = Tk()  
searchScreen.geometry('1000x500')  
searchScreen.title('Search Page')

#cpp image
imgfile = "Images/cppplogo.png"
image = PhotoImage(file = imgfile)
image = image.subsample(2)
imageLabel = Label(searchScreen, image=image)
imageLabel.grid(row = 0, column=0, columnspan=2, padx=10, pady=10)

#course id search bar
courseIDLabel = Label(searchScreen, text="CourseID: ")
courseIDLabel.grid(row=1, column=0, padx=10, pady=10)
courseID = StringVar()
courseIDEntry = Entry(searchScreen, textvariable=courseID)
courseIDEntry.grid(row=1, column=1, padx=10, pady=10)

#filters title
filtersLabel = Label(searchScreen, text="Filters: ", font=("Arial", 14))
filtersLabel.grid(row=2, column=0, padx=10, pady=10)

#major label and dropdown menu
majorLabel = Label(searchScreen, text="Major: ")
majorLabel.grid(row=3, column=0, padx=10, pady=10)

majorOptions = ['None','Computer Science', 'Biology', 'Mathematics', 'History']
major = StringVar()
major.set(majorOptions[0]) 
majorMenu = OptionMenu(searchScreen, major, *majorOptions)
majorMenu.config(width=20)
majorMenu.grid(row=3, column=1, padx=10, pady=10)

#academic standing label and dropdown menu
academicStandingLabel = Label(searchScreen, text="Academic Standing: ")
academicStandingLabel.grid(row=4, column=0, padx=10, pady=10)

academicStandingOptions = ['None','Freshman', 'Sophomore','Junior', 'Senior','Graduate Student']
academicStanding = StringVar()
academicStanding.set(academicStandingOptions[0]) 
academicStandingMenu = OptionMenu(searchScreen, academicStanding, *academicStandingOptions)
academicStandingMenu.config(width=20) 
academicStandingMenu.grid(row=4, column=1, padx=10, pady=10)


#professor
professorLabel = Label(searchScreen, text="Professor: ")
professorLabel.grid(row=5, column=0, padx=10, pady=10)
professor = StringVar()
professorEntry = Entry(searchScreen, textvariable=professor)
professorEntry.grid(row=5, column=1, padx=10, pady=10)


#instruction mode label and dropdown menu
instructionModeLabel = Label(searchScreen, text="Instruction Mode: ")
instructionModeLabel.grid(row=6, column=0, padx=10, pady=10)

instructionModeOptions = ['None','In-Person','Hybrid','Synchronous','Asynchronous']
instructionMode = StringVar()
instructionMode.set(instructionModeOptions[0]) 
instructionModeMenu = OptionMenu(searchScreen, instructionMode, *instructionModeOptions)
instructionModeMenu.config(width=20) 
instructionModeMenu.grid(row=6, column=1, padx=10, pady=10)

searchButton = Button(searchScreen, text="Search")
searchButton.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

searchScreen.mainloop()
