# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

My domain is student reviews of Computer Science professors at the University of Hawaii at Manoa. While the university’s official website provides information such as faculty research interests, contact details, and academic backgrounds, it does not offer insights into the classroom experience. This knowledge is valuable because students often want to understand a professor’s teaching style, workload, assessment methods, and course structure, such as whether classes rely heavily on readings or lecture slides, emphasize exams or projects, or include pop quizzes. These details are typically shared through student reviews and are difficult to find through official university channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 450 tokens

**Overlap:** 50 tokens

**Why these choices fit your documents:** Since my collection of student reviews is review-heavy, each student review should mostly stay together as one chunk so the meaning and context are not lost. A single review may mention several related details, such as teaching style, workload, exams, projects, grading, and classroom structure. Keeping each review together helps the retrieval system return complete student experiences instead of disconnected sentences. For longer reviews, a small 50-token overlap helps preserve context between chunks without creating too much repeated information.

**Final chunk count:** 76

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** `all-MiniLM-L6-v2` using the `sentence-transformers` library

**Production tradeoff reflection:**
For this project, `all-MiniLM-L6-v2` is a good choice because it runs locally, is fast, and does not require an API key or paid usage. Since the corpus is made up of short student reviews, a lightweight embedding model should be enough to retrieve relevant chunks about teaching style, workload, grading, exams, projects, and classroom experience.

If this system were deployed for real users and cost was not a constraint, I would consider using a stronger embedding model with higher retrieval accuracy and a larger context length. A larger context window could help with longer reviews or combined professor/course summaries. I would also consider whether the model handles domain-specific academic language well, since students may refer to course numbers, assignments, exams, or department-specific terms. Multilingual support could also matter if students write reviews in different languages. However, stronger models may have higher latency and require paid API usage, so I would weigh accuracy against speed, cost, and ease of deployment.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

My system enforces grounding by passing only the retrieved ChromaDB chunks into the LLM as the context. The system prompt tells the model that it must answer only from those retrieved sources and must not use outside knowledge. The prompt includes rules such as:

```
You are a grounded question-answering assistant for a RAG system.

Rules:
1. Answer using ONLY the provided context sources.
2. Do NOT use outside knowledge.
3. Do NOT guess or infer beyond what the sources say.
4. If the context does not contain enough information, say:
   "I don't have enough information in the provided documents to answer that."
5. When you use information from a source, cite it using the source label, such as [Source 1].
6. If the question asks about official information such as research interests, title, office, email, or education, use sources with Source type: official_faculty.
7. If the question asks about student reviews, only use sources with Source type: student_review.
8. If a professor appears in the official faculty source but has no student review source, say that student review information is not available in the provided documents.
```

The retrieved context is formatted into labeled source blocks before being sent to the model. Each block includes the professor name, source type, source file, distance score, and chunk text. This helps the model distinguish between official faculty information and student review information. I also use a maximum best-distance check so that if the best retrieved chunk is too weakly related to the query, the system declines to answer instead of generating a guess.

**How source attribution is surfaced in the response:**

Source attribution is handled in two ways. First, the system prompt instructs the LLM to cite retrieved chunks using labels such as [Source 1] or [Source 2] when it uses information from them. Second, the application appends a source list programmatically after generation. This means the interface always shows which chunks were retrieved, even if the LLM forgets to cite them in the answer.

