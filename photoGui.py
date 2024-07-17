import tkinter as tk
from tkinter import Scrollbar, Frame
from PIL import Image, ImageTk
import sqlite3
from math import *

# Global variables
displayPhotos = []
photoLabels = []
photoReferences = []

# Function to find and display photos based on user input tags
def findPhotos():
    global displayPhotos
    displayPhotos.clear()  # Clear previous search results
    
    # Connect to SQLite database
    conn = sqlite3.connect('metaData.db')
    cursor = conn.cursor()
    
    # Get input tags from the entry widget
    tagID = tagEntry.get().lower().strip().split(",")
    
    # Search SQL query based on tags
    query = "SELECT imagePath FROM photos WHERE "
    conditions = []
    for tag in tagID:
        conditions.append(f"RiderName LIKE '%{tag}%' OR RiderNumber LIKE '%{tag}%' OR Date LIKE '%{tag}%' OR Series LIKE '%{tag}%' OR Class LIKE '%{tag}%' OR BikeColor LIKE '%{tag}%' OR NamePlateColor LIKE '%{tag}%'")
    query += " OR ".join(conditions)
    
    # Execute query
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    # Populate displayPhotos with image paths from database query
    for row in rows:
        displayPhotos.append(row[0])
    
    # Call function to load and display matched photos
    loadDisplayPhotos()

# Function to load the photos
def loadDisplayPhotos():
    global displayPhotos, photoReferences, photoLabels
    
    # Clear previous photos and their references
    for label in photoLabels:
        label.destroy()
    photoLabels.clear()
    photoReferences.clear()
    
    numPhotos = len(displayPhotos)
    numRows = ceil(numPhotos/3)
    c = 0
    r = 0
    for imagePath in displayPhotos:
        try:
            img = Image.open(imagePath)
            # Resize while maintaining aspect ratio
            originalWidth, originalHeight = img.size
            aspectRatio = originalWidth / originalHeight
            newWidth = 100  # Fixed width for each photo
            newHeight = int(newWidth / aspectRatio)
            imgResized = img.resize((newWidth, newHeight), Image.BILINEAR)
            photo = ImageTk.PhotoImage(imgResized)

            #configure the columns
            displayAlbum.columnconfigure(c, weight=1)
            displayAlbum.rowconfigure(numRows, weight=1)
            
            # Create Button for displaying the photo
            label = tk.Label(displayAlbum, image=photo, borderwidth=1)
            label.grid(padx=1, pady=1, column=c, row=r)
            label.image = photo  # Keep a reference to the PhotoImage
            label.imagePath = imagePath # Store imagePath as a custom attribute for later usage, such as onImageClicked event.
            photoReferences.append(photo)  # Store the PhotoImage reference
            
            # Bind click event to handle image selection
            label.bind("<ButtonRelease-1>", onImageClicked)
            
            photoLabels.append(label)  # Store label in list to prevent garbage collection
            
            # Adjust grid layout counters
            c += 1
            if c >= 3:
                c = 0
                r += 1

        except Exception as e:
            print(f"Error loading {imagePath}: {e}")


