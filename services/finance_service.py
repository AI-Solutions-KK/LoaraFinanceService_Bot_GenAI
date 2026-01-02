# services/finance_service.py

from db.repositories import LoanRepository
from sqlalchemy.orm import Session
import math


def is_emi_question(message: str) -> bool:
    keywords = ["emi", "installment", "monthly payment", "repayment"]
    return any(k in message.lower() for k in keywords)


def calculate_emi(principal: float, annual_rate: float, tenure_years: int):
    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12

    emi = principal * monthly_rate * math.pow(1 + monthly_rate, months)
    emi /= math.pow(1 + monthly_rate, months) - 1

    return round(emi, 2)


def handle_emi_query(message: str, session: Session) -> dict:
    """
    Returns structured EMI data (NOT string)
    """

    loan_type_key = None
    for key in ["home", "car", "gold", "personal"]:
        if key in message.lower():
            loan_type_key = key
            break

    if not loan_type_key:
        return {"error": "Please specify loan type (Home / Car / Gold / Personal)."}

    loan = LoanRepository.get_loan_by_type(session, loan_type_key)
    if not loan:
        return {"error": "Loan type not found."}

    principal = 1_000_000  # default Swagger-safe value
    tenure = loan.max_tenure_years
    emi = calculate_emi(principal, loan.interest_rate, tenure)

    return {
        "loan_type": loan.loan_type,
        "principal": principal,
        "interest_rate": loan.interest_rate,
        "tenure_years": tenure,
        "emi": emi
    }
