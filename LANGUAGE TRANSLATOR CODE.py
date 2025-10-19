import asyncio
from tkinter import *
import googletrans
from googletrans import Translator
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Initialize the main application window
root = Tk()
root.title('Language Translator')
root.iconbitmap('codemy.ico')  # App icon (Make sure codemy.ico exists)
root.geometry("880x300")  # Set the window size

# App Background Image (Commented Out for Now)
'''bg_image = Image.open(r'images.jpeg')  # Replace with your JPEG file path
bg_image = bg_image.resize((880, 300), Image.ANTIALIAS)  # Resize the image to fit the window size
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = Canvas(root, width=880, height=300)
canvas.pack(fill=BOTH, expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, anchor=NW, image=bg_photo)'''

# Initialize the Translator object from googletrans
translator = Translator()

# Function to translate text asynchronously
async def translate_it_async():
    try:
        # Clear previous translation before inserting new text
        translated_text.delete(1.0, END)

        # Get the source and destination languages from dropdown menus
        from_language = original_combo.get()
        to_language = translated_combo.get()

        # Get corresponding language codes from googletrans dictionary
        from_lang_key = [key for key, value in languages.items() if value == from_language][0]
        to_lang_key = [key for key, value in languages.items() if value == to_language][0]

        # Retrieve input text from the text box and remove extra whitespace
        input_text = original_text.get(1.0, END).strip()

        # Perform asynchronous translation using googletrans
        translated_words = await translator.translate(input_text, src=from_lang_key, dest=to_lang_key)

        # Display the translated text in the output text box
        translated_text.insert(1.0, translated_words.text)

    except Exception as e:
        # Show an error message if translation fails
        messagebox.showerror("Translation Error", str(e))

# Wrapper function to execute async function inside Tkinter event loop
def translate_it():
    loop = asyncio.get_event_loop()  # Get the current event loop
    loop.run_until_complete(translate_it_async())  # Run the async function

# Function to clear both text fields
def clear():
    original_text.delete(1.0, END)
    translated_text.delete(1.0, END)

# Retrieve the language dictionary from googletrans
languages = googletrans.LANGUAGES  # This is a dictionary {code: "Language Name"}
language_list = list(languages.values())  # Convert dictionary values into a list

# Create input text field (where user types original text)
original_text = Text(root, height=10, width=40)
original_text.grid(row=0, column=0, pady=20, padx=10)

# Create the Translate button
translate_button = Button(root, text="Translate!", font=("Helvetica", 24), command=translate_it)
translate_button.grid(row=0, column=1, padx=10)

# Create output text field (where translated text appears)
translated_text = Text(root, height=10, width=40)
translated_text.grid(row=0, column=2, pady=20, padx=10)

# Create dropdown menus for selecting source and target languages
original_combo = ttk.Combobox(root, width=50, value=language_list)
original_combo.current(21)  # Set default language to English
original_combo.grid(row=1, column=0)

translated_combo = ttk.Combobox(root, width=50, value=language_list)
translated_combo.current(26)  # Set default translated language to Spanish
translated_combo.grid(row=1, column=2)

# Create the Clear button to reset text fields
clear_button = Button(root, text="Clear", command=clear)
clear_button.grid(row=2, column=1)

# Start the Tkinter event loop
root.mainloop()