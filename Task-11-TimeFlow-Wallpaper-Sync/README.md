# TimeFlow Wallpaper Sync

TimeFlow Wallpaper Sync is a Python application that transforms your desktop wallpaper into a live information dashboard.

It reads content from a user-provided text file and displays it directly on the system wallpaper along with a live clock that updates every second.

The application continuously monitors the text file and automatically updates the wallpaper whenever the file content changes.

---

## Features

-  **Live Clock** – Displays the current time with seconds.
-  **Current Date** – Shows the current day and date.
-  **Text File Sync** – Reads notes, plans, schedules, or reminders from 'notes.txt'.
-  **Automatic File Monitoring** – Detects changes in 'notes.txt' using 'watchdog'.
-  **Dynamic Wallpaper Updates** – Regenerates and applies the wallpaper automatically.
-  **Colorful Dashboard Design** – Gradient background with purple, blue, cyan, and pink accents.
-  **Automatic Text Wrapping** – Long lines are wrapped to fit inside the wallpaper.
-  **Empty File Handling** – Displays a message when the file is empty.
-  **Missing File Handling** – Displays a message when 'notes.txt' is missing.
-  **Ubuntu Integration** – Uses 'gsettings' to automatically apply the generated wallpaper.
-  **Clean Shutdown** – The program can be stopped safely using 'Ctrl + z'.

---

##  Project Structure


Task-11-TimeFlow-Wallpaper-Sync/
main.py
notes.txt
requirements.txt
README.md
.gitignore
wallpaper.png


> 'wallpaper.png' is generated automatically when the program runs.

---

##  Installation

### 1. Clone the repository

git clone <YOUR-REPOSITORY-URL>
cd amfoss-tasks/Task-11-TimeFlow-Wallpaper-Sync


### 2. Create a virtual environment

python3 -m venv venv


### 3. Activate the virtual environment

source venv/bin/activate

### 4. Install dependencies

pip install -r requirements.txt
---

##  Usage

Run the application:

python3 main.py

The program will:

1. Read the content of 'notes.txt'.
2. Generate a colorful wallpaper containing the notes.
3. Display the current time and date.
4. Update the time every second.
5. Monitor 'notes.txt' for changes.
6. Automatically update the wallpaper when the file is modified.

Stop the application using:

Ctrl + z

---

##  Editing Notes

Edit 'notes.txt' while the application is running:

Today's Plan

1. Complete ASK-11
2. Study Python
3. Practice DSA
4. Push the project to GitHub

Save the file.

TimeFlow automatically detects the change and updates the wallpaper.

---

##  Edge Case Handling

### Empty File

If 'notes.txt' is empty, the wallpaper displays:

The file is empty.

### Missing File

If notes.txt does not exist, the wallpaper displays:

File not found: notes.txt

### Long Text

Long lines are automatically wrapped to fit inside the notes panel. If the content exceeds the available vertical space, the remaining content is represented with:

' ... '

---

##  Customization

The wallpaper theme can be customized by changing the RGB color values inside 'main.py'.

For example:

CYAN = (80, 230, 255)
PURPLE = (190, 120, 255)
PINK = (255, 100, 190)

The background gradient can also be changed:

top_color = (18, 12, 45)
middle_color = (42, 25, 85)
bottom_color = (10, 35, 70)

This makes it easy to create different color themes.

---

## Technologies Used

- Python
- Pillow
- watchdog
- GNOME 'gsettings'
- threading
- datetime

---

## Possible Future Improvements

- Automatic startup when the user logs in.
- Multiple wallpaper themes.
- Configurable fonts and text sizes.
- Support for multiple note files.
- Automatic font resizing based on text length.
- Better handling of very large text files.


## Demonstration

Screenshots demonstrating:

- Initial wallpaper generation
- Live clock updates
- Automatic wallpaper update after modifying 'notes.txt'
- Long text handling
- Empty file handling
- Missing file handling

will be added here.

---

##  Author

**Ayush**