# Function to handle image selection event
def onImageClicked(event):
    try:
        # Clear any previous content in the previewFrame
        for widget in topPreviewFrame.winfo_children():
            widget.destroy()

        # Get the clicked label widget and its associated image
        selectedLabel = event.widget
        selectedImage = selectedLabel.image
        
        # Fetch the imagePath from the label's tag attribute
        imagePath = selectedLabel.imagePath
        
        # Connect to SQLite database
        conn = sqlite3.connect('metaData.db')
        cursor = conn.cursor()

        # Query to fetch metadata based on imagePath
        query = "SELECT RiderName, RiderNumber, Series, Class, BikeColor, Date FROM photos WHERE imagePath = ?"
        cursor.execute(query, (imagePath,))
        row = cursor.fetchone()
        
        # Extract metadata values
        riderName = row[0]
        riderNumber = row[1]
        series = row[2]
        class_ = row[3]
        bikeColor = row[4]
        date = row[5]

        # Determine alt text based on available metadata
        if riderName:
            altText = f"Image shows Rider {riderName}, racing {class_} class at {series} on {date}."
        elif riderNumber:
            altText = f"Image shows unidentified rider on their {bikeColor} bike and rider number {riderNumber} racing at {series} on {date}."
        else:
            altText = f"Image shows unidentified rider on their {bikeColor} bike racing at {series} on {date}."

        # Display altText in previewFrame
        altLabel = tk.Label(topPreviewFrame, text=altText)
        altLabel.pack(padx=10, pady=10)

        # Load and display the clicked image in previewFrame
        img = Image.open(imagePath)
        # Resize while maintaining aspect ratio
        originalWidth, originalHeight = img.size
        aspectRatio = originalWidth / originalHeight
        newWidth = 700  # Fixed width for each photo
        newHeight = int(newWidth / aspectRatio)
        imgResized = img.resize((newWidth, newHeight), Image.BILINEAR)
        photo = ImageTk.PhotoImage(imgResized)
            
        # Create Label for displaying the photo
        previewLabel = tk.Label(topPreviewFrame, image=photo)
        previewLabel.image = photo  # Keep a reference to the PhotoImage
        previewLabel.pack(padx=10, pady=10, side='top')

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error handling image click: {e}")


# Open the editing window function
def openEdit():
    # Create the editing window
    editWin = tk.Toplevel(window)
    editWin.geometry("1000x1000")
    editWin.title("Photo Editing")


# GUI code begins
window = tk.Tk()
window.geometry("1000x600")
window.title("Photo Search and Display")

# Main frame
mainWin = tk.PanedWindow(window, bg="light blue")
mainWin.pack(fill="both", expand=1)

# Photo search frame for related widgets
photoSearchFrame = tk.Frame(mainWin, width=300, height=600)
photoSearchFrame.pack(side="left")
mainWin.add(photoSearchFrame)

# Tag labels and entry
NewUserSearchLabel = tk.Label(photoSearchFrame, text="NEW USERS: Narrow your search by entering date, series, bike or nameplate color", bg="light blue", wraplength=200)
ReturnUserSearchLabel = tk.Label(photoSearchFrame, text="RETURNING USERS: Rider name can be used to narrow search.", bg="light blue", wraplength=200)
infoTagLabel = tk.Label(photoSearchFrame, text="Separate keywords with a comma or space", bg="light blue", wraplength=200)
tagEntry = tk.Entry(photoSearchFrame)
searchButton = tk.Button(photoSearchFrame, text="Search Photos", command=findPhotos)

NewUserSearchLabel.pack(pady=5, padx=3, fill="x")
ReturnUserSearchLabel.pack(padx=3, pady=5, fill="x")
infoTagLabel.pack(padx=3, pady=5, fill="x")
tagEntry.pack(padx=3, pady=5, fill="x")
searchButton.pack(padx=3, pady=5, fill="x")

#Create A Canvas
canvas = tk.Canvas(photoSearchFrame)
canvas.pack(side='top', fill='y')

#Add A Scrollbar to the Canvas
scrollbar = Scrollbar(canvas, orient='vertical', command=canvas.yview, scrollregion=canvas.bbox("all"))
scrollbar.pack(side='right', fill='y')
#Configure Canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>')
#Create another Frame inside the Canvas
displayAlbum = tk.Frame(canvas)
displayAlbum.pack(side='left')

# Preview frame (for an enlarged preview)
previewFrame = tk.Frame(mainWin, bg="white", width=900, height=700, padx=1, pady=1)
previewFrame.pack(side='right')
mainWin.add(previewFrame)

#Button to call new view
#create container first to hold photo so it doesn't disable the button
topPreviewFrame=tk.Frame(previewFrame)
topPreviewFrame.pack(side='top')
choosePhotoButton = tk.Button(previewFrame, text="Select", command=openEdit)
choosePhotoButton.pack(side='bottom')

# Start GUI
window.mainloop()
