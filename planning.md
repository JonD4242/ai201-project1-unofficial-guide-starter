# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This RAG system serves as an unofficial survival guide for Baruch College (CUNY) students, covering the practical knowledge that doesn't appear in any official handbook — from navigating CUNYfirst registration and avoiding waitlist traps, to finding financial aid, picking professors, and making the most of campus life. The domain draws on official Baruch resources, student-generated reviews, and community advice to answer the questions students actually ask.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Ready, Set, Register! | Official registration guide and tips | https://www.baruch.cuny.edu/advisement/ready-set-register/ |
| 2 | New Student Onboarding Guide | Comprehensive guide for incoming Baruch students | https://www.baruch.cuny.edu/new-student-programs/new-student-onboarding-guide/ |
| 3 | First Year Course Scheduling | Course scheduling guidance for first-year students | https://www.baruch.cuny.edu/new-student-programs/first-year-student-orientation/first-year-course-scheduling/ |
| 4 | Registrar FAQ | Frequently asked questions about registration, holds, and enrollment | https://enrollmentmanagement.baruch.cuny.edu/registrar/frequently-asked-questions/ |
| 5 | CUNYfirst Registration How-To (PDF) | Step-by-step guide for registering via CUNYfirst | https://enrollmentmanagement.baruch.cuny.edu/wp-content/uploads/sites/18/2020/10/How-to-register.pdf |
| 6 | Financial Aid Services | Overview of financial aid options and processes | https://enrollmentmanagement.baruch.cuny.edu/financial-aid-services/ |
| 7 | Financial Aid Overview – Undergraduate Catalog | Detailed breakdown of grants, loans, and scholarships | https://baruch-undergraduate.catalog.cuny.edu/fees-expenses-and-financial-aid/financial-aid-and-award/financial-aid-brochure |
| 8 | Student Clubs and Organizations | Directory and info on 120+ student clubs and campus life | https://studentaffairs.baruch.cuny.edu/studentlife/student-activities/student-clubs-organizations/ |
| 9 | Baruch College – Rate My Professors (School Page) | Aggregate professor ratings and student reviews | https://www.ratemyprofessors.com/school/222 |
| 10 | Search All Baruch Professors – Rate My Professors | Full searchable list of Baruch professor reviews | https://www.ratemyprofessors.com/search/professors/222?q=*&did=1019 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 50 characters

**Reasoning:** The source documents are a mix of FAQ pages, step-by-step guides, and short informational paragraphs. A 500-character chunk is roughly 2–4 sentences — large enough to contain a complete thought (e.g., one registration step or one financial aid rule) but small enough that retrieval returns focused, relevant content rather than entire pages. A 50-character overlap prevents important information from being lost at chunk boundaries, such as when a sentence spans the end of one chunk and the start of the next.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers (local, no API key required)

**Top-k:** 5

**Production tradeoff reflection:** all-MiniLM-L6-v2 is fast and lightweight, which makes it ideal for a local prototype. In a real production deployment, I would consider a model like text-embedding-3-large (OpenAI) or instructor-xl, which produce higher-quality embeddings on domain-specific text at the cost of higher latency and API fees. I would also weigh context length — all-MiniLM-L6-v2 has a 256-token limit, which can truncate longer chunks — and multilingual support if serving non-English-speaking students.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | How do I register for classes at Baruch? | Log into CUNYfirst, go to Self Service > Student Center, click Search for Classes, and enroll using your assigned registration date. |
| 2 | What happens if a class I want is full? | You can add yourself to the waitlist using the Wait List feature in CUNYfirst and monitor your Student Center for updates. |
| 3 | How do I apply for financial aid at Baruch? | Complete the FAFSA using Baruch's federal code 007273 and check the Financial Aid Services portal for your aid package. |
| 4 | How do I join a student club at Baruch? | Browse the 120+ clubs listed on the Student Affairs website; most meet during Club Hours on Thursdays 12:40–2:20pm. |
| 5 | How do I check professor ratings before registering? | Visit ratemyprofessors.com/school/222 and search by professor name or department; look at overall rating, difficulty, and "would take again" percentage. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Chunk boundary splits key information:** Some documents (especially the FAQ) contain multi-part answers where the question and its answer may fall in different chunks. If a chunk boundary splits a question from its answer, retrieval might return the question text without the corresponding answer, causing the LLM to respond with incomplete or inaccurate information.

2. **Rate My Professors content is curated, not scraped:** Because RMP blocks automated scrapers, the two RMP documents contain manually written fallback text rather than real student reviews. This means the system cannot answer specific questions about individual professors' ratings or comments, and may incorrectly generalize from the curated summary.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INDEXING PIPELINE                            │
│                       (run once: ingest.py)                         │
│                                                                     │
│  documents/*.txt  ──►  chunk_text()   ──►  SentenceTransformer     │
│  (10 .txt files)       500 char/50     │   all-MiniLM-L6-v2        │
│                        char overlap    │   (sentence-transformers)  │
│                                        ▼                            │
│                                   ChromaDB                          │
│                                   (chroma_db/)                      │
│                                   164 chunks stored                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        QUERY PIPELINE                               │
│                   (runtime: query.py / app.py)                      │
│                                                                     │
│  User question  ──►  SentenceTransformer  ──►  ChromaDB            │
│                       (embed question)          query()             │
│                                                 top-5 chunks        │
│                                                      │              │
│                                                      ▼              │
│                                              Groq API               │
│                                         llama-3.3-70b-versatile     │
│                                              │                      │
│                                              ▼                      │
│                                    Grounded answer + sources        │
│                                    displayed in Gradio UI           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I gave Claude the Chunking Strategy section of this planning.md and asked it to implement a `chunk_text()` function using 500-character chunks with 50-character overlap, with boundary-aware splitting that prefers newlines and sentence endings over mid-word cuts. I verified the output by checking that total chunk count (164) was reasonable for 10 documents and that individual chunks read as complete thoughts.

**Milestone 4 — Embedding and retrieval:**
I gave Claude the Retrieval Approach section and asked it to write `query.py` using sentence-transformers for embedding, ChromaDB for retrieval (top-5), and Groq's llama-3.3-70b-versatile for generation with a strict grounding instruction. I verified it by running test queries and checking that answers cited sources and refused to answer questions outside the documents.

**Milestone 5 — Generation and interface:**
I gave Claude the completed `query.py` and asked it to wrap the same logic in a Gradio ChatInterface with example questions. I verified by opening the UI and testing all 5 evaluation questions from the Evaluation Plan.
