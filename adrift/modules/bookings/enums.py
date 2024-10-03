from enum import Enum

class BookingStatus(Enum):
    CONFIRMED = 'Confirmed'
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'

    def __str__(self):
        return self.name
    

class BookingType(Enum):
    CHILD = 'Child'
    ADULT = 'Adult'
    DISABLED = 'Disabled'

    def __str__(self):
        return self.name


class PaymentMethod(Enum):
    CREDIT_CARD = 'Credit Card'
    CASH = 'Cash'

    def __str__(self):
        return self.name
