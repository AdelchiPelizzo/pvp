import csv
import xlsxwriter
from datetime import datetime
from xlsxwriter import Workbook

def save_styled_excel(data):
    if not data:
        print("No data to save to Excel.")
        return

    # Create a new Excel file and add a worksheet
    workbook = xlsxwriter.Workbook('styled_output.xlsx')
    worksheet = workbook.add_worksheet()

    # Define some formats
    bold_format = workbook.add_format({'bold': True})
    date_format_with_time = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm'})  # Include time for Data Vendita
    date_format_without_time = workbook.add_format({'num_format': 'dd/mm/yyyy'})  # Only date for Data Pubblicazione
    currency_format = workbook.add_format({'num_format': '€#,##0.00'})
    text_wrap_format = workbook.add_format({'text_wrap': True})
    general_format = workbook.add_format({'border': 1})

    # Set column widths for readability
    worksheet.set_column('A:A', 10)  # ID
    worksheet.set_column('B:B', 50)  # URL
    worksheet.set_column('C:C', 70)  # Description
    worksheet.set_column('D:D', 15)  # Data Vendita
    worksheet.set_column('E:E', 15)  # Data Pubblicazione
    worksheet.set_column('F:F', 15)  # Offerta Minima
    worksheet.set_column('G:G', 15)  # Prezzo Base
    worksheet.set_column('H:H', 10)  # Superficie
    worksheet.set_column('I:I', 20)  # Tribunale
    worksheet.set_column('J:J', 15)  # N° Procedura
    worksheet.set_column('K:K', 15)  # Anno Procedura
    worksheet.set_column('L:L', 20)  # Tipologia
    worksheet.set_column('M:M', 15)  # Lotto nr.
    worksheet.set_column('N:N', 50)  # Indirizzo

    # Write headers
    headers = list(data[0].keys())
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, bold_format)

    # Write data rows
    for row_idx, item in enumerate(data, start=1):
        for col_idx, key in enumerate(headers):
            value = item.get(key)

            # Apply formatting based on column type
            if key == 'Data Vendita' and value:
                try:
                    date_value = _convert_to_date(value, with_time=True)  # Convert to datetime with time
                    worksheet.write_datetime(row_idx, col_idx, date_value, date_format_with_time)
                except Exception as e:
                    print(f"Error formatting date '{value}' in row {row_idx}, column {col_idx}: {e}")
                    worksheet.write(row_idx, col_idx, value, general_format)

            elif key == 'Data Pubblicazione' and value:
                try:
                    date_value = _convert_to_date(value, with_time=False)  # Convert to datetime without time
                    worksheet.write_datetime(row_idx, col_idx, date_value, date_format_without_time)
                except Exception as e:
                    print(f"Error formatting date '{value}' in row {row_idx}, column {col_idx}: {e}")
                    worksheet.write(row_idx, col_idx, value, general_format)

            elif key in ['Offerta Minima', 'Prezzo Base'] and value:
                try:
                    worksheet.write_number(row_idx, col_idx, _convert_to_number(value), currency_format)
                except Exception as e:
                    print(f"Error formatting number '{value}' in row {row_idx}, column {col_idx}: {e}")
                    worksheet.write(row_idx, col_idx, value, general_format)

            elif key == 'description' and value:
                worksheet.write(row_idx, col_idx, value, text_wrap_format)
            else:
                worksheet.write(row_idx, col_idx, value if value else "", general_format)

    # Add a filter to make sorting easier in Excel (Optional)
    worksheet.autofilter(0, 0, len(data), len(headers) - 1)

    # Close the workbook to save the file
    workbook.close()

    print("Excel file with styling has been saved.")

def _convert_to_date(date_string, with_time=True):
    """
    Convert date string to datetime object.
    If 'with_time' is True, expects a time string; otherwise, it assumes no time is included.
    """
    try:
        if with_time:
            # Parse datetime with time
            return datetime.strptime(date_string, "%d/%m/%Y %H:%M")
        else:
            # Parse date without time
            return datetime.strptime(date_string, "%d/%m/%Y")
    except ValueError as e:
        print(f"Error converting date '{date_string}': {e}")
        return None

# Helper function to convert currency strings to float
def _convert_to_number(currency_str):
    return float(currency_str.replace('.', '').replace(',', '.').replace(' €', '')) if currency_str else 0.0


# Example data call
data = [# Include your provided data here as a list of dictionaries
]

save_styled_excel(data)


def save_to_excel(data, filename="output.xlsx"):
    """
    Save the extracted data to an Excel file.

    :param data: A list of dictionaries containing scraped data.
    :param filename: The output Excel file name.
    """
    try:
        # Validate the input
        if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
            raise ValueError("Data must be a list of dictionaries.")

        # Create a new Excel file and add a worksheet
        workbook = Workbook(filename)
        worksheet = workbook.add_worksheet()

        # Write the header (keys from the first dictionary)
        headers = data[0].keys()
        for col_idx, header in enumerate(headers):
            worksheet.write(0, col_idx, header)

        # Write the data rows
        for row_idx, row in enumerate(data, start=1):
            for col_idx, header in enumerate(headers):
                worksheet.write(row_idx, col_idx, row.get(header, ""))

        workbook.close()
        print(f"Data saved successfully to {filename}")

    except ValueError as ve:
        print(f"Input Error: {ve}")

    except Exception as e:
        print(f"Error saving data to Excel: {e}")


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
