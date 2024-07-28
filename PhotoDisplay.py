"""
Kayla Day
SDEV 140 Final Project
July 28, 2024
This part of the program is used to display the photos for the user. It will display a smaller thumbnail sized photos as an albumn that can be scrolled through,
as well as a preview (larger version) of the photo that is clicked on. This class calls to the database as needed and displays the photos and alternate text that 
it recieves from the database. 
"""
# Import statements setction.
import tkinter as tk # Imports tkinter for GUI
from tkinter import Label # Imports label from tkinter
from PIL import Image, ImageTk # Imports Image and Image tk from PIL so that photos can be displayed in the GUI and manipulated for layout
from math import ceil # Imports the math module, ceil is used for layout in unknown row size.
from DatabaseManagement import DatabaseManagement # Imports the database class that is located in its own file.

# Begins the PhotoDisplay class. The only gui portions in this class are relative to the specific container that holds each image and the alternate text. Those containers are sent to the Main class. 
# This class receives requests from the GUI in the main class, coordinates those requests with the database, prepares the photo, and sends that photo / alternate text packed in its gui container back to the main class
class PhotoDisplay:
    # Defines variables of this class. It recieves two container names from the main class which are needed to store the GUI containers into. 
    # It also initializes lists that can interact among the entire class. This allows fluent passing of the data without having to worry about how many arguments it is receiving or must receive at a time.
    def __init__(self, parent_display_album, parent_top_preview_frame):
        self.parent_display_album = parent_display_album # This is the album container of the main class, used to hold small images from 1 to the whole album
        self.parent_top_preview_frame = parent_top_preview_frame # This is the preview frame container from the main class, this holds a much larger version of whatever photo the user click on in the album container.
        self.display_photos = [] # intializes the list to hold photos that will go into the albumn container
        self.photo_labels = [] # initializes the list to hold the containers with the photos.
        self.db_manager = DatabaseManagement() # Initializes the communication to the datatbase management class for use throughout the entire class.

    # This method receives the tags from the main class that the user entered. It is called when the search button is pushed.
    # This method will send those tags to the database management class and call the next method needed to display the results.
    def find_photos_and_display(self, tag): # Allow tags to come in
        self.display_photos = self.db_manager.find_photos(tag) # Makes display photos list to equal the image paths (file names of the photos) and sends any tag names entered to further define the search criteria.
        self.load_display_photos() # Calls the next method, meaning that it causes the method to begin running. Needed because everything outside of the Main method is not going to automatically run since it is not in the main loop.

    # This method is called as a result of find photos (and display). This is the display part of that method. This will take in the display photos list, filled from the database.
    # This method will then manipulate those photos by resizing them, and packing them into labels. Those labels are formatted into a grid, and sent to the main class.
    # The main class will receive these labels, and those labels will be placed in the album container, whose information (variable name) was sent and declared in the init portion of this class.
    def load_display_photos(self): # Only pass in self, because every variable it needs to receive is defined as self and/or coming from another class/method.
        # Giving a widget new data does not replace the old data, so the widgets have to be destroyed.
        # Doing this initially allows for new instances without having to restart the application or adding to the previous. The user can search and receive new results rather than being stuck with their decision.
        for label in self.photo_labels: # Cycle through every label the may or may not be in the photo label list
            label.destroy() # Destroy the labels inside of the list
        self.photo_labels.clear() # Clear the list also for extra emptiness, or incase the widgets start acting like cockroaches. If the list isn't cleared, it will just create new labels of the same photos.

        num_photos = len(self.display_photos) # Determine how many image files exist (don't use -1 because this isn't being used for index!)
        num_rows = ceil(num_photos / 3) # Use that length of the list (the number of photos that will be displayed), and divide by 3. This will determine the amount of rows that there will be. 3 represents how many colums there will be, which is already known.
        c = 0 # Set colums variable to 0
        r = 0 # Set row variable to 0

        # This section is going to manipulate every photo, create a label, and place the photo of each label. It also determines the placement in the grid each time.
        for image_path in self.display_photos: # Cycle through each photo path in the list that came from the database.
            try:
                img = Image.open(image_path) # Create the GUI Image of the photo and open the file name of the photo.
                original_width, original_height = img.size # Grab the width and height (this is automatic because metadata travels with photos and are attached to them in their files.) Make size represent this size for this image (img)
                aspect_ratio = original_width / original_height # Aspect ratio is used to keep the same proportions when resizing images. This is used to maximize quality and prevent distortion problems. The equation is simply dividing the width by the height.
                new_width = 100 # Create the new width size
                new_height = int(new_width / aspect_ratio) # divide the new width by aspect ratio and use that to determine the new height of the image.
                img_resized = img.resize((new_width, new_height), Image.BILINEAR) # resize the image with the new width and height, Bilinear is used for 2D resizing, because two values, height and width, are being used.
                photo = ImageTk.PhotoImage(img_resized) # Create the resized and final Gui image that will be placed in the container.

                label = Label(self.parent_display_album, image=photo, bd=5, relief="raised") # Create the label to hold the GUI image. Declare the parent container, and borders
                label.grid(padx=1, pady=1, column=c, row=r) # Place the label into a grid, make the column and row equal the values in c and r so that each new photo is placed in a new position on the grid.
                label.image = photo # Save an instance of the image and photo (So that it doesn't get lost in the trash)
                label.image_path = image_path # Save an instance of the image path as well for the same reason.
                label.bind("<ButtonRelease-1>", self.on_image_clicked) # Bind this label to an event instance for if it is clicked on, command the event to run the on image clicked class. Doing this here creates an event trigger for each individual photo. 
                self.photo_labels.append(label) # Add the label to the photo labels list.
                # This is where c and r are incremented to determine grid placement 
                c += 1 # Allow c to increment by one to fill the colums of the row
                if c >= 3: # When all of the colums in the row are filled, this will become true
                    c = 0 # Make c equal zero again, to begin filling the next row
                    r += 1 # Increment r to start the next row

            except Exception as e: # Error handling when there is an issue with loading an image.
                print(f"Error loading {image_path}: {e}") # print the error for debugging, Error loading specifies that there was an issue within this section and the specific image path(s) will be given as well to help narrow down the problem.

    # This method is called when one of the the smaller photos displayed in the album portion of the GUI is clicked on by the user.
    # The purpose of the next two methods and event is to display a larger version of the photo into the display portion, so that the user can see a more accurate version of the original photo. 
    # The smaller versions make scrolling through many photos much simpler, but by doing so, they lose out on a clarity, so this method, in combination with the previous will allow the user to experience easy navigation through the search, while still being able to have a full view of the photo before they enter the ordering phase.
    # This method specifically receives the trigger from the Main class, and sends the image path of the photo to the database, the database will return the alternate text, and then this method sends everything to the next method to configure the display.
    def on_image_clicked(self, event): # allow the variables in this class needed, as well as the event trigger to pass into this.
        for widget in self.parent_top_preview_frame.winfo_children(): # Just like in the album, the widgets have to be destroyed in order to create new instances
            widget.destroy() # Destroy the widgets (both the alternate text and the label that holds the image.)
                             # No list this time, giving the variables new data is enough to clear
        selected_label = event.widget # Make the new label equal the label that was clicked on
        selected_path = selected_label.image_path # Make the new file path of the photo equal the file path of the photo that was clicked on
        alt_text = self.db_manager.preview_photo(selected_path) # Call the database to receive the alternate text for this photo, make the search criteria be the file path of the photo since that is the unique identifier in the database for that photo.
        self.show_preview(selected_path, alt_text) # Call the show preview method and pass the selected path that holds the file path, as well as the alternate text to that method for the next step.
        self.db_manager.disconnect() # Disconnect from the database here, otherwise disconnection will have to be made in the database management class before the return statements are sent back here. To prevent the possiblity of that disconnect causing any loss of data, or in other words severing ties before the information is sent back, just close here to be safe.

    # This method is called by on image clicked method above. This method takes the data acquired, and creates the GUI versions of both. 
    # More specifically, it takes the file path of the photo that was clicked on, and the alternate text that the database management class put together, places them into labels, and sends them to the main class. 
    # The parent container that the labels are placed to was sent and initiated in the init portion of this class (parent top preview frame)
    # The alternate text and photo are placed in their own container here together, and then sent to the main class because sending them into the same container individually with the select button would make the button disappear (we destroy widgets, and it got included since it was a child too!), so doing this created a more fluent transfer because the container that exists to receive them are empty.
    def show_preview(self, selected_path, alt_text): # pass self, the selected path, and the alternate text into this method. 
        alt_label = tk.Label(self.parent_top_preview_frame, text=alt_text, bg='teal', fg='white', font=('Verdana', 10, 'bold'), relief='ridge', bd=5, wraplength=400) # Create and style the lable that will hold and display the alternate text
        alt_label.pack(padx=5, pady=5) # Just pack the label, there are only two widgets in the container. Give it a little bit of space. 
        # This section will resize the photo just like the method prior did for the album
        # This is not resizing the same instance of that smaller version, it is still grabbing the photo from the file path of the folder that it sits in.
        # The photo is resized because these are real photos straight from my nikon d7100 camera, which takes professional photos. The original sizes of these photos are substantially too large for this GUI application. 
        img = Image.open(selected_path) # Open the GUI version of the photo file path
        original_width, original_height = img.size # Grab the original sizes of the photo again
        aspect_ratio = original_width / original_height # Use aspect ratio to resize the photo
        new_width = 700 # Declare the new width of the image.
        new_height = int(new_width / aspect_ratio) # Determine the new height of the image based on aspect ratio and the declared width. As mentioned previously, this is to hold the quality of the photo and prevent distortions.
        img_resized = img.resize((new_width, new_height), Image.BILINEAR) # Resize the image with the new width and height. Bilinear is used to resize 2D objects. Since 2 values are used, heigh and width, Bilinear is appropriate.
        photo = ImageTk.PhotoImage(img_resized) # Create the final GUI resized instance of this photo.

        preview_label = tk.Label(self.parent_top_preview_frame, image=photo, bg='gray',relief='sunken', bd='5') # Create and style the label that holds this photo, and place the photo into the label.
        preview_label.image = photo # Create a seperate instance of the photo, to fight against automatic garbage disposal problems.
        preview_label.pack(padx=5, pady=5) # Pack the photo label with a little space, it will automatically place under the alternate text.
