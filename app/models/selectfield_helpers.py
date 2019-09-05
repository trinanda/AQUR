import enum


class Gender(enum.Enum):
    MALE = 'Male'
    FEMALE = 'Female'

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
        return str(self.value)


last_educations = [(str(y), str(y)) for y in (LastEducation)]
