"""
Kayla Day
SDEV 140 Final Project
July 28, 2024
This is the Main class of the program. The purpose of this class is to run the program as a GUI that the user can interact with.
There are some labels that are created outside of this class, which is in the PhotoDisplay class. These labels are the ones that hold the photos
as well as the alternate text used in this program. Otherwise, the rest of the GUI widgets are here, as well as the main loop needed to run the program.
That is why I named this the Main class, as the name suggests that it is used to run the program.
I also named this class Main, because if anyone was ever interested in using parts of this file to build upon, other IDEs can be very particular 
about requiring a "Main" class to exist, File names are named the same as the class name, because IDEs can be picky about that as well.

**IMPORTANT: The photos within this project are were photographed, edited, and created by me. I own all of the rights to these photos. While the program itself is made by me as well, I welcome anyone who
would want to use the code and building upon it with credit to me. However, I do not want the photos involved to be used for anything more than viewing purposes, as these are not for anyone other than myself to recreate and distribute. 
"""
# Import statements for the Main class
import tkinter as tk # Imports tkinter which is used for the GUI application
from tkinter import Label, Frame, Canvas, Scrollbar, Toplevel, Entry, Button, PanedWindow # Imports specific to widgets used
import tkinter as ttk # Imports ttk, which is used for the scrollbar in the album
from PIL import Image, ImageTk # Imports PIL, which gives adequate options and quality in displaying the photos in this GUI application
from PhotoDisplay import PhotoDisplay  # Imports the  PhotoDisplay class


