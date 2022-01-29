import pandas

class AdmissionsData():
    #  Allows for easier common queries against admissions data

    program_abbreviations = {
        'AFM': 'Accounting and Financial Management',
        'FARM': 'Financial Analysis Risk Management',
        'Math': 'Mathematics',
        'Math/BBA': 'Mathematics and Business Administration',
        'BMath/BBA': 'Mathematics and Business Administration',
        'CS': 'Computer Science',
        'CS/BBA': 'Computer Science and Business Administration',
        'CFM': 'Computing and Financial Management',
        'ARBUS': 'Arts and Business',
        'ENBUS': 'Environment and Business',
        'CE': 'Computer Engineering',
        'EE': 'Electrical Engineering',
        'SE': 'Software Engineering',
        'SYDE': 'Systems Design Engineering',
        'Chem Eng': 'Chemical Engineering',
        'Mech Eng': 'Mechanical Engineering',
        'Mechatronics': 'Mechatronics Engineering',
        'Nano': 'Nanotechnology Engineering',
        'Math/CPA': 'Mathematics and Chartered Professional Accountancy',
        'Biotech/CPA': 'Biotechnology and Chartered Professional Accountancy',
    }

    # TODO: Cache creation / singleton this?
    def __init__(self, year: int):
        self.__data = pandas.read_csv("waterloo_%d.csv" % year)

        # Keep only relevant columns
        self.__data = self.__data[ ['Status', 'Program', 'Co-op' 'Grade Percentage', 'Date Accepted', 'Type', 'Other'] ]

    
    def program_data_exists(self, program_name: str) -> bool:
        pass

    def get_program_data(self, program_name: str, *, applicant_type, date_accepted):
        # TODO: Add support for filtering based on other attributes?
        
        # Return High, Low, Number of entries?
        
        pass

    

