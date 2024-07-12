import tkinter as tk
from PIL import ImageTk, Image
import sqlite3

#global variables
displayPhotos = []

# Function to find and display photos based on user input tags
# Need to work on this function further, it works, but multiple keywords doesn't narrow it down further, you can see in print statements that it does search all the tags, but adds to the list when it finds one tag instead. 
# Keep testing with Taylor, stoney. (right now IXCR photos will show up also)
# Want to also 
def findPhotos():
    
    # Connect to SQLite database
    conn = sqlite3.connect('metaData.db') # Connects the database
    cursor = conn.cursor() # Cursor for database
    
    # Get input tags from the entry widget
    tagID = tagEntry.get().lower().strip().split(",") # Change the input and seperate multiple key words
    
    # Search SQL query based on tags
    query = "SELECT imagePath FROM photos WHERE " # Command to query, this will return the file name from the photos table in database
    conditions = [] # Place the tag names that the user entered into a list
    for tag in tagID: # Cycle through each tag
        # Compare tag(s) to each value in the columns of the table in database and add to the list
        conditions.append(f"RiderName LIKE '%{tag}%' OR RiderNumber LIKE '%{tag}%' OR Date LIKE '%{tag}%' OR Series LIKE '%{tag}%' OR Class LIKE '%{tag}%' OR BikeColor LIKE '%{tag}%' OR NamePlateColor LIKE '%{tag}%'") 
        print("conditions after append", conditions) # Temporary check
    query += " OR ".join(conditions)
    print("conditions after join:", conditions) # Temporary check
    # Execute the commands above
    cursor.execute(query)
    rows = cursor.fetchall() # function to collect the results of each imagePath. This is because each new row is a new image, and the columns in that row are it's personalized tags. 
    print("rows:", rows) # Temporary check
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    # Populate displayPhotos with image paths from database query
    for row in rows: 
        displayPhotos.append(row[0])
    
    # Call the function to load and display matched photos
    loadDisplayPhotos()

#function to load the photos
def loadDisplayPhotos():
    global displayPhotos
    
    # Clear previous photos and their references
    for label in photoLabels:
        label.destroy()
    
    # Iterate through each photo in list of found photos
    for imagePath in displayPhotos:
        i = 0
        try:
            img = Image.open(imagePath)  # Open the image
            # Resize while maintaining aspect ratio
            originalWidth, originalHeight = img.size
            aspectRatio = originalWidth / originalHeight
            newWidth = 600  # Fixed width for each photo
            newHeight = int(newWidth / aspectRatio)
            imgResized = img.resize((newWidth, newHeight))  # Resize image
            photo = ImageTk.PhotoImage(imgResized)  # Convert to PhotoImage
            
            # Create Label for displaying the photo
            label = tk.Label(photoDisplayFrame, image=photo)
            label.pack(padx = 3, pady = 3, side = "left")
            label.image = photo  # Keep a reference to the PhotoImage
            
            # Bind click event to handle image selection
            label.bind("<ButtonRelease-1>", onImageClicked)
            
            photoLabels.append(label)  # Store label in list to prevent garbage collection
            
        except Exception as e: # If the photo does not load, run this instead. 
            print(f"Error loading {imagePath}: {e}") # Probably will change later, to display as alternate text.

# Function to handle image selection event
def onImageClicked(event): # This is referring to the image that the user clicks after they have been loaded
     # Grab the location of the selected photo here, grab by index, it should display in the order of the list, so we can get location in relation to the list
    if index < len(displayPhotos): # Prevent out of bounds errors 
        selectedImage = displayPhotos[index] # Grab file name (imagePath)
        # Add future code here to raise the next frame for editing


# GUI code begins
window = tk.Tk()
window.title("Photo Search and Display")

# Photo search frame for related widgets
photoSearchFrame = tk.Frame(window)
photoSearchFrame.pack(side="top", padx=10, pady=10)

# Tag labels and entry
NewUserSearchLabel = tk.Label(photoSearchFrame, text="NEW USERS: Narrow your search by entering keywords...")
ReturnUserSearchLabel = tk.Label(photoSearchFrame, text="RETURNING USERS: Search by first and last name, rider number...")
infoTagLabel = tk.Label(photoSearchFrame, text="Separate keywords with a comma or space")
NewUserSearchLabel.pack()
ReturnUserSearchLabel.pack()
infoTagLabel.pack()

# Entry for tags
tagEntry = tk.Entry(photoSearchFrame)
tagEntry.pack()

# Button to initiate photo search
searchButton = tk.Button(photoSearchFrame, text="Search Photos", command=findPhotos)
searchButton.pack()

# Photo display frame
photoDisplayFrame = tk.Frame(window)
photoDisplayFrame.pack(side="bottom")

# Store the loaded PhotoImage objects to prevent garbage collection
photoLabels = []

window.mainloop()
