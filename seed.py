from datetime import date

from budget_tracker_api.database import SessionLocal, create_tables
from budget_tracker_api.enums import TransactionType
from budget_tracker_api.models import Budget, Category, Transaction


def seed() -> None:
    create_tables()
    with SessionLocal() as session:
        if session.query(Category).first() is not None:
            print("Database already has data, nothing to do.")
            return

        categories = {
            name: Category(name=name, color=color)
            for name, color in [
                ("Plata", "#27AE60"),
                ("Hrana i piće", "#2ECC71"),
                ("Prevoz", "#3498DB"),
                ("Zabava", "#9B59B6"),
            ]
        }
        session.add_all(categories.values())
        session.flush()  

        def tx(kind, amount, day, description, category):
            return Transaction(
                type=kind,
                amount=amount,
                date=date(2026, 10, day),
                description=description,
                category_id=categories[category].id,
            )

        session.add_all([
            tx(TransactionType.INCOME, "1500.00", 1, "Plata za oktobar", "Plata"),
            tx(TransactionType.EXPENSE, "25.50", 5, "Ručak", "Hrana i piće"),
            tx(TransactionType.EXPENSE, "60.40", 12, "Namirnice", "Hrana i piće"),
            tx(TransactionType.EXPENSE, "40.00", 15, "Gorivo", "Prevoz"),
            tx(TransactionType.EXPENSE, "15.00", 20, "Bioskop", "Zabava"),
        ])
        session.add_all([
            Budget(month=date(2026, 10, 1), amount="100.00", category_id=categories["Hrana i piće"].id),
            Budget(month=date(2026, 10, 1), amount="30.00", category_id=categories["Prevoz"].id),
        ])
        session.commit()
        print("Seeded sample data for October 2026.")


if __name__ == "__main__":
    seed()