import os
import tkinter as tk
from tkinter import ttk
#from tkinter.messagebox import showinfo
import openai
from googlesearch import search
import webbrowser
from PIL import ImageTk, Image

# Main window

root = tk.Tk()
root.geometry("1300x600")
root.resizable(True, True)
root.title('Vacation Planner')

def show_button(): # Enables the button to select which hotel you want information for
    select_destination_button.configure(state="enabled")

def open_website(url):
    webbrowser.open_new(url)

def display_selected():  

    for widget in info_f.winfo_children():
        widget.destroy()

    current_destination_label = ttk.Label(info_f, text="Results for " + selected_destination.get(), font=('Tekton Pro', 15))  
    current_destination_label.grid(row=0, column=0, columnspan=2)

    website_label = ttk.Label(info_f, text="Here is a link to the place you selected: ")
    website_label.grid(row=1, column=0)

    for result in search(selected_destination.get(), tld="co.in", num=1, stop=1, pause=2):                           # Google search for hotel website
        website_button = ttk.Button(info_f, text=selected_destination.get(), command=lambda: open_website(result))
        website_button.grid(row=1, column=1) 


def get_results():
    openai.api_key = "KEY"

    costPerDay = str(round(int(budget.get())/int(num_people.get())/int(days.get()),2)) # Calculates the cost per day per person

    # Makes the String to sent to GPT3
    qString = "Give me a list of " + building.get() + "s in " + destination.get() + " that cost less than $" + costPerDay + " per day and have a " + str(rating.get()) + " star rating." # Main string to send to GPT3 if no ammenities required
    aString = " The " + building.get() + "s should have"                                                                                                                                 # Additional string for ammenities

    amenities = [wifi, breakfast, cable, twentyFourHrCheckIn, gym, pool]

    addition = False
    for i in range(len(amenities)):                             # Looks to see if the ammenity should be added
        if (amenities[i].get() != ""):
            aString += " " + amenities[i].get() + ","
            addition = True

    aString = aString[:len(aString)-1]                          # gets rid of extra comma on the end
    aString += "."

    if addition == True:                                        # Adds additional string to the main string if ammenities are requested
        qString += aString

    print(qString)  # Prints the Query String

    response = openai.Completion.create(model="text-davinci-002",
                                            prompt=qString,
                                            temperature=0.7,
                                            max_tokens=50,
                                            top_p=1)
    
    query_result = response.choices[0].text

    print(query_result)  # Prints the String result from GPT3

    #query_result = "\nHampton Inn & Suites Columbus-Downtown\nHilton Garden Inn Columbus Airport\n"  # Temporary so not to constatly use GPT3 while testing

    destinations = []
    
    query_result = query_result.strip('\n')
    destinations = query_result.split("\n")

    print(destinations) # Prints unedited list of places

    for i in range(len(destinations)-1,-1,-1):
        destinations[i] = destinations[i].strip('-,.1234567890() ')
        if destinations[i] == "" or len(destinations[i]) > 75:
            destinations.pop(i)

    print(destinations) # Prints cleaned up list of places

    global selected_destination
    selected_destination = tk.StringVar()

    result_title = ttk.Label(result_f, text="Here is a list of places that meet your criteria:", font=15)
    result_title.grid(row=0, column=0, sticky='w', pady=10)

    for i in range(len(destinations)):
        r = ttk.Radiobutton(result_f, text=destinations[i], value=destinations[i], variable=selected_destination, command=show_button)
        r.grid(row=i+1, column=0, sticky='w')
    
    



# Input Variables
building = tk.StringVar()
destination = tk.StringVar()
days = tk.StringVar()
num_people = tk.StringVar()
budget = tk.StringVar()
rating = tk.IntVar()
wifi = tk.StringVar()
breakfast = tk.StringVar()
cable = tk.StringVar()
twentyFourHrCheckIn = tk.StringVar()
gym = tk.StringVar()
pool = tk.StringVar()

# Input Frame
input_f = ttk.Frame(root, relief='solid', borderwidth=2, padding=10)
input_f.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

# Text Entries
building_label = ttk.Label(input_f, text="What type of location would you like to stay at? (e.g. hotel)").pack(fill='x', expand=True)
building_entry = ttk.Entry(input_f, textvariable=building)
building_entry.pack(fill='x', expand=True)
building_entry.focus()

destination_label = ttk.Label(input_f, text="Where do you want to go? (e.g. Ohio)").pack(fill='x', expand=True)
destination_entry = ttk.Entry(input_f, textvariable=destination).pack(fill='x', expand=True)

days_label = ttk.Label(input_f, text="How many days do you wish to stay?").pack(fill='x', expand=True)
days_entry = ttk.Entry(input_f, textvariable=days).pack(fill='x', expand=True)

num_people_label = ttk.Label(input_f, text="How many people will be staying?").pack(fill='x', expand=True)
num_people_entry = ttk.Entry(input_f, textvariable=num_people).pack(fill='x', expand=True)

budget_label = ttk.Label(input_f, text="What is your budget?").pack(fill='x', expand=True)
budget_entry = ttk.Entry(input_f, textvariable=budget).pack(fill='x', expand=True)

def slider_changed(event):
    rating_value_label.configure(text=rating.get())

rating_label = ttk.Label(input_f, text="What rating do you want your place to have? (1-5)").pack(fill='x', expand=True)
rating_slider = ttk.Scale(input_f, from_=1, to=5, orient='horizontal', command=slider_changed, variable=rating).pack(fill='x', expand=True)
rating_value_label = ttk.Label(input_f, text=rating.get())
rating_value_label.pack(fill='x', expand=True)

amenities_label = ttk.Label(input_f, text="What amenities would you like to have?").pack(fill='x', expand=True)

wifi_checkbox = ttk.Checkbutton(input_f, text="Wifi", variable=wifi, onvalue="wifi", offvalue="").pack(fill='x', expand=True)
breakfast_checkbox = ttk.Checkbutton(input_f, text="Breakfast", variable=breakfast, onvalue="breakfast", offvalue="").pack(fill='x', expand=True)
cable_checkbox = ttk.Checkbutton(input_f, text="Cable", variable=cable, onvalue="cable", offvalue="").pack(fill='x', expand=True)
twentyFourHrCheckIn_checkbox = ttk.Checkbutton(input_f, text="24 Hour Check-in", variable=twentyFourHrCheckIn, onvalue="24 hour check-in", offvalue="").pack(fill='x', expand=True)
gym_checkbox = ttk.Checkbutton(input_f, text="Gym", variable=gym, onvalue="gym", offvalue="").pack(fill='x', expand=True)
pool_checkbox = ttk.Checkbutton(input_f, text="Pool", variable=pool, onvalue="pool", offvalue="").pack(fill='x', expand=True)

q_button = ttk.Button(input_f, text="Find Places", command=get_results).pack(fill='x', expand=True, pady=10)

# Result Frame
result_f = ttk.Frame(root, relief='solid', borderwidth=2, padding=10)
result_f.grid(row=0, column=1)

select_destination_button = ttk.Button(result_f, text="Get more info!", state='disabled', command=display_selected)
select_destination_button.grid(row=100, column=1)


# Info Frame
info_f = ttk.Frame(root, relief='solid', borderwidth=2, padding=10)
info_f.grid(row=1, column=1)
"""
img = ImageTk.PhotoImage(Image.open("mnt.jpg"))
picture_label = ttk.Label(root, image = img)
picture_label.grid(row=2, column=2)
"""


root.mainloop()
