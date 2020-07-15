import gspread
from datetime import date
from gspread.exceptions import CellNotFound
import generator

gc = gspread.oauth()

spreadsheet = gc.open('Workout Generator')
exercises = spreadsheet.worksheet('weights').col_values(1)[1:]
workouts = spreadsheet.worksheet('workouts')

# Establish the current max dimensions of the workouts sheet
max_row = len(workouts.col_values(1))


def find_or_create_col(sheet, search_string):
    # Search for the string in the first row of the sheet and return the col number
    try:
        col_num = sheet.find(search_string, 1).col
    except CellNotFound:
        # If there are no matches this exercise doesn't exist in the workouts sheet so create it at the right most cell
        max_col = len(sheet.row_values(1))
        sheet.update_cell(1, max_col + 1, search_string)
        col_num = max_col + 1
    return int(col_num)


def upload_workout(sheet, workout, points):
    # Get max row for sheet + 1
    row = len(sheet.col_values(1)) + 1
    today = date.today().strftime('%d/%m/%Y')

    sheet.update_cell(row, 1, today)  # Add in today's date
    sheet.update_cell(row, 2, points)  # Add in the points total

    # Loop through the workout an update the relevant columns
    for ex in workout:
        col = find_or_create_col(sheet, ex)
        sheet.update_cell(row, col, workout[ex][0])


sample_workout, sample_points = generator.generate_workout(100, spreadsheet.worksheet('weights').get_all_values()[1:])

upload_workout(workouts, sample_workout, sample_points)