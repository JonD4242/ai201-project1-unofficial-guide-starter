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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
