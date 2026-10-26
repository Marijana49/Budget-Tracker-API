# Category exeptions
class CategoryNameTaken(Exception):
    """Kategorija sa tim imenom već postoji!"""

class CategoryNotFound(Exception):
    """Kategorija ne postoji!"""

class CategoryHasTransactions(Exception):
    """Kategorija sadrži transakcije, ne može se obrisati!"""


# Transaction exeptions
class InvalidAmount(Exception):
    """Vrijednost nije validna!"""

class TransactionNotFound(Exception):
    """Transakcija ne postoji!"""