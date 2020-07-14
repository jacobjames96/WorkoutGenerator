import gspread
import pandas as pd

# Authorise
gc = gspread.oauth()

weights = pd.DataFrame(gc.open('Workout Generator').worksheet('weights').get_all_records())