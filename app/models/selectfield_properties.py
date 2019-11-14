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
    REGULAR = 'Regular'
    PRIVATE = 'Private'

    def __str__(self):
        return '{}'.format(self.value)


class DayNameList(enum.Enum):
    None_choice = ' '
    Sunday = _l('Sunday')
    Monday = _l('Monday')
    Tuesday = _l('Tuesday')
    Wednesday = _l('Wednesday')
    Thursday = _l('Thursday')
    Friday = _l('Friday')
    Saturday = _l('Saturday')

    def __str__(self):
        return '{}'.format(self.value)


class MonthNameList(enum.Enum):
    January = _l('January')
    February = _l('February')
    March = _l('March')
    April = _l('April')
    May = _l('May')
    June = _l('June')
    July = _l('July')
    August = _l('August')
    September = _l('September')
    October = _l('October')
    November = _l('November')
    December = _l('December')

    def __str__(self):
        return '{}'.format(self.value)


class PaymentStatus(enum.Enum):
    PENDING = _l('PENDING')
    INSTALLMENT = _l('INSTALLMENT')
    REJECTED = _l('REJECTED')
    COMPLETED = _l('COMPLETED')
    WARNING_1 = _l('Warning-1')
    WARNING_2 = _l('Warning-2')
    WARNING_3 = _l('Warning-3')

    def __str__(self):
        return '{}'.format(self.value)


class RegistrationPaymentStatus(enum.Enum):
    PENDING = _l('PENDING')
    INSTALLMENT = _l('INSTALLMENT')
    COMPLETED = _l('COMPLETED')

    def __str__(self):
        return '{}'.format(self.value)


last_educations = [(y.name, _l(str(y.value))) for y in (LastEducation)]
gender = [(y.name, _l(str(y.value))) for y in (Gender)]
type_of_class = [(y.name, _l(str(y.value))) for y in (TypeOfClass)]
day_name_list = [(y.name, _l(str(y.value))) for y in (DayNameList)]
month_name_list = [(y.name, _l(str(y.value))) for y in (MonthNameList)]
payment_status = [(y.name, _l(str(y.value))) for y in (PaymentStatus)]
registration_payment_status = [(y.name, _l(str(y.value))) for y in (RegistrationPaymentStatus)]
