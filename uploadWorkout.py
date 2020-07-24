from datetime import date
from gspread.exceptions import CellNotFound
import gspread


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


def upload_workout(workout, points):
    gc = gspread.oauth()
    spreadsheet = gc.open('Workout Generator')
    sheet = spreadsheet.worksheet('workouts')

    # Get max row for sheet + 1
    row = len(sheet.col_values(1)) + 1
    today = date.today().strftime('%d/%m/%Y')

    # TODO: Make this more concise, use one update statement for these two lines
    sheet.update_cell(row, 1, today)  # Add in today's date
    sheet.update_cell(row, 2, points)  # Add in the points total

    # Loop through the workout an update the relevant columns
    for ex in workout:
        col = find_or_create_col(sheet, ex)
        sheet.update_cell(row, col, workout[ex][0])
