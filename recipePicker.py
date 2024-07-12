import tkinter as tk # import tkinter
from PIL import ImageTk # import PIL
import sqlite3 # import sqlite3
from numpy import random # import random from numpy

app_width = 500  # set app width
app_height = 600  # set app height
bg_color = "#3d6466"  # set background color

# Initialize app
root = tk.Tk()
root.title("Recipe Picker")  # set title of app
root.eval("tk::PlaceWindow . center")  # center app on screen

# Calculations to center app on screen
screen_width = root.winfo_screenwidth()  # get screen width
screen_height = root.winfo_screenheight()  # get screen height

# x = (screen_width // 2) - (app_width // 2)  # calculate x position
# y = (screen_height // 2) - (app_height // 2)  # calculate y position
# root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")  # set app position on screen

# Create frames
frame1 = tk.Frame(root, width=app_width, height=app_height, bg=bg_color)  # main frame
frame2 = tk.Frame(root, bg=bg_color) # second frame. Height and width are determined by widgets placed inside

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()
        
        
for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky='nsew')  # place frame in window. sticky is to expand in all directions of our frame
    frame.pack_propagate(0)  # don't allow the widgets inside to determine the frame's width / height

def fetch_db():
    conn = sqlite3.connect("data/recipes.db")  # connect to database
    cursor = conn.cursor()  # create cursor object
    cursor.execute("SELECT * FROM sqlite_schema WHERE type = 'table';")  # execute query to get all tables
    all_tables = cursor.fetchall()  # fetch all results
    # get random recipe
    idx = random.randint(0, len(all_tables)-1)  # get random index
    # fetch ingredients
    table_name = all_tables[idx][1]  # get table name
    cursor.execute(f"SELECT * FROM {table_name}")  # execute query to get all ingredients
    table_records = cursor.fetchall()  # fetch all results
    
    conn.close()  # close connection
    return table_name, table_records  # return ingredients and table name. Return structure is IMPORTANT!

def pre_process_data(table_name, table_records):
    # get title
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title]) # convert to lowercase
    
    # get ingredients
    ingredients = []
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        
        # assemble to get full ingredients (e.g. 1 cup of flour)
        full_ingredient = f"{qty} {unit} of {name}"
        ingredients.append(full_ingredient)        
    return title, ingredients  # return title and ingredients


def load_frame1():
    # Clear frame1 before adding new widgets
    clear_widgets(frame1)
    # raise frame 1
    frame1.tkraise()  # raise frame 1
    frame.pack_propagate(0)  # don't allow the widgets inside to determine the frame's width / height
    # Create widgets (stack vertically)
    # Image
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")  # import image
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)  # create widget
    logo_widget.image = logo_img  # keep a reference to the image
    logo_widget.pack()  # pack widget. This will set the image's dimensions (centered)
    # Label
    tk.Label(frame1, text="Ready for your random recipe?", 
         bg=bg_color, fg="white", font=("TkMenuFont", 14)
        ).pack()  # create widget
    # Button
    tk.Button(frame1, 
          text="SHUFFLE", bg="#28393a", 
          fg="white", font=("TkMenuFont", 14),
          cursor="hand2", relief="flat",
          activebackground="#badee2", activeforeground="black",
          command=lambda: load_frame2()
        ).pack(pady=20)  # create widget
    # Label
    tk.Label(frame1, text="Made by Precious",
             fg="white", bg=bg_color, font=("TkMenuFont", 10)
             ).pack(side="bottom")  # create widget

def load_frame2():
    # Clear frame2 before adding new widgets
    clear_widgets(frame2)
    #raise frame 2
    frame2.tkraise()  # raise frame 2
    frame.pack_propagate(1)  # don't allow the widgets inside to determine the frame's width / height

    table_name, table_records = fetch_db()  # fetch database
    title, ingredients = pre_process_data(table_name, table_records)  # pre-process data
    
    # Create widgets (stack vertically)
    # Image
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")  # import image
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)  # create widget
    logo_widget.image = logo_img  # keep a reference to the image
    logo_widget.pack(pady=20)  # pack widget. This will set the image's dimensions (centered)
    # Label
    tk.Label(frame2, text=title, 
         bg=bg_color, fg="white", font=("TkHeadinFont", 20)
        ).pack(pady=25)  # create widget
    # Labels for ingredients
    for i in ingredients:
        tk.Label(frame2, text=i, bg='#28393a', fg="white", font=("TkMenuFont", 12)).pack(fill='both', padx=20) # create widget
    # Button
    tk.Button(frame2, 
          text="BACK", bg="#28393a", 
          fg="white", font=("TkMenuFont", 14),
          cursor="hand2", relief="flat",
          activebackground="#badee2", activeforeground="black",
          command=lambda: load_frame1()
        ).pack(pady=20)  # create widget
    

load_frame1()  # load frame1


# Run app
root.mainloop()
