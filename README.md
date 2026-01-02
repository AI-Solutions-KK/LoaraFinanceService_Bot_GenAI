Loara Finance Service Bot is a production-grade Generative AI backend system designed for financial institutions.

The system combines deterministic financial logic (EMI calculation) with controlled Large Language Model responses for finance-related queries.

Key design principles:
- EMI calculations are strictly mathematical (no LLM involvement)
- Financial knowledge is sourced from structured databases and policy documents
- LLM is used only for explanation and natural language interaction
- Hallucination is prevented through strict system prompts and knowledge injection

This project is intentionally built without AI orchestration frameworks in Phase 1 to ensure clarity, control, and auditability, and is designed to be migrated later to LangChain, LangGraph, and cloud-native architectures (AWS).
