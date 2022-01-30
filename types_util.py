from abc import ABC, abstractmethod

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

    # Add sample / example value?
    