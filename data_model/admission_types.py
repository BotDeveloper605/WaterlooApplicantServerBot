from abc import ABC, abstractmethod
from collections import namedtuple
import pandas


SummaryData = namedtuple('SummaryData', ['low', 'high', 'num_applicants'])

class ApplicantField(ABC):

    @classmethod
    @abstractmethod
    def field_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def is_valid(cls, value: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def invalid_hint(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def translate(cls, value: str) -> any:
        pass
    

class GradeAverage(ApplicantField):
    # Percentage grade average in [0, 100]

    @classmethod
    def field_name(cls) -> str:
        return "AVERAGE"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        try:
            num_value = float(value)
            assert(0 <= num_value <= 100)
        except Exception as e:
            return False
        else:
            return True

    @classmethod
    def invalid_hint(cls) -> str:
        return "{field_name}: must be decimal number in range [0, 100]".format(field_name = cls.field_name())

    @classmethod
    def tranlsate(cls, value: str) -> float:
        return float(value)

class ApplicationType(ApplicantField):

    APPLICANT_TYPES = [ '101', '105', '105D', '105F' ]

    @classmethod
    def field_name(cls) -> str:
        return "TYPE"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.APPLICANT_TYPES

    @classmethod
    def invalid_hint(cls) -> str:
        return "{field_name}: must be one of [101, 105, 105D, 105F]".format(field_name = cls.field_name())

    @classmethod
    def translate(cls, value: str) -> str:
        return value


class Program(ApplicantField):

    abbreviations = pandas.read_csv('data_model/abbreviations.csv')
    program_codes = pandas.read_csv('data_model/program_codes.csv')

    @classmethod
    def field_name(cls) -> str:
        return "PROGRAM"

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.program_codes['Code'].unique()

    @classmethod
    def invalid_hint(cls) -> str:
        return "{field_name}: must be a Waterloo OUAC program application code".format(field_name = cls.field_name())

    @classmethod
    def translate(cls, value: str) -> str:
        return value

    @classmethod
    # This will throw if program code not present.. caller's problem
    def get_code_to_long(cls, program_code: str) -> str:
        return cls.program_codes.loc[cls.program_codes['Code'] == program_code, 'Long'].iloc[0]

    @classmethod
    # This will throw if program long not present.. caller's problem
    def get_long_to_code(cls, program_long: str) -> str:
        return cls.program_codes.loc[cls.program_codes['Long'] == program_long, 'Code'].iloc[0]

    @classmethod
    # This will throw if program short (abbreviation) not present.. caller's problem
    def get_short_to_long(cls, program_short: str) -> str:
        return cls.abbreviations.loc[cls.abbreviations['Short'] == program_short, 'Long'].iloc[0]

    @classmethod
    # TODO: Does this really fit the theme of the current class?
    #       - this is turning more into a little data store... not necessarily a wrong direction..
    # Return number of people enrolled in a program, according to OUAC
    def get_enrollment_numbers(cls, program_code: str) -> int:
        return cls.program_codes.loc[cls.program_codes['Code'] == program_code, 'Enrollment'].iloc[0]


if __name__ == "__main__":
    assert(Program.get_enrollment_numbers('WCS') == 345)