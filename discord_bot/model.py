from collections import namedtuple
import pandas

SummaryData = namedtuple('SummaryData', ['low', 'high', 'num_applicants'])

class AdmissionsData():
    # Allows for easier common queries against admissions data

    # Allow for common short-hands
    __program_abbreviations = {
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

    @classmethod
    def data_years_available(cls):
        return [2021]

    # TODO: Cache creation / singleton this?
    # TODO: protect against bad queries?
    def __init__(self, year: int):
        self.__data = pandas.read_csv("../data/waterloo_%d.csv" % year)

        self.__headers = ['Status', 'Program', 'Co-op', 'Grade Percentage', 'Date Accepted', 'Type', 'Other']

        # Keep only relevant columns
        self.__data = self.__data[self.__headers]


    # Check if we have data on a given program
    def program_data_exists(self, program_name: str) -> bool:
        return self.__program_abbreviations.get(program_name, program_name) in self.__data['Program'].unique()


    def __drop_invalid(self, df: pandas.DataFrame) -> pandas.DataFrame:

        # Remove Text Grades 
        # .. sorry IB kids.. I'll learn your system one day
        df = df[ df['Grade Percentage'].apply(lambda x: x.isnumeric()) ].copy()
        df['Grade Percentage'] = df['Grade Percentage'].astype("float")

        # TODO: Condtionally drop no Type, Date Accepted?

        return df


    # Return available summary information for a given program
    def get_program_data(self, program_name: str, *, status: str = None, applicant_type: str = None) -> SummaryData:
        # TODO: Add support for filtering based on other attributes?
        program_name = self.__program_abbreviations.get(program_name, program_name)

        data_slice = self.__data[self.__data['Program'] == program_name]
        data_slice = self.__drop_invalid(data_slice)

        if (status is not None):
            data_slice = data_slice[ data_slice['Status'].str.equals(status) ]

        if (applicant_type is not None):
            data_slice = data_slice[ data_slice['Type'].str.contains(applicant_type) ]

        return SummaryData(
                data_slice['Grade Percentage'].min(), 
                data_slice['Grade Percentage'].max(),
                len(data_slice['Grade Percentage']))

    # For testing
    def get_data(self):
        return self.__data


if __name__ == "__main__":
    admissions_data = AdmissionsData(2021)
    cs_data = admissions_data.get_program_data('Computer Science')
