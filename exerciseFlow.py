import gspread
import generator
import uploadWorkout
import telegram_commands
from datetime import datetime

# Authorise & open the spreadsheet
gc = gspread.oauth()
spreadsheet = gc.open('Workout Generator')

# Retrieve the current workout points target
points_target = int(spreadsheet.worksheet('target').acell('B1').value)

# Get exercises data as a list of lists, drop the first item because it is headers
exercise_weights = spreadsheet.worksheet('weights').get_all_values()[1:]


if __name__ == '__main__':
    print("Hello! Time for a workout!")
    workout, points = generator.generate_workout(points_target, exercise_weights)
    print("Here is your workout, worth {} points:".format(points))
    workout_formatted = generator.format_workout(workout)
    print(workout_formatted)
    uploadWorkout.upload_workout(spreadsheet.worksheet('workouts'), workout, points)

    today = datetime.today().strftime('%d/%m/%Y')

    telegram_message = today + '\n Archie did a workout worth {} points'.format(points) + ' consisting of: \n'

    telegram_commands.telegram_bot_sendtext(telegram_message + workout_formatted)

