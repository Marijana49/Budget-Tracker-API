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


# CSV exeptions
class InvalidCsvFile(Exception):
    """CSV nema očekivane kolone ili ga nije moguće pročitati!"""


# Budget exeptions
class BudgetAlreadyExists(Exception):
    """Budžet već postoji!"""

class BudgetNotFound(Exception):
    """Budžet ne postoji!"""