#
# This is a math quiz application built using Python's Tkinter library. 
# It reads questions, choices, answers and type of question from a CSV file, and presents them to the user in a quiz format. 
# The user can select their answer by typing 'A', 'B', 'C', or 'D' and pressing 'Enter'. 
# The application keeps track of the user's score and provides feedback on whether their answer was correct or incorrect. 
# After a set number of questions, it displays the final score and offers options to retry the quiz or return to the home menu.


from tkinter import *
import csv
from random import choice, shuffle

#----------------GETTING DATA FROM CSV-------------#
def get_data(csv_file: str) -> list:
    #This function is responsible for reading the data from the CSV file and storing it in a list of tuples.
    data = []
    with open(csv_file, mode="r", newline='') as file:
        reader = csv.reader(file)
        next(reader) # Skips the header row
        for row in reader:
            data.append(tuple(row)) 
    return data

#-----------------VARIABLES---------------#
data = get_data("data.csv")
FG_COLOR = "LIGHT GREEN"
BG_COLOR = "BLACK"
FONT = "Courier"
startTimer = 3 # Counts down for 3 seconds before quiz
numProblems = 3 # Number of problems for the duration of the quiz
score = 0 # Score gained from the correct answers
stage = 1 # Starts with the first randomly picked problem
quiz_started = False 

#----------------SETTING UP THE COUNTDOWN-----------#
def countdown(count): 
    # This function is responsible for the countdown before the quiz starts, and also for the countdown between questions. 
    # It takes in the count (in seconds) as a parameter, and updates the timer label accordingly. 
    # If the quiz has not started yet, it sets up the countdown screen with the timer and the label, and starts the countdown. 
    # If the quiz has already started, it simply continues the countdown until it reaches 0, at which point it either displays the final score if the quiz is completed, 
    # or generates the next question if there are still questions left.

    global stage, startTimer, quiz_started
    if count > 0: # If the count is greater than 0, it means the countdown is still ongoing, so it updates the timer label with the current count and continues the countdown after 1 second
        timerLabel.config(text=f"{count}")
        if not(quiz_started): # If the quiz has not started yet, sets up the countdown screen with the timer and the label, and starts the countdown
            window.columnconfigure(0, weight=1)
            window.rowconfigure(0, weight=1)
            window.rowconfigure(1, weight=1)
            label.config(text="The quiz starts in:", font=(FONT, 20, "bold"), fg=FG_COLOR, bg=BG_COLOR)
            label.grid(row=0, column=0, columnspan=2, sticky="nsew")
            timerLabel.config(font=(FONT, 15, "bold"), fg=FG_COLOR, bg=BG_COLOR)
            timerLabel.grid(row=1, column=0, columnspan=2)
            quiz_started = True
            window.after(1000, countdown, count - 1)
        else:    
            window.after(1000, countdown, count - 1)
    else: 
        # If the count is 0, it means the countdown is complete, so it checks if the quiz is completed or not. 
        # If it is, it displays the final score, if not, it generates the next question

        if stage > numProblems: # If the stage is greater than the number of problems, it means the quiz is completed, so it displays the final score and the options to retry or go to menu
            display_result()

        else: # If the stage is not greater than the number of problems, it means the quiz is still ongoing, so it removes the timer and generates the next question
            timerLabel.grid_remove()
            generate_question() 
        

#-------------GETTING A RANDOMIZED PROBLEM FROM DATA------------#
def get_randomized_problem() -> dict:
    # This function is responsible for getting a random problem from the data list, 
    # and returning it as a dictionary with the question, choices, answer, and type of the problem.
    global data
    chosen_problem = choice(data)
    question = chosen_problem[0]
    choices = chosen_problem[1].split(":")
    shuffle(choices) # Shuffling the choices
    choices = tuple(choices) # Converts into tuples for memory efficiency
    answer = chosen_problem[2]
    type = chosen_problem[3]

    dict = { # Creates a dictionary to store the question, choices, answer, and type of the problem for easy access
        "question": question,
        "choices": choices,
        "answer": answer,
        "type": type
    }
    data.remove(chosen_problem) # Removes the chosen problem from the data to prevent duplicated questions
    return dict


#----------------CONTROLLING THE PLACEHOLDER---------#
def on_focus_in(event): 
    # This function is responsible for deleting the placeholder once the user clicks the text box
    if input_text.get("1.0", "end-1c") == "Type 'A', 'B', 'C' or 'D, and press 'Enter'" or input_text.get("1.0", "end-1c") == "Invalid choice!":
        input_text.delete("1.0", END)
        input_text.config(insertbackground=FG_COLOR, insertborderwidth=4, fg=FG_COLOR)

def on_focus_out(event): 
    # This function is responsible for setting the placeholder once the user clicks out the text box
    if not input_text.get("1.0", "end-1c").strip() or input_text.get("1.0", "end-1c").strip() == "Invalid choice!":
        input_text.delete("1.0", END)
        input_text.insert("1.0", "Type 'A', 'B', 'C' or 'D, and press 'Enter'")
        input_text.config(fg=FG_COLOR)
        window.focus_set()

