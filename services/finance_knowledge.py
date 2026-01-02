# services/finance_knowledge.py
# Builds trusted finance knowledge context for LLM

from sqlalchemy.orm import Session
from pathlib import Path

from db.repositories import LoanRepository


class FinanceKnowledgeBuilder:
    """
    Builds factual knowledge context from DB + policy docs.
    """

    def __init__(self, session: Session):
        self.session = session

    def build_loan_context(self) -> str:
        """
        Build loan products context from database.
        """
        loans = LoanRepository.get_all_loans(self.session)

        lines = ["LOARA FINANCE LOAN PRODUCTS:\n"]

        for loan in loans:
            lines.append(
                f"""
Loan Type: {loan.loan_type}
Interest Rate: {loan.interest_rate}% per annum
Tenure: {loan.min_tenure_years} to {loan.max_tenure_years} years
Processing Fee: {loan.processing_fee_percent}%
Description: {loan.description}
""".strip()
            )

        return "\n\n".join(lines)

    def build_policy_context(self) -> str:
        """
        Load policy documents (markdown/text).
        """
        policy_dir = Path("docs/policies")
        policy_texts = []

        for policy_file in policy_dir.glob("*.md"):
            content = policy_file.read_text(encoding="utf-8")
            policy_texts.append(
                f"POLICY DOCUMENT: {policy_file.name}\n{content}"
            )

        return "\n\n".join(policy_texts)

    def build_full_context(self) -> str:
        """
        Combined trusted knowledge.
        """
        return (
            self.build_loan_context()
            + "\n\n"
            + self.build_policy_context()
        )
