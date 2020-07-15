import gspread
import generator
import uploadWorkout

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
    print(generator.format_workout(workout))
    uploadWorkout.upload_workout(spreadsheet.worksheet('workouts'), workout, points)
