# Category exeptions
class CategoryNameTaken(Exception):
    """Kategorija sa tim imenom već postoji!"""

class CategoryNotFound(Exception):
    """Kategorija ne postoji!"""

class CategoryHasTransactions(Exception):
    """Kategorija sadrži transakcije, ne može se obrisati!"""