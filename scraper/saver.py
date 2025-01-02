import csv


def save_to_csv(data, filename="output.csv"):
    """
    Save the extracted data to a CSV file.

    :param data: A list of dictionaries containing scraped data.
    :param filename: The output CSV file name.
    """
    try:
        # Open the file in write mode with newline='' to avoid extra lines in Windows
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys(), quoting=csv.QUOTE_ALL)
            writer.writeheader()  # Write header row
            writer.writerows(data)  # Write the rows

        print(f"Data saved successfully to {filename}")

    except Exception as e:
        print(f"Error saving data to CSV: {e}")


def save_to_txt(data, filename="output.txt"):
    """
    Save the scraped data to a text file in a readable format.

    :param data: List of dictionaries containing scraped data.
    :param filename: Name of the output text file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as txtfile:
            for value in data:
                txtfile.write("=== Entry ===\n")
                txtfile.write(f"{value}\n")
                txtfile.write("\n")  # Add a blank line between entries
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to text file: {e}")
