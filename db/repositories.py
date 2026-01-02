# db/repositories.py
from sqlalchemy.orm import Session
from db.models import LoanProduct


class LoanRepository:
    """
    Handles loan product DB access
    """

    @staticmethod
    def get_all_loans(session: Session):
        return session.query(LoanProduct).all()

    @staticmethod
    def get_loan_by_type(session: Session, loan_type: str):
        return (
            session.query(LoanProduct)
            .filter(LoanProduct.loan_type.ilike(f"%{loan_type}%"))
            .first()
        )
