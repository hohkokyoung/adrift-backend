from enum import Enum
from django_countries.data import COUNTRIES

class LogAction(Enum):
    CREATE = 'Create'
    UPDATE = 'Update'
    DELETE = 'DELETE'

    def __str__(self):
        return self.name

class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    
    def __str__(self):
        return self.name
    
Country = Enum('Country', dict(COUNTRIES))
# class CountryEnum(Enum):
    # for code in COUNTRIES:
    #     print(code)
        