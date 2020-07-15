import gspread
import random
import math

# Authorise & open the spreadsheet
gc = gspread.oauth()
spreadsheet = gc.open('Workout Generator')

# Retrieve the current workout points target
points_target = int(spreadsheet.worksheet('target').acell('B1').value)

# Get exercises data as a list of lists, drop the first item because it is headers
exercise_weights = spreadsheet.worksheet('weights').get_all_values()
exercise_weights.pop(0)

# Randomise the list of exercises (without specifying a seed to get a different shuffle every time)


def generate_workout(points_target, exercise_weights):
    workout = {}

    num_exercises = len(exercise_weights)
    # Shuffle the list of exercises to make sure exercises are varied each time this is run
    random.shuffle(exercise_weights)

    points_total = 0
    # Set the counter for the loop equal to the number of exercises, so we can start on the first exercise
    # (by taking modulo num_exercises)
    counter = num_exercises
    while points_total < points_target:
        #TODO: Randomise the exercise list every time to avoid bias towards the first exercise

        # Get the next exercise details, update the type of the number variables
        name, value, exercise_type, min_reps = exercise_weights[counter % num_exercises]
        value = float(value)
        min_reps = int(min_reps)

        # Choose a random number of "reps" to do (between 1 and 3) and multiply this by the minimum number
        # of reps to do for this exercise
        reps = random.randint(1, 3) * int(min_reps)

        # Calculate the points contribution by multiplying the reps by the 'per rep point value'
        exercise_points = reps * float(value)

        # Check if this exercise will take us over the points threshold - if so do the minimum number of repetitions
        # necessary. For example if we are currently at 85/100 points and this is an exercise worth 1 point per rep
        # and a minimum of 10 reps per exercise, we need to do 20 reps (2 repetitions) to beat the 100 target
        if points_total + exercise_points > points_target:
            # Current points gap divided by per rep value, ceiling divided by the minimum reps to get a number
            # of repetitions, finally multiplied by the minimum repetitions to get total repetitions
            reps = math.ceil(((points_target - points_total) / float(value)) / int(min_reps)) * int(min_reps)
            exercise_points = reps * float(value)

        # Log the exercise and number of reps (updating the number of reps if we have already added it to the workout)
        # TODO Better formatting of the output string to incorporate what type of exercise it is
        if name in workout:
            workout[name][0] += reps
        else:
            workout[name] = [reps, exercise_type]

        points_total += exercise_points
        counter += 1

    #TODO Output the workout to Google sheets? This could maybe be done elsewhere.
    return workout, points_total


for i in range(10):
    workout, points = generate_workout(points_target, exercise_weights)
    print(workout)
    print(points)