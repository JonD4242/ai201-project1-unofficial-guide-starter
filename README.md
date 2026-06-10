# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This RAG system serves as an unofficial survival guide for Baruch College (CUNY) students, covering the practical knowledge that doesn't appear in any official handbook — from navigating CUNYfirst registration and avoiding waitlist traps, to finding financial aid, picking professors, and making the most of campus life. The domain draws on official Baruch resources, student-generated reviews, and community advice to answer the questions students actually ask.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Ready, Set, Register! | Official web page | https://www.baruch.cuny.edu/advisement/ready-set-register/ |
| 2 | New Student Onboarding Guide | Official web page | https://www.baruch.cuny.edu/new-student-programs/new-student-onboarding-guide/ |
| 3 | First Year Course Scheduling | Official web page | https://www.baruch.cuny.edu/new-student-programs/first-year-student-orientation/first-year-course-scheduling/ |
| 4 | Registrar FAQ | Official web page | https://enrollmentmanagement.baruch.cuny.edu/registrar/frequently-asked-questions/ |
| 5 | CUNYfirst Registration How-To | Official PDF guide | https://enrollmentmanagement.baruch.cuny.edu/wp-content/uploads/sites/18/2020/10/How-to-register.pdf |
| 6 | Financial Aid Services | Official web page | https://enrollmentmanagement.baruch.cuny.edu/financial-aid-services/ |
| 7 | Financial Aid Overview – Undergraduate Catalog | Official catalog page | https://baruch-undergraduate.catalog.cuny.edu/fees-expenses-and-financial-aid/financial-aid-and-award/financial-aid-brochure |
| 8 | Student Clubs and Organizations | Official web page | https://studentaffairs.baruch.cuny.edu/studentlife/student-activities/student-clubs-organizations/ |
| 9 | Baruch College – Rate My Professors | Student review aggregator | https://www.ratemyprofessors.com/school/222 |
| 10 | Search All Baruch Professors – Rate My Professors | Student review aggregator | https://www.ratemyprofessors.com/search/professors/222?q=*&did=1019 |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The source documents are mostly FAQ pages, registration guides, and short informational paragraphs — not long narrative text. A 500-character chunk captures roughly one complete thought (a registration step, a financial aid rule, a club description) without pulling in unrelated content. HTML was stripped and whitespace normalized before chunking using BeautifulSoup. The 50-character overlap ensures that sentences split across a boundary are still represented in at least one chunk.

**Final chunk count:** 164 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast, free, and runs locally, making it ideal for a prototype. In production, I would consider a larger model like text-embedding-3-large (OpenAI) for better semantic accuracy on domain-specific student language (e.g., informal terms like "shopping period" or "prereq waiver"). The tradeoff is cost and latency — API-hosted models add per-query fees and network delay. I would also consider a model with a longer context window, since all-MiniLM-L6-v2's 256-token limit can truncate chunks that are close to the 500-character limit.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt explicitly states: "Answer using ONLY the information in the context below. Do not use outside knowledge. If the context does not contain enough information to answer, say: 'I don't have enough information about that in my sources.'" This instruction is sent with every query, before the retrieved chunks.

**How source attribution is surfaced in the response:** Each retrieved chunk is prefixed with its source filename (e.g., `[Source 1: 04_registrar_faq.txt]`) before being passed to the LLM. The system prompt instructs the model to cite source filenames at the end of every answer, so the user can trace which document the answer came from.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | How do I register for classes at Baruch? | Log into CUNYfirst, go to Student Center, search for classes, enroll on your assigned date | Correctly explained CUNYfirst steps and mentioned enrollment date/time | Relevant | Accurate |
| 2 | What happens if a class I want is full? | Add yourself to the waitlist in CUNYfirst and monitor Student Center | Correctly described the Wait List feature and how to use it | Relevant | Accurate |
| 3 | How do I apply for financial aid at Baruch? | Complete FAFSA with Baruch's code 007273, check Financial Aid portal | Mentioned FAFSA and the Financial Aid Services page, cited correct source | Relevant | Accurate |
| 4 | How do I join a student club at Baruch? | Browse Student Affairs website, clubs meet Thursdays 12:40–2:20pm | Correctly described Club Hours and the Student Affairs directory | Relevant | Accurate |
| 5 | Where is Baruch located? | 55 Lexington Ave, Manhattan (not in source documents) | Correctly refused: "I don't have enough information about that in my sources." | Off-target (as expected) | Accurate (correct refusal) |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "Where is Baruch located?"

**What the system returned:** "I don't have enough information about that in my sources."

**Root cause (tied to a specific pipeline stage):** The failure is at the document collection stage — Baruch's address and physical location were never included in any of the 10 source documents. When the retrieval stage queried ChromaDB, the top-5 chunks returned were about registration and onboarding (loosely related to "Baruch") but contained no location information. Because the context was empty of address data, the LLM correctly refused rather than hallucinating.

**What you would change to fix it:** Add a source document that covers basic Baruch facts — for example, the Baruch College "About" page (https://www.baruch.cuny.edu/about/) — which includes the address, campus map, and contact information.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the Chunking Strategy section before coding forced me to commit to a specific chunk size (500 characters) and explain why it fit my documents. This made it easy to give Claude a precise prompt when generating `ingest.py` — instead of saying "split the text," I could say "split into 500-character chunks with 50-character overlap, breaking at newlines or sentence boundaries when possible." The result was code that matched the intent without needing revision.

**One way your implementation diverged from the spec, and why:** The spec assumed all source documents would be scraped or downloaded manually. In practice, Rate My Professors (sources 9 and 10) blocks automated scrapers, so those two documents were replaced with curated fallback text summarizing what RMP provides and how to use it. This means the system cannot answer questions about specific professors' ratings — a gap that would need to be addressed in a production version by finding an alternative data source or manually copying professor reviews.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md and a list of 10 downloaded .txt documents, asking Claude to implement `ingest.py` with `chunk_text()` using 500-char chunks, 50-char overlap, and boundary-aware splitting.
- *What it produced:* A complete `ingest.py` that loaded all documents, chunked them, generated embeddings with sentence-transformers, and stored 164 chunks in ChromaDB.
- *What I changed or overrode:* Nothing — the chunk count and output matched the spec exactly on the first run.

**Instance 2**

- *What I gave the AI:* The completed `ingest.py` and the Retrieval Approach section from planning.md, asking Claude to write `query.py` using ChromaDB (top-5), sentence-transformers for query embedding, and Groq llama-3.3-70b-versatile with a strict grounding system prompt.
- *What it produced:* A `query.py` with both CLI and interactive modes, and an `app.py` Gradio UI wrapping the same logic.
- *What I changed or overrode:* I kept the temperature at 0.2 (Claude's choice) rather than 0, because a small amount of variation makes the answers read more naturally without sacrificing accuracy.
