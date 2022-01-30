from abc import ABC, abstractmethod
from collections import namedtuple
import pandas


SummaryData = namedtuple('SummaryData', ['low', 'high', 'num_applicants'])

class ApplicantField(ABC):

    @classmethod
    @abstractmethod
    def is_valid(cls, value: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def translate(cls, value: str) -> any:
        pass
    

class GradeAverage(ApplicantField):
    # Percentage grade average in [0, 100]

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
    def tranlsate(cls, value: str) -> float:
        return float(value)

class ApplicationType(ApplicantField):

    APPLICANT_TYPES = [ '101', '105', '105D', '105F' ]
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.APPLICANT_TYPESs

    @classmethod
    def translate(cls, value: str) -> str:
        return value


class Program(ApplicantField):

    abbreviations = pandas.read_csv('abbreviations.csv')
    program_codes = pandas.read_csv('program_codes.csv')

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.program_codes['Code'].unique()

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
    # This will throw if program code not present.. caller's problem
    def get_short_to_long(cls, program_short: str) -> str:
        return cls.abbreviations.loc[cls.abbreviations['Short'] == program_short, 'Long'].iloc[0]