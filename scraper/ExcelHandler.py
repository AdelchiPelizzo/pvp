import csv
from xlsxwriter import Workbook

# Open CSV file
with open("data.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file)

    # Create a new Excel file
    workbook = Workbook("output.xlsx")
    worksheet = workbook.add_worksheet()

    # Write rows from CSV to Excel
    for row_idx, row in enumerate(csv_reader):
        for col_idx, cell in enumerate(row):
            worksheet.write(row_idx, col_idx, cell)

    workbook.close()