# This begins the main class which creates and styles the GUI application. The main loop of this program is ran within this file, which is at the bottom at the end of this main class.
# The purpose of this GUI application is to allow the user to search through my photo album, select the photo they want to personalize for purchase, and select options related to that photo.
# Options refer to digital copy or the size of the print, adding text which is a popular choice in motorcross racing, and alternative print mediums outside the typical type of print that would be placed into a frame.
# Originally, I was going to place the text style, and even vignette previews, but I need to do more research and testing on how a previewed version of that would look through these imports.
# I do not want to add these previews, if they will make the image quality appear bad, because I do not want the user thinking that is the "finalized" version of what they would receive.
# Instead, the options can be selected, those selections along with the information on the customer form, are then printed to show that the information is received.
# In the future, I plan to add that into the database, but in the testing phases, that will create a large table of fake submissions. I would rather add that when I have fully added all of my future plans.
# I also intend to build upon this to begin helping me organize my photos and create my own "recognition" system. The tags are related to this recognition, the rider number, the bike color, name plate color.
# Existing auto recognition systems use the face, in motorcross, the face is covered by a helmet. Using multiple different recognitions and then combining that with body compositition, I hope to achieve a system that works for motorcross photographers.
# I decided to play with a database for this application, for usability with my future ideas, as well as because of the size that this can become. Right now, there are very few photos attached in the file, enough for the purpose of this submission. I come home with approximately 800 photos each race. A database is going to be necessary. As well as better search criteria when I am move advanced in my skills.
# I use colors in the background and text, and font styles to keep a uniformed style through out the application. I use borders to help single out smaller sections that are within larger containers.
# I use a left to right/ and top to bottom type of flow for order and progression through the application. So the first part of the program begins on the left top corner, when completed the photos display underneath, filling the enter left section. This helps the user know that the next flow is going to be on the left, which ends up showing up at the top. The flow logically makes sense that the last interaction (the select button) is expected to be at the bottom of that right half.
# The top level flow follows the first. Where options are selected on the left side, top to bottom, while the form is on the right. The submit button is expected to be underneath the form, which is where I placed it to keep the same flow through out. 
# I did this so that minimal text in guiding the user through the process is needed, and is more kept to options and submission rather than telling the user how to navigate the GUI.
class Main:
    # Define variables that will be used across this class
    def __init__(self, root): # Pass the root window through as well.
        self.root = root # Root is the root container that holds the entire GUI application.
        self.root.geometry("1000x600") # This sizes the application
        self.root.title("Kayla Day MX Photography") # Title of the root window is the name of this program, which I named as my unofficial business name.

        self.main_win = tk.PanedWindow(self.root, bg="black") # Paned window holds all children widgets. A paned window is used to allow resizing between the photo album side, and preview section. This helps, based on the size that the album will become, as well as different screen sizes among users.
        self.main_win.pack(fill="both", expand=True) # Paned window is packed inside of the root, and fills the whole root window.
        # Call the two main methods that involve the first part of this program in this class (they will call next methods).
        # Do not initialize the Editor Method here, otherwise the Top Level will activate before it is supposed to.
        self.setup_photo_search_frame() # Calls the method for the search method and album display
        self.setup_preview_frame() # Calls the method for the preview display

        # Initialize classes
        self.photo_display = PhotoDisplay(self.display_album, self.top_preview_frame) # Initializes communication to the PhotoDisplay class, to be used through out this entire class.
        self.setup_buttons() # intializes the method to initialize some of the buttons involved (not all buttons.) It wasn't necessary, but allows for organization in the future upon growth.

    #This section relates the the search methods and display of the photos in the album. 
    # More specifically, this is the GUI portion that creates the layout and display as well as the interaction for the user
    # This method calls the PhotoDisplay class for manipulation of photos, and the PhotoDisplay class calls the database manager for logic of the search.
    def setup_photo_search_frame(self):
        self.photo_search_frame = tk.Frame(self.main_win, bg="black", bd=5, relief='groove') # Creates the frame to hold the widgets for the search criteria and album
        self.photo_search_frame.pack(side="left", fill='both', expand='True') # Packed into the left side of the panel window, so that it can be resized in the center by the user.
        self.main_win.add(self.photo_search_frame) # Add declares the photo search frame as a child of the paned window, so that is can adopt the options accepted by paned window

        #This section creates the widgets that help guide the user on their search
        self.new_user_search_label = tk.Label(self.photo_search_frame, text="NEW USERS: Narrow your search by entering rider number, date, series, bike or nameplate color. If using rider number, use another descriptor to ensure you receive all photos of the rider you are looking for. (Seperate with comma(,)) ",bg='black', fg='white', font=('Verdana', 10, 'bold'), wraplength=370) # This label creates an informative text to new users, that helps guide them on how they can narrow down their search despite being a new user. 
        self.return_user_search_label = tk.Label(self.photo_search_frame, text="RETURNING USERS: Rider name can be used to narrow search.", bg='black', fg='white', font=('Verdana', 10, 'bold'), wraplength=370) # This label gives an informative text to returning users, guiding them to use the rider's name to narrow search methods.
        self.tag_entry = tk.Entry(self.photo_search_frame) # This creates the text box that the user can type their search descriptors into. When this is sent to the PhotoDisplay and the Database Management classes, these typed entries are the "tags" used in the logic.
        self.search_button = tk.Button(self.photo_search_frame, text="Search Photos", width=20) # This creates the button for the user to submit their search criteria. Not entering anything pulls up the whole album.
        # This section packs the widgets that guide the users search.
        # The order that they are packed places them in the order that they will be displayed vertically.
        self.new_user_search_label.pack(pady=5, padx=3) # New users
        self.return_user_search_label.pack(padx=3, pady=5) # Returning users
        self.tag_entry.pack(padx=3, pady=5, fill='x') # Text entry box
        self.search_button.pack(padx=3, pady=5) # Button to submit search
        # This section is the bottom part of the search section. This section displays the albumn, which is the result of what the user enters or doesn't enter.
        self.canvas = tk.Canvas(self.photo_search_frame, bg="teal") # Canvas is created and necessary for use of the scrollbar. Swapping this out for a different container will alter and even eliminate the functionality of the scrollbar.
        self.scrollbar = ttk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview) # This creates the scrollbar for the album, and places the layout to be vertical and in the yview of the canvas.
        self.display_album = ttk.Frame(self.canvas, bg="teal") # The frame for the photo album that the photos will be placed inside (from the PhotoDisplay class) is created after the scrollbar, so that it "exists" for the next line.
        self.display_album.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),) # This binds the album frame to the scrollbar, and configures the scroll bar to be able to scroll through the entire region of the canvas that encompasses both the scrollbar and the album frame.
        self.canvas.create_window((0, 0), window=self.display_album, anchor='w') # This creates the window for the album and anchors it into the window
        self.canvas.configure(yscrollcommand=self.scrollbar.set) # This configures this command for the canvas and scrollbar to scroll up and down (y), and sets scrollbar(variable name) to do so.
        self.canvas.pack(side='left', fill='both', expand=True) # This packs the canvas into the search frame, however it needs to be declared on the left side because this is declaring its position to to scrollbar in this case.
        self.scrollbar.pack(side='right', fill='y') # Pack the scroll bar on the right side of the canvas and allows it to fill the entire height of the canvas (y)

    # This method sets up and styles the GUI widgets and display of the preview section. 
    # This is where a larger version of the photo that is clicked on in the album is displayed along with its alternate text.
    # The button for final selection of the photo that is in the preview frame opens the next part of this program, which is selection and submission of editing/ordering options
    def setup_preview_frame(self):
        self.preview_frame = tk.Frame(self.main_win, bg="black", width=900, height=800, padx=1, pady=1) # Creates the frame to hold all widgets that will be used in the preview frame
        self.preview_frame.pack(side='right') # Packs this frame on the right side of the photo search frame, dividing the two section for visibility, layout, and user understanding
        self.main_win.add(self.preview_frame) # Makes this frame a child of the paned window, so that is can adopt the options that paned windows accept.

        self.top_preview_frame = tk.Frame(self.preview_frame, bg="black", height=750) # Creates the top portions of the preview frame. The photo and alternate text widgets that are displayed inside of this frame are created in the DisplayPhotos class.
        self.top_preview_frame.pack(side='top', fill='both') # Places this frame in the top portion of the preview frame
        self.choose_photo_button = tk.Button(self.preview_frame, text="Select", command=self.editor) # This creates the button used to open the editor portion of this GUI application. This must be placed in the preview frame. Otherwise, the button gets destroyed due to logic needed to display new instances of preview photos and alternate texts
        self.choose_photo_button.pack(side='bottom') # Places this at the bottom of the frame, so that is displays under the alternate text and photo.
    
    # This method sets up the next part of this GUI application. To put this into a visual look and feel for the user, I used a top level to open a second window, without closing the instances of the first part of this application.
    # This method does not run at all until the select button (var name choose_photo_button) is called, so that the window does not pop up until the user decides to choose the photo in the preview section.
    def editor(self):
        # Creates the edit frame (top level). 
        self.edit_frame = tk.Toplevel(bg="black") 
        self.edit_frame.title("Photo Options") # Gives this top level a title, to guide the user in understanding that the purpose of the window is choosing options related to submitting the order.
        self.edit_frame.geometry('1000x500')  # Adjusts size for better visibility

        # Frame for editor options
        # The variable name suggests controls, because in the future the user will have more control of editing options.
        # For now, it holds selectable options
        self.editor_controls_frame = tk.Frame(self.edit_frame, bg="black", width=400, height=400) # Creates the frame that holds editing option widgets
        self.editor_controls_frame.pack(fill='both', padx=10, pady=20, side='left') # Places on the left side of the frame, to section all purposes to the left.

        # Common font style
        font_style = ("Helvetica", 12) # Initiates a common font style to be used through out this section due to all of the lists and buttons.
        font_color = "#FFFFFF"  # White, used for common text color

        # This section creates and styles the widgets relates to the choice of: Print size or digital copy selection
        self.size_label = tk.Label(self.editor_controls_frame, text="Print Size or Digital Copy:", bg="teal", font=font_style, fg=font_color, bd=2, relief='ridge', padx=5, pady=5) # This label titles the section.
        self.size_label.grid(row=0, column=0, sticky='w', pady=10, padx=10) # Grid is used to place through out editor options. 
        self.sizelist = ['CHOOSE','Digital', '8 x 10', '11 x 14', '16 x 20', '20 x 24', '24 x 30']  # Declares the list of size options, or digital if not wanting print. CHOOSE is there to indicate to the user to make a selection. If no selection is made, I will know, so I will not mistake the first selection in the list as a choice.
        self.size_var = tk.StringVar(self.edit_frame) # Creates a string variable to hold the value of what is chosen in this section.
        self.size_var.set(self.sizelist[0])  # A default value has to be declared, as mentioned, I set CHOOSE so that no selection does not get confused as a selection.
        self.size_optionmenu = tk.OptionMenu(self.editor_controls_frame, self.size_var, *self.sizelist) # Option menu is created. with the variable assigned as well as the list that will display the options. 
        self.size_optionmenu.config(font=font_style, fg=font_color, bg="gray") # This configures styling of the option menu
        self.size_optionmenu.grid(row=0, column=1, pady=10, padx=10) # This is placed in the grid to the right of the label that titles  what this option menu is. 

        # This section creates and styles the widgets relating to the choice of: Alternate print mediums selection
        self.medium_label = tk.Label(self.editor_controls_frame, text="Alternate Print Mediums:", bg="teal", font=font_style, fg=font_color, bd=2, relief='ridge', padx=5, pady=5) # This creates and styles a label the titles this selection section for the user. It is styled the same as the previous label to keep a uniformed look and feel purpose of the previous label.
        self.medium_label.grid(row=1, column=0, sticky='w', pady=10, padx=10) # This places the label under the first label in the grid, starting a new row.
        self.mediumlist = ['NONE', 'Canvas', 'Acrylic', 'Metal', 'Poster']  # This declares the list for the options in this section.
        self.medium_var = tk.StringVar(self.edit_frame) # This creates a string variable to hold the selection that the user makes.
        self.medium_var.set(self.mediumlist[0]) # A default value has to be declared again, so just like the above menu, I start with a value that suggests no selection has been made. I chose NONE, to indicate that not wanting any of those options is an acceptable choice. It also reinforces that the first selection really needs to be selected.
        self.medium_optionmenu = tk.OptionMenu(self.editor_controls_frame, self.medium_var, *self.mediumlist) # Another option menu is created here, with the string variable assigned as well as the list of available options.
        self.medium_optionmenu.config(font=font_style, fg=font_color, bg="gray") # This configures the menu with its text styles and colors.
        self.medium_optionmenu.grid(row=1, column=1, pady=10, padx=10) # This places the menu on the right side of the label. Keeping the same flow to further associate the label as a title description of what this menu is about.

        # This section creates and styles the widgets related to the choice of: Choosing text options to add to the photo
        self.photo_text_label = tk.Label(self.editor_controls_frame, text="Choose Text:", bg="teal", font=("Helvetica", 14, "bold"), fg=font_color, bd=2, relief='ridge', padx=5, pady=5) # This creates a label that titles this section of editing selections. Font type and color stays the same besides becoming bold and appearing slightly larger. This is because this section is different and uses buttons for selection. This gives a visual awareness to this change.
        self.photo_text_label.grid(row=2, column=0, pady=20) # This label is placed in the grid under the first two, starting a new row.

        # This section titles and creates each button selection option for choosing text options to add to the photo.
        # Each button is initially unfilled, and the user can select all or no options.
        self.text_label = tk.Label(self.editor_controls_frame, bg="teal", fg=font_color) # This creates and styles an empty label container to hold the individual buttons to seperate them from the rest of the background and contain them as one.
        self.text_label.grid(row=3, column=0, rowspan=3, pady=5) # This container is placed in the grid under the the label that titles it. Rowspan allows it to stretch across the rows for better visiability between the titles and the actual button.
        
        self.name_var = tk.BooleanVar() # This creates a boolean variable for the first button, the variable name suggests what the boolean value relates to among the options
        self.name_checkbutton = tk.Checkbutton(self.text_label, text="Rider Name", font=font_style, bd=2, relief='groove', padx=5, pady=5, variable=self.name_var) # The butoon is created, the text titles the button, font is styled and colored in theme, the boolean variable is assigned, and a border is used to single out the selection.
        self.name_checkbutton.grid(row=0, column=0, sticky='w', pady=5, padx=10) # Button is placed into the grid of the label container created above to section this off.
        
        self.ridernum_var = tk.BooleanVar() # This creates a new boolean variable for the second button, variable name clarifies what the value is related to.
        self.ridernum_checkbutton = tk.Checkbutton(self.text_label, text="Rider Number", font=font_style, bd=2, relief='groove', padx=5, pady=5, variable=self.ridernum_var) # The butoon is created, the text titles the button, font is styled and colored in theme, the boolean variable is assigned, and a border is used to single out the selection. Style is completely consistent with the first.
        self.ridernum_checkbutton.grid(row=1, column=0, sticky='w', pady=5, padx=10) # This places the button under the first button in a new row
        
        self.series_var = tk.BooleanVar() # The last boolean variable is created, named in relation to the option.
        self.series_checkbutton = tk.Checkbutton(self.text_label, text="Series", font=font_style, bd=2, relief='groove', padx=5, pady=5, variable=self.series_var) # The butoon is created, the text titles the button, font is styled and colored in theme, the boolean variable is assigned, and a border is used to single out the selection. Style remains consistent.
        self.series_checkbutton.grid(row=2, column=0, sticky='w', pady=5, padx=10) # The last button is positioned under the first to for a consistent layout.

        # This section creates and styles widgets to create the look and feel of a customer form.
        # This allows the user to enter their information into text fields that will be submitted with the options.
        # This section displays on the right side of the toplevel, and signifies the last phases of the application. 
        self.form_frame = tk.Frame(self.edit_frame, width=200, height=400, bg="black") # Creates a frame to section of the right side of the top level. It is sized to allow easy visibility of the form and submit order button
        self.form_frame.pack(side='right', fill='both', padx=10, pady=10) # Officially places this frame on the right side of the editor controls frame
        self.info_label = tk.Label(self.form_frame, bg='black', fg=font_color, font=font_style, text="After selecting your photo options on the left, please fill out the form below.", width=200) # Creates label to give instructions to the user.
        self.info_label.pack(fill='both', pady=20, padx=10) # This information label is placed at the top of the form frame, y padding is larger, to seperate it from the actual form.
        self.form_box = tk.Frame(self.form_frame, bg='teal') # A new frame is created and colored to encompass the fields of the form and visually look like a form.
        self.form_box.pack(fill='both', padx=20, pady=20) # The form is packed under the information label, and extra padding helps to seperate it as its own entity.

        # Form fields are declared in this section
        fields = [("First Name:", "first_name"),
                  ("Last Name:", "last_name"),
                  ("Address:", "address"),
                  ("Email:", "email"),
                  ("Phone Number:", "phone_number"),]


        # This section automatically creates labels (for titles) and text entry widgets for the user to enter information to
        #This allows for the more above to be easily added to or changed, without have to write new lines of code to creat the corresponding label and entry widgets.
        for index, (label_text, var_name) in enumerate(fields): # Cycle through the list of paired fields for the form. Enumerate is used because it is very useful for obtaining and manipulating the values in a list that are styled in this fashion. In this case it will take the first pair, and assign the first value to the label_text, and the second will be assigned to var_name. These variable names with their string value will complete the rest of the logic to create the form
            label = tk.Label(self.form_box, text=label_text, fg=font_color, font=font_style, bg='teal') # Creates the label to display the title indicator of what the user need to enter. Assign label_text to assign the value. Each new loop will place the next value for the each first pair in the fields list.
            label.grid(column=0, row=index, padx=10, pady=10, sticky='w') # Places the label into the grid, all labels will remain in the first column, but row will increment with index in the list. This starts places each label in a new row each loop.
            entry = tk.Entry(self.form_box, bg='white', width=40, font=font_style) # Creates the entry widget, which is the text box that the user types into
            entry.insert(0, "none")  # Initializes with "none" with none incase nothing is entered.
            entry.grid(column=1, row=index, padx=5, pady=5) # Places the entry into the grid, each of these will remain in the same column, which it the column to the right of its corresponding label. row increments with index just like the label does. 
            setattr(self, f"{var_name}_entry", entry) # This sets the attribute value of the entry widget and formats the string value for that user input.

        # This creates the sumbit button for the top level editor section. This submits all values of the selections made and input entered for this section of the program. For the user, this is completing the order choices of their photo.
        self.submit_button = tk.Button(self.form_box, text="Submit Order", font=("Helvetica", 14, "bold"), fg=font_color, bg="teal", bd=2, relief='ridge', command=self.submit_order) # This creates the submit order button. Clicking the button calls the submit order function, this command is assigned to the button in this line.
        self.submit_button.grid(column=0, row=len(fields), columnspan=2, pady=20) # This positions the button into the grid under the form. Using columnspan helps to center the button in relation to the form.

    # This method hold the logic to handle the values from the order that was submitted.
    # It begins with the form, so that customer information is shown first.
    # This information is not displayed in the GUI, to simulate a normal order submission feel to it.
    def submit_order(self):
        # Retrieve values from form fields, setting to None if the field is empty
        first_name = self.first_name_entry.get() 
        last_name = self.last_name_entry.get() 
        address = self.address_entry.get()
        email = self.email_entry.get() 
        phone_number = self.phone_number_entry.get() 
        
        # Get selections from the text options. The boolean values are used to decide if they are added to the list or not.
        selected_text_options = []
        if self.name_var.get(): # Retrieves the value for if rider name was selected. If it was the boolean value witll be true and this will run and add Rider name to the list. If not, then this will be skipped.
            selected_text_options.append("Rider Name") # Adds to the list if the button was pressed.
        if self.ridernum_var.get(): # Retrieves the rider number boolean value, the same logic applies as above.
            selected_text_options.append("Rider Number") # Adds Rider number to the list if true
        if self.series_var.get(): # Gets the boolean for series. Runs same logic as above.
            selected_text_options.append("Series") # Adds series to the list if selected.
        
        # Both of these get the value for the to menu option lists
        size_option = self.size_var.get() # This retrieves size
        medium_option = self.medium_var.get() # This retrives the medium.
        
        # I don't have a way to actually store these results currently
        #This section sets up print statements, to display and verify the functionality of the widgets used in this editing options section and to verify that it is all the correct values.
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Address:", address)
        print("Email:", email)
        print("Phone Number:", phone_number)
        print("Text Options:", selected_text_options)
        print("Size Option:", size_option)
        print("Medium Option:", medium_option)

    # This method is to set up buttons related to the GUI
    # So far, it only holds the button for finding and displaying photos. The purpose is more for future use, to clean up code and organization the larger that this program gets.
    def setup_buttons(self):
        self.search_button.config(command=lambda: self.photo_display.find_photos_and_display(self.tag_entry.get())) # configures the search button to call the related method in Photo Display and sends the values of the entered tag names to the class and method needed for further logic.

# This creates and establishes the main loop that will run the the GUI program. It is placed outside of the class, that that the loop continues to run without needing to call a method to keep the GUI running. 
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