def click_outside(event): 
    # This function is responsible for unfocusing the text box when the user clicks outside of it
    if event.widget == window: 
        # Checks if the user clicks on the window (outside of the text box), 
        # and if so, it sets the focus back to the window and calls the on_focus_out function 
        # to reset the placeholder if necessary
        window.focus_set()
        on_focus_out(None)

#-----------------GENERATING QUESTION-------------------#

def generate_question():
    # This function is responsible for generating the question and the choices on the screen, based on the current stage of the quiz.
    global problem, choices
    problem = get_randomized_problem() # Gets the randomized problem from data
    question = problem["question"]
    choices = {
        'A': problem["choices"][0],
        'B': problem["choices"][1],
        'C': problem["choices"][2],
        'D': problem["choices"][3],
    }
    type = problem["type"]
    if type == "WORD": # If the problem is a word problem, uses a smaller font size to fit the question in the label
        font = (FONT, 12, "bold")
    else: # If not, uses a larger font size for better readability
        font = (FONT, 16, "bold")

    window.grid_columnconfigure(0, weight=1) # Configures the grid to have equal weight for both columns, so that the layout is balanced and adjusts properly when the window size changes
    window.grid_columnconfigure(1, weight=1)

    # Configures the label and the choices to display the question and the choices, with appropriate formatting and layout
    label.config(text=f"{stage}.) {question}", font=font, fg=FG_COLOR, bg=BG_COLOR, justify="left", wraplength=500) # Adjusts the label to fit the question and align it to the left, and wraps the text if it's too long
    label.grid(row=0, column=0, columnspan=2, sticky="w", pady=20)
    
    aLabel.config(text=f"A.) {choices["A"]}", font=font, fg=FG_COLOR, bg=BG_COLOR)
    aLabel.grid(row=1, column=0, sticky="w", padx=70)

    bLabel.config(text=f"B.) {choices["B"]}", font=font, fg=FG_COLOR, bg=BG_COLOR)
    bLabel.grid(row=2, column=0,  sticky="w", padx=70)

    cLabel.config(text=f"C.) {choices["C"]}", font=font, fg=FG_COLOR, bg=BG_COLOR)
    cLabel.grid(row=1, column=1, sticky="w", padx=20)

    dLabel.config(text=f"D.) {choices["D"]}", font=font, fg=FG_COLOR, bg=BG_COLOR)
    dLabel.grid(row=2, column=1, sticky="w", padx=20)
    
    # Configures the input text box for the user to type their answer, with appropriate formatting and layout, 
    # and sets the focus to the window to prevent accidental typing in the text box when it's not supposed to be active
    input_text.grid(row=3, column=0, pady=30, padx=50, sticky="ew", columnspan=2)
    input_text.delete("1.0", END)
    input_text.insert(index="1.0", chars="Type 'A', 'B', 'C' or 'D, and press 'Enter'")
    input_text.config(insertbackground=FG_COLOR, insertborderwidth=4) # Sets the cursor color and border width for better visibility
    window.focus_set()

    #Binding events to the input text box
    input_text.bind("<FocusIn>", on_focus_in)
    input_text.bind("<FocusOut>", on_focus_out)
    input_text.bind("<Return>", check)
    window.bind("<Button-1>", click_outside)

#----------------CHECKING ANSWER------------#
def check(event):
    # This function is responsible for checking the user's answer when they press 'Enter' after typing their choice in the text box.
    global problem, choices, score
    user_choice = input_text.get("1.0", "end-1c").strip().upper() # Gets the user input, removes any leading/trailing whitespace, and converts it to uppercase for comparison
    correct_choice = [k for k, v in choices.items() if v == problem["answer"]][0] # Gets the key of the correct choice (A, B, C, or D) by comparing the value of the choices with the answer in the problem

    if user_choice in ['A', 'B', 'C', 'D']: #Checks if the user input is A, B, C, or D
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)

        #Removes the choices and the text box after the user enters their answer
        aLabel.grid_remove()
        bLabel.grid_remove()
        cLabel.grid_remove()
        dLabel.grid_remove()
        input_text.grid_remove()
        if choices[user_choice] == problem["answer"]: # If the user's choice is correct, it adds 1 to the score and displays "Correct!" in the text box, along with the correct answer.
             score += 1
             label.config(text=f"Correct! The answer is {correct_choice}.) {problem["answer"]}.", font=(FONT, 17, "bold"), fg=FG_COLOR, bg=BG_COLOR, anchor=CENTER)

        else: # If not, it displays "Incorrect!" in the text box, along with the correct answer.
            label.config(text=f"Incorrect! The answer is {correct_choice}.) {problem["answer"]}.", font=(FONT, 17, "bold"), fg="RED", bg=BG_COLOR, anchor=CENTER)
        label.grid(row=0, column=0, pady=20, columnspan=2, sticky="nsew")

        window.focus_set() #This is to prevent the user from accidentally typing in the text box when they are not supposed to, by setting the focus back to the window after they submit their answer.
        next_question()
        
    else: # If not A, B, C, or D, prints out "Invalid choice!" in the text box
        input_text.delete("1.0", END)
        input_text.insert("1.0", "Invalid choice!")
        input_text.config(fg=FG_COLOR)
        window.after(2000, lambda: on_focus_out(None)) #Resets the text box after 2 seconds
        

