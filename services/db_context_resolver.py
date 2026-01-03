# services/db_context_resolver.py

from db.repositories import LoanRepository


def resolve_context_from_db(question: str, session) -> str:
    """
    Pulls ONLY factual data from DB if relevant.
    No hallucination. No inference.
    """

    context_blocks = []

    # Basic keyword check (fast + safe)
    q = question.lower()

    if "interest" in q or "rate" in q or "home loan" in q:
        loans = LoanRepository.get_all_loans(session)

        for loan in loans:
            context_blocks.append(
                f"""
Loan Type: {loan.loan_type}
Interest Rate: {loan.interest_rate}% per annum
Tenure: {loan.min_tenure_years} to {loan.max_tenure_years} years
Processing Fee: {loan.processing_fee_percent}%
Description: {loan.description}
""".strip()
            )

    if not context_blocks:
        return ""

    return "\n\n".join(context_blocks)
