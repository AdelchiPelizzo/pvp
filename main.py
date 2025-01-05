import tkinter as tk
from tkinter import messagebox
from scraper.fetcher import fetch_html
from scraper.parser import parse_home
from scraper.parser import scrape_multiple_pages
from scraper.saver import save_to_csv, save_to_txt, save_to_excel, save_styled_excel


def on_submit():
    """
    Collect user input from the GUI, build the URL, fetch and scrape data, and save it to a CSV file.
    """
    params = {}
    for key, entry in entries.items():
        value = entry.get().strip()
        if value:
            params[key] = value

    print(params)

    url = f"https://pvp.giustizia.it/pvp/it/lista_annunci.page?searchType=ultimiAnnunci&page=0&size=1000&sortProperty=dataOraVendita,desc&sortAlpha=citta,asc&searchWith=Raggio%20d%27azione&codTipoLotto=IMMOBILI&raggioAzione={params.get('Raggio')}&coordIndirizzo={params.get('Latitudine')},%20{params.get('Longitudine')}"
    print(f"Built URL: {url}")

    # Fetch the HTML content
    try:
        html_content = fetch_html(url)
        print(f"HTML Content Length: {len(html_content)}")  # Check if content is fetched
        with open("debug.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        # Parse the HTML and extract data
        data = parse_home(html_content)
        print(data)
        if data:
            selectors = {
                "description": "span.corpus-s.gui-dettaglio-annuncio-desc-text",
                "Data Vendita": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "Data Pubblicazione": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "Offerta Minima": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "Prezzo Base": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "Superficie": "div.row",
                "Tribunale": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "N° Procedura": "gui-text-tile",
                "Anno Procedura": "gui-text-tile",
                "Tipologia": "div.row",
                "Lotto nr.": "div.gui-text-tile-container.text-regular.corpus-s.align-text-start.flex-column",
                "Indirizzo": "span.title-bold.corpus-l",
            }
            result = scrape_multiple_pages(data, selectors)

            # Save the data to a CSV file
            save_to_csv(result)
            save_to_txt(result)
            save_to_excel(result, "output.xlsx")
            save_styled_excel(result)
            submit_button.config(bg=original_bg, fg=original_fg, text="Recupera")
            messagebox.showinfo("Success", f"Data saved successfully!")
        else:
            messagebox.showwarning("No Data", "No data found in the HTML response.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def on_submit_click():
    """
    Change the Submit button's style temporarily on click, perform the operation, and restore its style.
    """
    # Temporarily change the style
    submit_button.config(bg="lightgray", fg="black", text="Elaborando ...")
    submit_button.update()  # Ensure the changes are immediately visible

    try:
        # Perform the submit action
        on_submit()
    finally:
        # Restore the original style
        submit_button.config(bg=original_bg, fg=original_fg, text="Recupera")


# Create the main application window
root = tk.Tk()
root.title("Auzione")

# Style the root window
root.geometry("270x400")  # Increased height for better spacing
root.configure(bg="#8a90cf")  # Light gray background

# Add padding to the frame and ensure widgets don't overlap
frame = tk.Frame(
    root,
    padx=5,  # Reduced horizontal padding inside the frame
    pady=5,  # Reduced vertical padding inside the frame
    bg="#ffffff",
    relief="groove",
    borderwidth=2
)
frame.pack(pady=30, padx=30, fill="both", expand=True)

# Store the original button style
original_bg = "#3d46a6"  # Green background
original_fg = "white"    # White text

# Add a title label
title_label = tk.Label(
    root,
    text="Aste pvp.giustizia.it",
    font=("Arial", 16, "bold"),
    bg="#8a90cf",
    fg="#d0d1d9"
)
title_label.pack(pady=10)

# Define parameter fields and their default values
fields_with_defaults = {
    "Raggio": "1",  # Default value for 'Raggio'
    "Latitudine": "42.0995997",  # Default latitude (example: Rome, Italy)
    "Longitudine": "14.7191431"  # Default longitude (example: Rome, Italy)
}

entries = {}

# Create input labels and entry fields dynamically with reduced spacing
for field, default_value in fields_with_defaults.items():
    label = tk.Label(
        frame,
        text=field.capitalize(),
        font=("Arial", 10),
        bg="#ffffff",
        anchor="w"
    )
    label.pack(fill="x", pady=(2, 1))  # Reduced space between the label and the field
    entry = tk.Entry(frame, font=("Arial", 12), width=15)  # Keep the fields consistent in size
    entry.insert(0, default_value)  # Set the default value
    entry.pack(pady=8)  # Reduced vertical padding for the entry field
    entries[field] = entry

# Add a Submit button with better spacing and padding
submit_button = tk.Button(
    root,
    text="Recupera",
    font=("Arial", 12, "bold"),
    bg=original_bg,
    fg=original_fg,
    padx=20,  # Increased padding
    pady=10,  # Increased padding
    relief="raised",
    command=on_submit_click
)
submit_button.pack(pady=(5, 20), side="bottom")  # Added extra padding at the bottom

# Run the Tkinter event loop
root.mainloop()
