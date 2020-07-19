import gspread
import generator
import uploadWorkout
import telegram_commands
from datetime import datetime
import settings

# Authorise & open the spreadsheet
gc = gspread.oauth()
spreadsheet = gc.open('Workout Generator')

# Retrieve the current workout points target
points_target = int(spreadsheet.worksheet('target').acell('B1').value)

# Get exercises data as a list of lists, drop the first item because it is headers
exercise_weights = spreadsheet.worksheet('weights').get_all_values()[1:]
categories = set([exercise[4] for exercise in exercise_weights])

if __name__ == '__main__':
    print("Hello! Time for a workout!")

    print("The current categories are: {}. Would you like to change the available categories for today's workout?"
          .format(categories))

    change = input('Type Y to change categories else press enter to keep all categories: ')
    # If user wants to exclude categories, loop through every category and give them a Y/N option for each
    if change.lower() == 'y':
        excluded_categories = []
        for cat in categories:
            while True:
                keep = input('{} - Y to keep or N to exclude: '.format(cat))
                if keep.lower() == 'y':
                    break
                elif keep.lower() == 'n':
                    excluded_categories.append(cat)
                    break
                else:
                    print('Not a valid response, try again')
        if len(set(excluded_categories)) == len(categories):
            # If the user has deselected all categories then generate a workout using the full exercise list instead
            print('You have excluded all categories. Generating a workout with all categories instead')
        else:
            categories = categories - set(excluded_categories)
            print("The categories chosen are: {}".format(categories))
    # Select only exercises from the weights list where the 'category' is in the chosen category list
    exercise_weights = [exercise for exercise in exercise_weights if exercise[4] in categories]

    workout, points = generator.generate_workout(points_target, exercise_weights)
    print("Here is your workout, worth {} points:".format(points))
    workout_formatted = generator.format_workout(workout)
    print(workout_formatted)

    log = input('Workout complete, upload and send to Blue? (Type anything to upload + send else press enter)')
    if log != '':
        uploadWorkout.upload_workout(spreadsheet.worksheet('workouts'), workout, points)

        today = datetime.today().strftime('%d/%m/%Y')

        telegram_message = today + '\n Archie did a workout worth {} points'.format(points) + ' consisting of: \n'

        #telegram_commands.telegram_bot_sendtext(telegram_message + workout_formatted, settings.telegram['dark_chat'])
        telegram_commands.telegram_bot_sendtext(telegram_message + workout_formatted, settings.telegram['archie_chat'])

