from collections import namedtuple
import pandas

SummaryData = namedtuple('SummaryData', ['low', 'high', 'num_applicants'])

class AdmissionsData():
    # AdmissionsData Allows for easier common queries against admissions data

    @classmethod
    def data_years_available(cls):
        return [2021]

    # TODO: Cache creation / singleton this?
    # TODO: protect against bad queries?
    def __init__(self, year: int):
        # Load program data
        self.__data = pandas.read_csv("../data/waterloo_%d.csv" % year)

        self.__headers = ['Status', 'Program', 'Co-op', 'Grade Percentage', 'Date Accepted', 'Type', 'Other']

        # Keep only relevant columns
        self.__data = self.__data[self.__headers]

        # == Load program abbreviations == 
        self.__abbreviations = pandas.read_csv('abbreviations.csv')

        # == Load program codes ==
        self.__program_codes = pandas.read_csv('program_codes.csv')

    # Convert from a short version to the full names
    def __translate_program_name(self, program_name: str) -> str:
        if (program_name in self.__abbreviations['Short'].unique()):
            program_name = self.__abbreviations.loc[self.__abbreviations['Short'] == program_name, 'Long'].iloc[0]
        return program_name

    # Convert from a program code to the full name
    # WARN: This can throw errors when the program code is not found.. handle at caller.
    def translate_program_code(self, program_code: str) -> str:
        return self.__program_codes.loc[self.__program_codes['Code'] == program_code, 'Long'].iloc[0]

    # Convert from a program full name to the program code
    # WARN: This can throw erros when the program name is not found.. handle at the caller
    def get_program_code(self, program_name: str) -> str:
        return self.__program_codes.loc[self.__program_codes['Long'] == program_name, 'Code'].iloc[0]

    # Get program enrollment numbers
    # WARN: This can throw errors when the program code is not found.. handle at caller.
    def enrollment_number_lookup(self, program_code: str) -> int:
        return int(self.__program_codes.loc[self.__program_codes['Code'] == program_code, 'Enrollment'].iloc[0])

    # Check if we have data on a given program
    def program_data_exists(self, program_name: str) -> bool:
        return self.__translate_program_name(program_name) in self.__data['Program'].unique()


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
        program_name = self.__translate_program_name(program_name)

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

    def get_data(self):
        return self.__data

if __name__ == "__main__":
    admissions_data = AdmissionsData(2021)
    cs_data = admissions_data.get_program_data('Computer Science')
    cs_data2 = admissions_data.get_program_data('CS')

    assert(cs_data == cs_data2)
    assert(admissions_data.enrollment_number_lookup('WCS') == 345)
