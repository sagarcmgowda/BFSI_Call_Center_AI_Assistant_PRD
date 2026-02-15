from app.services.similarity_service import SimilarityService
from app.services.slm_service import SLMService
from app.services.rag_service import RAGService
from app.services.guardrail_service import validate_query


similarity_service = SimilarityService()
slm_service = SLMService()
rag_service = RAGService()


def process_query(query: str):
    """
    PRD-Compliant Pipeline:
    Guardrail → Tier 1 (Dataset) → Tier 2 (SLM) → Tier 3 (RAG + SLM if required)
    """

    query = query.strip()

    # -----------------------------------
    # 🛡 Guardrail Layer
    # -----------------------------------
    valid, message = validate_query(query)

    if not valid:
        return {
            "tier": "Guardrail",
            "response": message
        }

    # -----------------------------------
    # Tier 1 — Dataset Similarity
    # -----------------------------------
    dataset_response = similarity_service.search(query)

    if dataset_response:
        return {
            "tier": "Tier 1 - Dataset",
            "response": dataset_response
        }

    # -----------------------------------
    # Tier 2 — Local SLM Generation
    # -----------------------------------
    slm_response = slm_service.generate(query)

    # -----------------------------------
    # Tier 3 — RAG Trigger (if required)
    # -----------------------------------
    compliance_keywords = [
        "policy",
        "penalty",
        "npa",
        "90 days",
        "regulation",
        "rbi",
        "legal",
        "guidelines"
    ]

    if any(keyword in query.lower() for keyword in compliance_keywords):

        context = rag_service.retrieve(query)

        if context:
            grounded_response = slm_service.generate_with_context(query, context)

            return {
                "tier": "Tier 3 - RAG + SLM",
                "response": grounded_response
            }

    # -----------------------------------
    # Default Return (SLM Output)
    # -----------------------------------
    return {
        "tier": "Tier 2 - SLM",
        "response": slm_response
    }
