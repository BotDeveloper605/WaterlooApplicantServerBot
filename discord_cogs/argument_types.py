from types_util import ApplicantField


class AdmissionsOfficerMode(ApplicantField):

    APPLICANT_TYPES = [ 'NORMAL', 'EVIL' ]

    @classmethod
    def field_name(cls) -> str:
        return "OFFICER_MODE"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls.APPLICANT_TYPES

    @classmethod
    def invalid_hint(cls) -> str:
        return "{field_name}: must be one of [NORMAL, EVIL]".format(field_name = cls.field_name())

    @classmethod
    def translate(cls, value: str) -> str:
        return value