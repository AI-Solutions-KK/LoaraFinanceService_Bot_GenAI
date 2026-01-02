# db/seed_data.py
# Run once to seed Loara Finance core business data

from sqlalchemy.orm import Session

from db.config import engine
from db.models import LoanProduct
from db.base import Base


def seed_loan_products():
    """
    Inserts initial loan products and rates into database.
    This is SYSTEM TRUTH (no hallucination).
    """

    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)

    # Clear old data (safe for dev)
    session.query(LoanProduct).delete()

    products = [
        LoanProduct(
            loan_type="Home Loan",
            interest_rate=8.75,
            min_tenure_years=5,
            max_tenure_years=30,
            processing_fee_percent=0.5,
            description="Housing loan for purchase or construction of residential property."
        ),
        LoanProduct(
            loan_type="Car Loan",
            interest_rate=9.5,
            min_tenure_years=1,
            max_tenure_years=7,
            processing_fee_percent=1.0,
            description="Loan for purchase of new or used vehicles."
        ),
        LoanProduct(
            loan_type="Gold Loan",
            interest_rate=10.25,
            min_tenure_years=1,
            max_tenure_years=5,
            processing_fee_percent=0.75,
            description="Loan against pledged gold ornaments."
        ),
        LoanProduct(
            loan_type="Personal Loan",
            interest_rate=12.5,
            min_tenure_years=1,
            max_tenure_years=5,
            processing_fee_percent=2.0,
            description="Unsecured personal loan for various needs."
        ),
    ]

    session.add_all(products)
    session.commit()
    session.close()

    print("✅ Loara Finance loan products seeded successfully.")


if __name__ == "__main__":
    seed_loan_products()
