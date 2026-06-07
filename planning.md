# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is student reviews of Computer Science professors at the University of Hawaii at Manoa. While the university’s official website provides information such as faculty research interests, contact details, and academic backgrounds, it does not offer insights into the classroom experience. This knowledge is valuable because students often want to understand a professor’s teaching style, workload, assessment methods, and course structure, such as whether classes rely heavily on readings or lecture slides, emphasize exams or projects, or include pop quizzes. These details are typically shared through student reviews and are difficult to find through official university channels.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source             | Description                                                                                                                                                                                          | URL or location                                    |
| --- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| 1   | UHM ICS Faculty    | Faculty directory for the Information and Computer Sciences department at University of Hawaiʻi at Mānoa, featuring faculty profiles, research interests, contact details, and academic backgrounds. | https://www.ics.hawaii.edu/people/                 |
| 2   | Rate My Professors | A Rate My Professors page for Kyungim Baek, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                   | https://www.ratemyprofessors.com/professor/1032361 |
| 3   | Rate My Professors | A Rate My Professors page for Edoardo Biagioni, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                               | https://www.ratemyprofessors.com/professor/8389    |
| 4   | Rate My Professors | A Rate My Professors page for Henri Casanova, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                 | https://www.ratemyprofessors.com/professor/1070112 |
| 5   | Rate My Professors | A Rate My Professors page for Richard Halverson, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                              | https://www.ratemyprofessors.com/professor/2013421 |
| 6   | Rate My Professors | A Rate My Professors page for Jason Leigh, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                    | https://www.ratemyprofessors.com/professor/1950937 |
| 7   | Rate My Professors | A Rate My Professors page for Carleton Moore, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                 | https://www.ratemyprofessors.com/professor/1898989 |
| 8   | Rate My Professors | A Rate My Professors page for Ravi Narayan, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                   | https://www.ratemyprofessors.com/professor/8392    |
| 9   | Rate My Professors | A Rate My Professors page for Dusko Pavlovic, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                 | https://www.ratemyprofessors.com/professor/2342816 |
| 10  | Rate My Professors | A Rate My Professors page for Andrey Popov, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                   | https://www.ratemyprofessors.com/professor/3048897 |
| 11  | Rate My Professors | A Rate My Professors page for Peter Sadowski, showing student ratings, difficulty level, recommendation rate, and review statistics.                                                                 | https://www.ratemyprofessors.com/professor/2639726 |

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

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

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
