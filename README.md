# BFSI Call Center AI Assistant

---

# How To Run Properly

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/build_dataset_index.py
python scripts/build_rag_index.py
uvicorn app.main:app
```

---

# 1. BFSI Call Center AI Assistant

## Project Overview

This project implements a lightweight, compliant, and efficient AI assistant designed to handle common Banking, Financial Services, and Insurance (BFSI) call center queries.

The assistant prioritizes curated responses to ensure regulatory compliance and minimizes hallucination risks by using a dataset-first architecture.

### The system supports:

- Loan eligibility and application status  
- EMI details and schedules  
- Interest rate information  
- Payment and transaction queries  
- Basic account and customer support  

---

# 2. Design Philosophy

In BFSI environments, accuracy and compliance are critical. Generative models alone can hallucinate financial data, which is unacceptable.

### Therefore, this system follows a strict response hierarchy:

1. Dataset Similarity Match (Primary Layer)  
2. Fine-Tuned Small Language Model (Fallback Layer)  
3. RAG-based Knowledge Retrieval (Complex Queries Only)  

### This ensures:

- Controlled responses  
- No fabricated financial information  
- Policy-grounded outputs  
- Regulatory safety  

---

# 3. System Architecture

```
User Query
   ↓
Guardrail Validation
   ↓
Dataset Similarity Check (FAISS)
   ↓
If Strong Match → Return Stored Response
Else
   ↓
Fine-Tuned Local SLM
   ↓
If Complex / Policy Query → RAG Retrieval
   ↓
Final Response
```

---

# 4. Core Components

## 4.1 Alpaca Dataset (Primary Response Layer)

- 150+ BFSI conversation samples  
- Format: Instruction, Input, Output  
- Professional, compliant tone  
- Used for similarity matching  

## 4.2 Small Language Model (Local SLM)

- Lightweight instruction-based model  
- Fine-tuned on BFSI dataset  
- Runs locally  
- Used only when no strong dataset match is found  

## 4.3 RAG Layer

- Used for complex financial or regulatory queries  
- Retrieves structured policy documents  
- Prevents hallucination  
- Ensures grounded answers  

---

# 5. Guardrails and Compliance

- No guessing of financial numbers  
- No generation of fake rates or policies  
- No exposure of sensitive customer data  
- Out-of-domain query rejection  
- Deterministic generation (low temperature)  

---

# 6. Scalability and Maintainability

- Vector indices version controlled  
- Dataset extensible  
- Knowledge documents updatable  
- Stateless API design  
- Supports horizontal scaling  

---

# 7. Deliverables

- 150+ Alpaca formatted BFSI dataset  
- Fine-tuned small local model  
- Structured RAG knowledge base  
- Working end-to-end demo  
- Technical documentation  

---

# Validate Full Architecture (Tier 1 → Tier 2 → Tier 3)

## 1. Guardrail Validation (Compliance Layer)

**Demo Query:**  
Give me someone else's account details

---

## 2. Tier 1 — Dataset Similarity (< 1 second)

**Demo Query:**  
How can I track my Personal Loan application?

---

## 3. Tier 2 — Fine-Tuned SLM (~40 sec CPU)

**Demo Query:**  
What is EMI?

---

## 4. Tier 3 — RAG (1–2 minutes CPU)

**Demo Query:**  
What happens if EMI is unpaid for 90 days?

---
## ARCHITECTURE DIAGRAM TEXT
```
+------------------+
|   User Query     |
+------------------+
          |
          v
+------------------+
|  Guardrail Layer |
|  - Privacy Check |
|  - Domain Check  |
|  - Safety Rules  |
+------------------+
          |
          v
+---------------------------+
| Tier 1: Dataset Layer     |
| - Alpaca 150+ samples     |
| - SentenceTransformer      |
| - FAISS Similarity Search  |
+---------------------------+
          |
   Strong Match?
        /     \
      Yes      No
      /          \
+----------------+   +-----------------------+
| Return Stored  |   | Tier 2: Local SLM     |
| Response       |   | - TinyLlama 1.1B      |
+----------------+   | - Controlled Prompt   |
                     +-----------------------+
                                |
                    Compliance / Policy Query?
                          /          \
                        Yes           No
                        /              \
        +-----------------------------+   +------------------+
        | Tier 3: RAG Layer           |   | Return SLM       |
        | - Policy Knowledge Base      |   | Response         |
        | - FAISS Retrieval            |   +------------------+
        | - Context + SLM Generation   |
        +-----------------------------+
                                |
                                v
                     +------------------+
                     | Final Response   |
                     +------------------+

```
---
