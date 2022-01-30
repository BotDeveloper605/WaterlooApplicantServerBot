import pandas

from data_model.admission_types import SummaryData, Program

class AdmissionsData():
    # AdmissionsData Allows for easier common queries against admissions data

    @classmethod
    def data_years_available(cls):
        return [2021]

    # TODO: Cache creation / singleton this?
    # TODO: protect against bad queries?
    def __init__(self, year: int):
        # Load program data
        self.__data = pandas.read_csv("data/waterloo_%d.csv" % year)

        self.__headers = ['Status', 'Program', 'Co-op', 'Grade Percentage', 'Date Accepted', 'Type', 'Other']

        # Keep only relevant columns
        self.__data = self.__data[self.__headers]

    def __drop_invalid(self, df: pandas.DataFrame) -> pandas.DataFrame:
        if (len(df) == 0):
            # Empty dataframe
            return df

        # Remove Text Grades 
        # .. sorry IB kids.. I'll learn your system one day
        df = df[ df['Grade Percentage'].apply(lambda x: x.replace('.', '', 1).isnumeric()) ].copy()
        df['Grade Percentage'] = df['Grade Percentage'].astype("float")

        # TODO: Condtionally drop no Type, Date Accepted?

        return df

    # Return available summary information for a given program
    def get_program_data(self, program_long: str, *, status: str = None, applicant_type: str = None) -> SummaryData:
        # TODO: Add support for filtering based on other attributes?, kwargs?

        data_slice = self.__data[self.__data['Program'] == program_long]
        data_slice = self.__drop_invalid(data_slice)

        if (status is not None):
            data_slice = data_slice[ data_slice['Status'].str.equals(status) ]

        if (applicant_type is not None):
            data_slice = data_slice[ data_slice['Type'].str.contains(applicant_type) ]

        slice_empty = len(data_slice) == 0

        return SummaryData(
                None if slice_empty else data_slice['Grade Percentage'].min(), 
                None if slice_empty else data_slice['Grade Percentage'].max(),
                len(data_slice))


if __name__ == "__main__":
    admissions_data = AdmissionsData(2021)
    cs_data = admissions_data.get_program_data('Computer Science')
    cs_data2 = admissions_data.get_program_data(Program.get_short_to_long('CS'))

    assert(cs_data == cs_data2)