Each displayed source includes the source file, professor name, source type, and distance score. This makes the answer traceable back to the retrieved documents and helps users see whether the response came from student reviews or official faculty information.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                                                                              | Expected answer                                                                                                                                                                                                                                                                                                                                              | System response (summarized)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Retrieval quality | Response accuracy |
| --- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ----------------- |
| 1   | What do students say about Peter Sadowski’s teaching style?                                           | The system should summarize student review evidence about Peter Sadowski’s teaching style, such as whether students describe the professor as clear, helpful, lecture-heavy, fast-paced, organized, or difficult to follow. The answer should only use information from the student reviews.                                                                 | According to the student reviews [Source 1, Source 2, Source 3, Source 4, Source 5], students have varying opinions about Peter Sadowski's teaching style. One student [Source 1] respected Professor Sadowski because he responded to student struggles by asking for feedback and suggestions to improve the course, and felt he genuinely cared about student success. However, another student [Source 2] felt that Professor Sadowski's answers to student questions were not always helpful, despite being knowledgeable about machine learning. Other students [Source 3, Source 4] described Professor Sadowski as knowledgeable but not strong at teaching the material, with high expectations and difficult concepts that many students struggled with. They also mentioned that the grading scale was not shown in the syllabus and that the class included a lot of homework. On the other hand, one student [Source 5] appreciated that Professor Sadowski reviewed the elementary math needed to understand the foundations of machine learning, making the course accessible to students from different backgrounds. They also appreciated that lectures were recorded and found the recordings useful for midterm review, and that Professor Sadowski responds quickly to questions and emails. Overall, the reviews suggest that Professor Sadowski's teaching style can be both helpful and challenging, with some students appreciating his efforts to support student success and others finding his expectations and teaching methods difficult to follow. | Relevant          | Accurate          |
| 2   | According to student reviews, what is the workload like in Carleton Moore’s class?                    | The system should state whether students describe the workload as light, moderate, or heavy. It should mention specific review details such as programming assignments, projects, readings, homework frequency, exam preparation, or deadline difficulty.                                                                                                    | According to student reviews, the workload in Carleton Moore's class is described as having "Lots of homework" [Source 1, Review 4; Source 3, Review 2]. One student mentions that the course had many assignments, although they were not very substantial [Source 3, Review 2]. Another student notes that the workload itself was not terrible, but the frequent quizzes made attendance feel required [Source 5, Review 5]. Additionally, the class is described as "Test heavy" [Source 3, Review 2] and having quizzes during every lecture [Source 5, Review 5]. Overall, the workload is characterized as time-consuming, especially for students without prior experience in the subject matter [Source 3, Review 2].                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | Relevant          | Accurate          |
| 3   | Do students say Henri Casanova’s course is more focused on exams, projects, homework, or quizzes?     | The system should identify the main assessment methods mentioned in the reviews. For example, it should say whether the course relies mostly on exams, projects, homework, pop quizzes, or a combination of these.                                                                                                                                           | According to the student reviews [Source 1, Source 2], Henri Casanova's course is described as "exam-heavy" [Source 1] and "test heavy" [Source 2]. There is no mention of the course being focused on projects, homework, or quizzes being a primary focus, although one review does mention that his slides include helpful practice problems [Source 1]. Another review describes the class as balanced [Source 3], but does not provide information about the specific focus of the course. Therefore, based on the provided context, it appears that Henri Casanova's course is more focused on exams.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Relevant          | Accurate          |
| 4   | What are Jason Leigh’s research interests, and what do students say about their classroom experience? | The system should combine sources carefully: it may answer the research-interest part using the official CS faculty source, but it should only answer the classroom-experience part if student reviews for Jason Leigh are available.                                                                                                                        | Jason Leigh's research interests are big data visualization, virtual reality, high performance networking, and video game design, as stated in [Source 2]. According to student reviews, students have varying opinions about their classroom experience with Professor Leigh. Some students found his lectures to be detailed and beginner-friendly [Source 1], while others thought they were not detailed enough [Source 3]. However, students generally agree that the slides contain the needed information and are available online [Source 3], and that exams are manageable if students study [Source 1, Source 4]. Students also appreciate that Professor Leigh cares about his students and that they can do well by attending class or studying the slides [Source 4]. The overall rating summary for Professor Leigh is 3.8 out of 5, with 75% of students saying they would take the course again, and a level of difficulty of 2.9 [Source 1, Source 3, Source 4, Source 5].                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Relevant          | Accurate          |
| 5   | What do students say about Haopeng Zhang’s teaching style and workload?                               | Haopeng Zhang should be a professor who appears on the official CS faculty list but does not appear in the student review source. The expected answer is that the professor appears in the official faculty source, but there are no student reviews available in the provided review dataset, so the system cannot answer about teaching style or workload. | I don't have enough information in the provided documents to answer that.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Relevant          | Accurate          |

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

**Question that failed:** What are Peter's research interests?

**What the system returned:** I don't have enough information in the provided documents to answer that. The provided documents do not contain information about Peter's research interests from a source with Source type: official_faculty. The only information available about Peter is from [Source 2] with Source type: student_review, which does not mention his research interests.

**Root cause (tied to a specific pipeline stage):** This failure happened during the retrieval stage. The query "What are Peter's research interests?" was too ambiguous because the dataset contains more than one professor with "Peter" in the name, including Peter Sadowsky and Peter-Michael Seidel. Since the query only used the first name "Peter", the embedding search did not know which professor the user meant. As a result, it retrieved a student review about Peter Sadowski/Sadowsky and unrelated official faculty chunks for other professors, instead of reliably retrieving the correct official faculty chunk.

