import enum


class Gender(enum.Enum):
    Male = 'Male'
    Female = 'Female'

    def __str__(self):
        return self.value


class LastEducation(enum.Enum):
    SD = 'SD'
    SMP = 'SMP'
    SMA = 'SMA'
    D1 = 'D1'
    D2 = 'D2'
    D3 = 'D3'
    S1 = 'S1'
    S2 = 'S2'
    S3 = 'S3'

    def __str__(self):
        return self.value


class TypeOfCourse(enum.Enum):
    REGULAR = 'REGULAR'
    PRIVATE = 'PRIVATE'

    def __repr__(self):
        return self.value


last_educations = [(str(y), str(y)) for y in (LastEducation)]
gender = [(str(y), y) for y in (Gender)]
