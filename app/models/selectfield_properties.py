import enum
from flask_babel import lazy_gettext as _l


class Gender(enum.Enum):
    Male = 'Male'
    Female = 'Female'

    def __str__(self):
        return '{}'.format(self.value)


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
        return '{}'.format(self.value)


class TypeOfClass(enum.Enum):
    REGULAR = 'REGULAR'
    PRIVATE = 'PRIVATE'

    def __str__(self):
        return '{}'.format(self.value)


class DayNameList(enum.Enum):
    None_choice = ' '
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

    def __str__(self):
        return '{}'.format(self.value)


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
        return '{}'.format(self.value)


class PaymentStatus(enum.Enum):
    PENDING = 'PENDING'
    INSTALLMENT = 'INSTALLMENT'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'

    def __str__(self):
        return '{}'.format(self.value)


class RegistrationPaymentStatus(enum.Enum):
    PENDING = 'PENDING'
    INSTALLMENT = 'INSTALLMENT'
    COMPLETED = 'COMPLETED'

    def __str__(self):
        return '{}'.format(self.value)


class CourseStatus(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    FINISHED = 'FINISHED'

    def __str__(self):
        return '{}'.format(self.value)


last_educations = [(y.name, _l(str(y.value))) for y in (LastEducation)]
gender = [(y.name, _l(str(y.value))) for y in (Gender)]
type_of_class = [(y.name, _l(str(y.value))) for y in (TypeOfClass)]
day_name_list = [(y.name, _l(str(y.value))) for y in (DayNameList)]
month_name_list = [(y.name, _l(str(y.value))) for y in (MonthNameList)]
payment_status = [(y.name, _l(str(y.value))) for y in (PaymentStatus)]
registration_payment_status = [(y.name, _l(str(y.value))) for y in (RegistrationPaymentStatus)]
course_status = [(y.name, _l(str(y.value))) for y in (CourseStatus)]