**What you would change to fix it:** I would add a name-matching step before semantic retrieval. If the user asks about a professor using only a partial name, the system should check the professor metadata for possible matches. If there is exactly one match, it can filter retrieval to that professor. If there are multiple matches, such as Peter Sadowsky and Peter-Michael Seidel, the system should ask the user to clarify which professor they mean before answering.

**Question that failed:** How's student reviews for Dusko?

**What the system returned:** I don't have enough information in the provided documents to answer that.

**Root cause (tied to a specific pipeline stage):** This failure happened during the retrieval stage. The professor exists in my dataset as Dusko Pavlovic, but the query only used the first name “Dusko.” For some professors, the embedding search was able to match first name, last name, or full name, but it did not work reliably for this professor. This shows that relying only on semantic similarity is not enough for professor name matching, especially when the query is short and contains limited context.

The generation step did not make up an answer, which is good. However, it refused to answer because the retrieved chunks did not include the correct Dusko Pavlovic student review chunk. So the actual problem was not that the answer was missing from the documents, but that the retriever failed to return the right document.

**What you would change to fix it:** I would add a professor-name matching step before vector retrieval. The system should check the professor metadata for full names, first names, last names, and aliases before relying on embedding similarity. If the user asks for "Dusko," the system should recognize that it matches Dusko Pavlovic and then filter retrieval to chunks where `professor = "Dusko Pavlovic"`.

I would also improve the metadata by storing separate fields such as `first_name`, `last_name`, and `full_name`. Then the retrieval function could detect partial-name queries more reliably. For student review questions, I would also filter or prioritize chunks with `source_type: student_review` so the system retrieves student review data instead of unrelated official faculty information.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** The planning.md spec helped me turn the project into a clear pipeline instead of trying to build everything at once. By writing out the stages first, such as document ingestion, chunking, embedding, retrieval, and generation, I had a guide for what each milestone needed to produce before moving on. It also helped me check my work more carefully, especially during chunk inspection and retrieval testing, because I knew what kind of output each stage was supposed to create.

**One way your implementation diverged from the spec, and why:** One way my implementation diverged from the original spec was that I decided to manually clean the .txt files instead of building a full scraping or raw-data cleaning pipeline. I made this change because my sources, especially student reviews, contained a lot of website UI text, ads, buttons, and repeated labels that were easier and safer to remove manually for this project. I also adjusted the chunking approach so that student reviews mostly stayed as complete review chunks, rather than splitting everything mechanically by token count, because keeping each review together made the retrieved results easier to understand and more useful for answering classroom-experience questions.

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

- _What I gave the AI:_ I gave Claude my Milestone 4 and Milestone 5 requirements, including the embedding model all-MiniLM-L6-v2, the vector store choice ChromaDB, my top-k value of 5, and the requirement that answers must be grounded only in retrieved chunks. I also gave it examples of the types of test questions I wanted to ask, such as professor research-interest questions and student-review questions.
- _What it produced:_ Claude produced code for embedding my chunks, saving them into ChromaDB, retrieving the top 5 relevant chunks with distance scores, and connecting retrieval to the Groq LLM using llama-3.3-70b-versatile. It also produced a Gradio interface where a user can enter a question and see both the answer and the retrieved sources.
- _What I changed or overrode:_ I adjusted the grounding logic after testing retrieval results. For example, when the system failed on partial-name questions like "What are Peter’s research interests?" or "How’s student reviews for Dusko?", I identified that the issue was related to name matching during retrieval. I decided that a future improvement should add a professor-name matching step before vector retrieval, using metadata fields like full name, first name, last name, and aliases. I also kept source attribution programmatic so the interface always displays retrieved source files, instead of relying only on the LLM to cite sources correctly.

**Instance 2**

- _What I gave the AI:_ I gave Claude my retrieval test output, including the query, retrieved chunks, source metadata, and distance scores. One example was the query "What are Kyungim Baek’s research interests?" where the first result contained the correct answer but had a distance score slightly above 0.5.

- _What it produced:_ Claude helped explain why the distance score could still be high even when the correct chunk was retrieved. It explained that the embedding compared the whole query to the whole chunk, and the official faculty chunk included extra information such as title, office, email, and education, which made the chunk less focused on research interests.
- _What I changed or overrode:_ I decided not to immediately change the chunking because the top retrieved result was still correct and useful. Instead, I documented this as a retrieval observation and considered future improvements, such as making official faculty chunks more focused or adding metadata filtering for questions about research interests.
