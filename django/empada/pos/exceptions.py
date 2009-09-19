"Global Empada POS Exceptions"

class DuplicateOpenedTicket(Exception):
    "System already have a ticket with this number opened"
    pass
class OperationNotPermited(Exception):
    "We cannot perform this operation"
    pass
