# test/test.py

from fastapi.testclient import TestClient
from api.api import app

client = TestClient(app)


def test_full_finance_flow():
    """
    End-to-end test covering:
    1. DB-backed context retrieval
    2. EMI calculation
    3. Session memory persistence
    4. Session isolation
    """

    session_id = "test-session-1"

    # --------------------------------------------------
    # 1. DB-backed question
    # --------------------------------------------------
    response_1 = client.post(
        "/chat",
        json={
            "message": "What is the interest rate for home loan?",
            "session_id": session_id
        }
    )

    assert response_1.status_code == 200
    body_1 = response_1.json()
    assert "8.75" in body_1["response"]

    print("✔ Interest rate fetched from DB")

    # --------------------------------------------------
    # 2. EMI calculation
    # --------------------------------------------------
    response_2 = client.post(
        "/chat",
        json={
            "message": "Calculate EMI for home loan of 50 lakh for 20 years",
            "session_id": session_id
        }
    )

    assert response_2.status_code == 200
    body_2 = response_2.json()

    assert body_2["data"]["loan_type"] == "Home Loan"
    assert body_2["data"]["emi"] > 0

    print("✔ EMI calculation works")

    # --------------------------------------------------
    # 3. Memory-based follow-up (same session)
    # --------------------------------------------------
    response_3 = client.post(
        "/chat",
        json={
            "message": "Do you remember what we discussed?",
            "session_id": session_id
        }
    )

    assert response_3.status_code == 200
    body_3 = response_3.json()

    memory_response = body_3["response"].lower()

    assert (
        "interest rate" in memory_response
        or "emi" in memory_response
        or "home loan" in memory_response
    ), "Session memory not working"

    print("✔ Session memory works")

    # --------------------------------------------------
    # 4. Session isolation (new session)
    # --------------------------------------------------
    response_4 = client.post(
        "/chat",
        json={
            "message": "Do you remember what we discussed?",
            "session_id": "new-session"
        }
    )

    assert response_4.status_code == 200
    body_4 = response_4.json()

    isolation_response = body_4["response"].lower()

    assert (
        "no prior" in isolation_response
        or "beginning" in isolation_response
        or "first interaction" in isolation_response
        or "no conversation" in isolation_response
        or "nothing to recall" in isolation_response
        or "do not have any prior" in isolation_response
    ), "Session isolation failed"

    print("✔ Session isolation works")
