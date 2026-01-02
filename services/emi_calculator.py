# services/emi_calculator.py

def calculate_emi(principal: float, annual_rate: float, years: int) -> int:
    """
    Deterministic EMI calculation.
    No LLM involved.
    """
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12

    if monthly_rate == 0:
        return int(principal / months)

    emi = principal * monthly_rate * ((1 + monthly_rate) ** months) / \
          (((1 + monthly_rate) ** months) - 1)

    return int(round(emi))
