# Engineering Report: Operation Ledger-Mind

## Financial Intelligence Showdown: Fine-Tuning vs. Advanced RAG

**Student Name:** [Your Name]  
**Date:** February 2026  
**Context:** Uber 2024 Annual Report Analysis

---

### 1. Executive Summary (Approx. 150 Words)

[Draft Content: Briefly state which architecture won for specific tasks. For example: "The RAG system (The Librarian) outperformed the fine-tuned model (The Intern) in factual retrieval and accuracy, while the fine-tuned model demonstrated superior tonal alignment and speed for creative summaries."]

### 2. Methodology (Approx. 500 Words)

#### 2.1 Prompting Strategy

[Explain the two-step Q/A generation pipeline used in 01_data_factory.ipynb. Discuss the use of LLM A for question generation and LLM B for answering.]

#### 2.2 Hybrid RAG Parameters

[Detail the Weaviate configuration, specifically the choice of BM25 vs. Vector search weights and the effectiveness of Cross-Encoder reranking.]

### 3. The "Hallucination" Audit (Approx. 500 Words)

[Analyze specific cases where "The Intern" (Fine-Tuned) failed, especially on financial numbers. Provide examples like: "When asked about the exact R&D spend, the fine-tuned model predicted $3.2B based on training patterns, whereas the actual value was $3.5B."]

### 4. Conclusion (Approx. 350 Words)

[Recommendation for Fintech clients. When is the overhead of fine-tuning worth it (tone, private data patterns) vs. RAG (accuracy, auditability)?]

---

_End of Report_
