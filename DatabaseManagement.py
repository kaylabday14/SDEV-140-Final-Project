"""
Kayla Day
SDEV 140 Final Project
July 28, 2024
This part of the program is the database manager. It connects to the database, sends commands to the database, and then disconnects from the database.
"""
# Import statements section
import sqlite3 as sq # this import is required for the database, it imports SQLite 

# Database Manager class holds all logic required to retrieve the information related to photos for this program.
class DatabaseManagement:
    # Define the attributes that this class holds.
    def __init__(self, db_name='metaData.db'): 
        self.db_name = db_name # Define the file name for the database so that the database can be found. File is in same folder as program files
        self.con = None # initiate variable for connection, define as none in this method because it does not need to be defined yet.

    # Connection method, this allows connection to the database from other methods as well as by other classes
    def connect(self):
        self.con = sq.connect(self.db_name) # This makes con equal connected, when this line runs, the database connection is on

    # Disconnection method, this allows disconnection from the database from other methods as well as by other classes
    def disconnect(self):
        if self.con: # First make sure that con is true, because if so, con is connected to the database. If not, there is no reason to have to disconnect from the database
            self.con.close() # This line disconnects from the database

    # This section connects to the database during the intial "find photos" phase among the main and photo display classes.
    # This runs as soon as the user presses search, before any photos have been loaded.
    # Tags that have been entered, to narrow the search are sent here, then they are compared within the database table.
    # For any matches found, the filepath names of the photos are returned to the Photo Display class.
    # If there was nothing entered, all of the filepath names for the photos in the database will be returned to Photo Display.
    # The purpose of this section is to allow the entire photo album to be displayed, or to narrow down the amount of photos that are displayed for faster searches.
    # The users would most likely be looking for a specific rider, not wanting to just view my photographs.
    # Note that the use of multiple keywords does not further narrow down the search but instead adds to it. This is because currently the only names I know are my husband's, bonus son's, and our family/friends. Users who are likely to use this would want to enter a number with a color, because if the number wasn't visible, adding a bike color or series name will ensure that they don't miss out on seeing a photo. 
    def find_photos(self, tag): # Pass the tag names into this method
        self.connect() # Connect to the database
        self.cursor = self.con.cursor() # Initiates a cursor variable and connects built in cursor function
        
        display_photos = [] # Create an empty list to hold results of the image file paths

        try:
            tag_id = tag.lower().strip().split(",") # Format what the user entered to stop any capitalization, whitespace, and split words by commas if the user entered more than one word.
            conditions = [] # Create an empty conditions list for command statements with the tags
            for tag in tag_id: # Cycle through all possible tags incase the user typed more than one
                # Line Below: This is formating the command of search criteria with the tag entered. This will allow the value of tag to be compared to every column in the database table
                conditions.append(f"RiderName LIKE '%{tag}%' OR RiderNumber LIKE '%{tag}%' OR Date LIKE '%{tag}%' OR Series LIKE '%{tag}%' OR Class LIKE '%{tag}%' OR BikeColor LIKE '%{tag}%' OR NamePlateColor LIKE '%{tag}%'")
            
            query = "SELECT imagePath FROM photos WHERE " + " OR ".join(conditions) # This defines the command line to select the value of imagePath and joins it with each line stored in the commands list. This makes query equal the entire statement to be exectuted.
            self.cursor.execute(query) # Exectute the query statement
            rows = self.cursor.fetchall() # Retrieve every result (image path) that matches the conditions. Rows is the variable used because the database table is set up so that every row "describes" or "belongs to" that one photo. Any variable could have been used, but it helps clarify how the table is set up.

            for row in rows: # cycle through the values in list rows
                display_photos.append(row[0]) # Add only the first column of each row, because the first column of each row is where the image path is stored
        # Account for any errors that may happen when trying to execute the above
        except sq.Error as e: 
            print(f"Error executing query: {e}") # Print this error for debugging. It will let you know that the error was during exectution, as well as where the error happened.
        # Once execution is finished, or an error has been sent for debugging, the connection to the cursor and database need to be closed.
        finally:
            self.cursor.close() # This closes the connection to the cursor which is how we manipulate the database
            self.disconnect() # This closes the connecton to the database
            return display_photos # return the list of image paths for the photos (returns to PhotoDisplay class)

    # This section connects to the database to find the specific tags based on the photo that was clicked.
    # This runs as a result of On Image Clicked event which so more defined and called from the PhotoDisplay class.
    # When the user clicks on a photo, a larger version of that photo is displayed, the image path is sent here to be used to retrieve all data from the row in relation to that photo (image path)
    # The purpose of this section is to create the alternate text and make it personalized and descriptive of that selected photo.
    def preview_photo(self, selected_path):
        self.connect() # Connect to the database 
        if not self.con: # Check to see if the connection was successful
            self.con = sq.connect(self.db_name) # If the connection was not successful through calling the connect method, this will make a new attempt by directly calling the built in method. This was placed because clicking on a new photo to pull a different image and alternate text was causing hiccups in connection. This gives a second chance to make that connection.
        self.cursor = self.con.cursor() # Connect to the cursor needed to make executions
        query = "SELECT RiderName, RiderNumber, Series, Class, BikeColor, Date FROM photos WHERE imagePath = ?" # Make query equal the command statement. What this statement does is collect every value from the row where the the mathing image path is found.
        self.cursor.execute(query, (selected_path,)) # Execute the command using both the query line and the image path that is in selected_path.
        column = self.cursor.fetchone() # Place the results into column list. Only one row in the database will match, so only one row is retrieved instead of all, but each column in that row is going to be entered into that list

        # This seperates the results in the column list and makes it equal to a variable name that describes what the element of that index is. 
        # The variable names represent what the values mean or represent. 
        if column:
            # Note that this is the set up of the table - 1 column. Image paths are actually in column 0, but in this case image paths weren't added to the list. 
            # So for example, in the database table, the rider name for that photo is actually in column 1 not column 0.
            rider_name = column[0] 
            rider_number = column[1]
            series = column[2]
            class_ = column[3]
            bike_color = column[4]
            date = column[5]
            # Some values a null in the database table, that is because not every rider name is stored or otherwise "known"
            # Other values that could be null are rider number and class, an unknown rider generally means unknown class as well, and if the number is not able to be seen, then rider number is going to be null as well.
            # The purpose of this section  not only personalizes the alternate text, but allows different descriptors in the alternate text for when very personalized keys, such as rider name, are not stored.
            # The way that the alternate text is written also provides a signal to the user that I do not know this information.
            # The reason of this signal is something I will be building upon, that isn't in the current program. For now, if a user sees that clearly visible rider numbers are mentioned, they may use that search criteria to narrow their search.
            if rider_name: # If the rider name is not null, then I will know what class they were in for this series and date of the photo
                alt_text = f"Image shows Rider {rider_name}, racing {class_} class at {series} on {date}." # use this alternate text.
            elif rider_number: # If the rider name is null, try the rider number, which is another specific descriptor. Add bike color with it, both of these give visual descriptors with the series and date.
                alt_text = f"Image shows unidentified rider on their {bike_color} bike and rider number {rider_number} racing at {series} on {date}." # use this alternate text.
            else: # If the rider name is unknown, and there is no rider number seen, the only descriptors available will be the bike color with the series and date.
                alt_text = f"Image shows unidentified rider on their {bike_color} bike racing at {series} on {date}." # Use this alternate text for these cases.
            
            return alt_text # Returns the alternate text to PhotoDisplay class so that it can be displayed with the selected photo.
        return None, None # The actual column list nor the selected path need to be returned, but none is written twice because two more returns are expected (3 total).
        # Disconnects from the database in PhotoDisplay class, under on_image_clicked method.
    
    
    
   