#----------------GENERATING NEXT QUESTION---------------#
def next_question(): 
    #Generates next question after 3 seconds
    global stage
    countdown(3)
    stage += 1

#----------------DISPLAYING RESULTS--------------#
def display_result():
        # This function is responsible for displaying the final score after the quiz is completed, and providing options to retry the quiz or go back to the menu.
        final_score = int(round(score/numProblems * 100)) # Converts the score to a percentage (integer) for display
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        window.rowconfigure(3, weight=1)
        label.config(text=f"Quiz completed! Your score is: \n\n\n{final_score}%", font=(FONT, 15, "bold"), fg=FG_COLOR, bg=BG_COLOR, anchor=CENTER, justify=CENTER)

        # Configures the abstract button to be a retry button, and the menu button to go back to the home page, with appropriate formatting and layout
        abstractButton.config(text="Retry Quiz", command=retry_quiz, anchor=CENTER, font=(FONT, 15, "normal"), fg=FG_COLOR, bg=BG_COLOR)
        abstractButton.grid(row=1, column=0, pady=5, columnspan=2)
        menu_button.config(text="Go To Menu", command=home, anchor=CENTER, font=(FONT, 15, "normal"), fg=FG_COLOR, bg=BG_COLOR)
        menu_button.grid(row=2, column=0, pady=5, columnspan=2)


#----------------INITIATE COUNTDOWN-------------#
def initiate(): #Starts the countdown for the quiz, and removes the start button
    abstractButton.grid_remove() #Initially removes the start button
    countdown(startTimer)

#----------------RETRY QUIZ------------------#
def retry_quiz():
    # This function is responsible for resetting the quiz variables and data to their initial state, 
    # and starting the quiz again by calling the initiate function.
    global stage, score, quiz_started, data
    stage = 1
    score = 0
    quiz_started = False
    data = get_data("data.csv") # Resets the data to the original state
    menu_button.grid_remove() # Removes the menu button
    initiate()

#-------------------HOME PAGE------------------#
def home():
    # This function is responsible for resetting the quiz variables and data to their initial state, 
    # and displaying the home page with the welcome message and the start button.
    global stage, score, quiz_started, data
    stage = 1
    score = 0
    quiz_started = False
    data = get_data("data.csv") # Resets the data to the original state
    menu_button.grid_remove()
    window.columnconfigure(0, weight=1) #Adjusts the column and row configuration to fit the home page layout
    window.rowconfigure(0, weight=1)
    label.config(text="Welcome to Math Quiz", font=(FONT, 20, "bold"), fg=FG_COLOR, bg=BG_COLOR, anchor="center")
    label.grid(row=0, column=0, pady=20, columnspan=2, sticky="nsew")
    abstractButton.config(text="Start Quiz", command=initiate)
    abstractButton.grid(row=1, column=0)


#-------------------CENTER THE WINDOW ON SCREEN------------------#
def center_window(window):
    # This function is responsible for centering the window on the screen when the application starts.
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

#-------------------MAIN WINDOW------------------#

#
# The following code sets up the main window of the application, with the appropriate title, size, background color, and layout configuration.
#

window = Tk()
window.resizable(width=0, height=0) #Prevents the user from resizing the window to maintain the layout integrity
window.title("Math Quiz")
window.config(width=500, height=350, bg=BG_COLOR)
center_window(window)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(3, weight=1)

#Label to display the title/question
label = Label(text="Welcome to Math Quiz", font=(FONT, 20, "bold"), fg=FG_COLOR, bg=BG_COLOR, anchor="center")
label.grid(row=0, column=0, pady=20, columnspan=2, sticky="nsew")

#Label for the countdown time
timerLabel = Label()

#Labels for A, B, C, D choices
aLabel = Label()
bLabel = Label()
cLabel = Label()
dLabel = Label()

#Anonymous button for both starting and retrying the quiz
abstractButton = Button(text="Start Quiz", font=(FONT, 15, "normal"), fg=FG_COLOR, bg=BG_COLOR, command=initiate)
abstractButton.grid(row=1, column=0)

#Menu Button
menu_button = Button()

#Text box for the user to prompt
input_text = Text(height=3, width=25, bg=BG_COLOR, fg=FG_COLOR, highlightcolor=FG_COLOR)

#-------------------START THE MAIN LOOP------------------#
window.mainloop()

