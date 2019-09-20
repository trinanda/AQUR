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


class TypeOfClass(enum.Enum):
    REGULAR = 'REGULAR'
    PRIVATE = 'PRIVATE'

    def __str__(self):
        return self.value


class DayNameList(enum.Enum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

    def __str__(self):
        return self.value


class MonthNameList(enum.Enum):
    January = 'January'
    February = 'February'
    March = 'March'
    April = 'April'
    May = 'May'
    June = 'June'
    July = 'July'
    August = 'August'
    September = 'September'
    October = 'October'
    November = 'November'
    December = 'December'

    def __str__(self):
        return self.value


class DayNameList(enum.Enum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wenesday = 'Wenesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

    def __str__(self):
        return self.value


class PaymentStatus(enum.Enum):
    PENDING = 'PENDING'
    INSTALLMENT = 'INSTALLMENT'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'

    def __str__(self):
        return self.value


class CourseStatus(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'

    def __str__(self):
        return self.value


last_educations = [(str(y), str(y)) for y in (LastEducation)]
gender = [(str(y), y) for y in (Gender)]
type_of_class = [(str(y), y) for y in (TypeOfClass)]
day_name_list = [(str(y), y) for y in (DayNameList)]
month_name_list = [(str(y), y) for y in (MonthNameList)]
day_name_list = [(str(y), y) for y in (DayNameList)]
payment_status = [(str(y), y) for y in (PaymentStatus)]
course_status = [(str(y), y) for y in (CourseStatus)]
