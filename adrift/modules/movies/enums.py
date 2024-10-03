from enum import Enum

class MPAA(Enum):
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    NC_17 = 'NC-17'

    def __str__(self):
        return self.name

class Role(Enum):
    DIRECTOR = 'Director' 
    WRITER = 'Writer'
    ACTOR = 'Actor'
    ACTRESS = 'Actress'
    COMPOSER = 'Composer'

    def __str__(self):
        return self.name

class Company(Enum):
    PRODUCTION = 'Production'
    DISTRIBUTION = 'Distribution'

    def __str__(self):
        return self.name