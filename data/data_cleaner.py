import pandas

data = pandas.read_csv("waterloo_2021.csv")

# Keep only relevant columns
data = data[ ['Status', 'Program', 'Grade Percentage', 'Date Accepted', 'Type', 'Other'] ]


# ======== Clean up the Progam column =====

# TODO: enum this?

# Some people have listed multiple entries.. 
# -> clean by hand (split into multiple entries for each program)


# Solve the longer name to the program
# -> explicit is better than implicit
def solve_program(program_name: str) -> str:
    program_mapping = {
        'AFM': 'Accounting and Financial Management', 
        'ARBUS': 'Arts and Business',
        'Math/BBA': 'Mathematics and Business Administration',
        'BMATH/BBA': 'Mathematics and Business Administration',
        'BM at Waterloo and BBA at Laurier': 'Mathematics and Business Administration',
        'FARM': 'Financial Analysis Risk Management',
        'farm': 'Financial Analysis Risk Management',
        

    }


    return program_name
