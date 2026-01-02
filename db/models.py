# db/models.py

from sqlalchemy import Column, Integer, String, Float, Text
from db.base import Base


class LoanProduct(Base):
    __tablename__ = "loan_products"

    id = Column(Integer, primary_key=True, index=True)

    loan_type = Column(String(100), nullable=False, unique=True)

    interest_rate = Column(Float, nullable=False)

    min_tenure_years = Column(Integer, nullable=False)
    max_tenure_years = Column(Integer, nullable=False)

    processing_fee_percent = Column(Float, nullable=False)

    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<LoanProduct {self.loan_type} @ {self.interest_rate}%>"
