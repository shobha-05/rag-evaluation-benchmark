# RAG Evaluation Benchmark

A RAG evaluation and benchmarking system that compares multiple retrieval strategies on the same document corpus and evaluation dataset.

The goal is to answer a simple question:

> **Which retrieval strategy gives the best results for the same RAG workload?**

The project currently evaluates **4 retrieval strategies** using **50 interview-standard questions** and semantic similarity scoring.

---

## 1. Project Overview

The pipeline is:

```text
PDF Documents
     ↓
Text Extraction
     ↓
Chunking Strategy
     ↓
Embeddings
     ↓
ChromaDB
     ↓
Question Retrieval
     ↓
Top-K Relevant Chunks
     ↓
Semantic Evaluation
     ↓
Accuracy / Quality Score
```

Each strategy uses the **same document and the same 50 questions** so that the strategies can be compared fairly.

---

## 2. Project Structure

```text
rag-evaluation-benchmark/
│
├── data/
│   ├── documents/
│   │   └── design-patterns.pdf
│   │
│   ├── questions/
│   │   └── rag_eval_dataset_interview.json
│   │
│   ├── evaluation/
│   │   ├── baseline_strategy_1.json
│   │   ├── baseline_strategy_2.json
│   │   └── baseline_strategy_3.json
│   │
│   ├── chroma/
│   ├── chroma_strategy2/
│   ├── chroma_strategy3/
│   └── chroma_strategy4/
│
├── src/
│   │
│   ├── ingestion/
│   │   └── pdf_loader.py
│   │
│   ├── chunking/
│   │   ├── simple_chunker.py
│   │   ├── semantic_chunker.py
│   │   ├── small_chunker.py
│   │   └── hybrid_chunker.py
│   │
│   ├── retrieval/
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   └── search.py
│   │
│   ├── evaluation/
│   │   ├── evaluate.py
│   │   ├── benchmark_strategy2.py
│   │   ├── benchmark_strategy3.py
│   │   └── benchmark_strategy4.py
│   │
│   └── main.py
│
├── tests/
├── requirements.txt
├── .env
└── README.md
```

---

# 3. What Each Folder Does

## `data/documents/`

Contains the documents used by the RAG system.

Example:

```text
design-patterns.pdf
```

This is the source knowledge base.

---

## `data/questions/`

Contains the evaluation dataset.

```text
rag_eval_dataset_interview.json
```

The dataset contains **50 questions**.

Each question contains:

```json
{
  "question_id": "q001",
  "question": "...",
  "expected_answer": "...",
  "source_section": "...",
  "difficulty": "easy",
  "relevant_content": "..."
}
```

The same 50 questions are used for every strategy.

---

## `data/evaluation/`

Stores baseline results for each strategy.

These files allow us to compare future changes against previous results.

Example:

```text
baseline_strategy_1.json
baseline_strategy_2.json
baseline_strategy_3.json
```

---

## `data/chroma*`

These directories contain the persisted ChromaDB vector collections.

Each strategy has its own collection so that experiments do not overwrite each other.

```text
data/chroma/
data/chroma_strategy2/
data/chroma_strategy3/
data/chroma_strategy4/
```

---

# 4. Source Code

## `src/ingestion/`

Responsible for loading source documents.

### `pdf_loader.py`

Reads the PDF and extracts its text.

```text
PDF → extracted text
```

---

# 5. Chunking Strategies

The main experiment in this project is comparing different ways of splitting documents into chunks.

## Strategy #1 — Fixed Chunking

File:

```text
src/chunking/simple_chunker.py
```

Configuration:

```text
Chunk size: 1000 characters
Overlap:    200 characters
```

Result:

```text
483 chunks
```

This is the baseline strategy.

---

## Strategy #2 — Paragraph-Aware Chunking

File:

```text
src/chunking/semantic_chunker.py
```

This strategy attempts to keep related lines/paragraphs together instead of blindly cutting every N characters.

Result:

```text
263 chunks
```

This strategy performed slightly worse than Strategy #1 for this dataset.

---

## Strategy #3 — Small Fixed Chunks

File:

```text
src/chunking/small_chunker.py
```

Configuration:

```text
Chunk size: 500 characters
Overlap:    100 characters
```

Result:

```text
965 chunks
```

This produced the best evaluation score.

---

## Strategy #4 — Hybrid Chunking

File:

```text
src/chunking/hybrid_chunker.py
```

Configuration:

```text
Maximum chunk size: 1000 characters
```

The strategy builds chunks from extracted lines while trying to avoid cutting content unnecessarily.

Result:

```text
397 chunks
```

---

# 6. Embeddings

File:

```text
src/retrieval/embedder.py
```

The project currently uses:

```text
all-MiniLM-L6-v2
```

Each chunk is converted into a vector representation.

For example:

```text
Text chunk
   ↓
Embedding model
   ↓
Vector
```

These vectors are stored in ChromaDB.

---

# 7. Vector Database

File:

```text
src/retrieval/vector_store.py
```

The project uses **ChromaDB** as the vector database.

The database stores:

```text
Chunk ID
Chunk text
Embedding
```

When a user asks a question:

```text
Question
   ↓
Question embedding
   ↓
Vector similarity search
   ↓
Top 5 chunks
```

---

# 8. Retrieval

File:

```text
src/retrieval/search.py
```

The retrieval layer:

1. Converts the question into an embedding.
2. Searches ChromaDB.
3. Retrieves the top 5 most similar chunks.

The important parameter is:

```text
top_k = 5
```

So every question is evaluated using its five most relevant retrieved chunks.

---

# 9. Evaluation

The project does not require the retrieved chunk to contain the **exact wording** of the expected answer.

Instead, it evaluates the **semantic similarity** between:

```text
Expected answer
       ↓
Embedding
       ↕
Retrieved chunk
       ↓
Embedding
```

Cosine similarity is used as the similarity measure.

### Thresholds

```text
Score >= 0.55  → CORRECT

0.40–0.54      → PARTIAL

< 0.40         → INCORRECT
```

For each question, the highest similarity among the top 5 retrieved chunks is used.

---

# 10. Final Score

The evaluation uses a weighted score:

```text
CORRECT = 1.0
PARTIAL = 0.5
INCORRECT = 0
```

Therefore:

```text
Score =
(Correct + 0.5 × Partial) / Total Questions
```

For example:

```text
34 correct
10 partial
6 incorrect

Score =
(34 + 0.5 × 10) / 50

= 39 / 50

= 78%
```

---

# 11. Benchmark Results

Current results:

| Strategy    | Chunking           | Chunks | Correct | Partial | Incorrect |      Score |
| ----------- | ------------------ | -----: | ------: | ------: | --------: | ---------: |
| Strategy #1 | 1000 + 200 overlap |    483 |      28 |      17 |         5 |    **73%** |
| Strategy #2 | Paragraph-aware    |    263 |      25 |      22 |         3 |    **72%** |
| Strategy #3 | 500 + 100 overlap  |    965 |      34 |      10 |         6 | **78% 🏆** |
| Strategy #4 | Hybrid 1000        |    397 |      29 |      17 |         4 |    **75%** |

### Current winner

**Strategy #3 — 500-character chunks with 100-character overlap**

```text
Semantic Score: 78%
```

This suggests that smaller chunks provided more focused retrieval for this particular document and question set.

---

# 12. How to Run the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Set the Python path:

```bash
export PYTHONPATH=src
```

---

## Run Strategy #1

```bash
PYTHONPATH=src python src/main.py
```

Evaluate:

```bash
PYTHONPATH=src python src/evaluation/evaluate.py
```

---

## Run Strategy #2

```bash
PYTHONPATH=src python src/evaluation/benchmark_strategy2.py
```

---

## Run Strategy #3

```bash
PYTHONPATH=src python src/evaluation/benchmark_strategy3.py
```

---

## Run Strategy #4

```bash
PYTHONPATH=src python src/evaluation/benchmark_strategy4.py
```

---

# 13. Adding New Evaluation Questions

Add questions to:

```text
data/questions/rag_eval_dataset_interview.json
```

Each question should contain:

```text
question_id
question
expected_answer
source_section
difficulty
relevant_content
```

All retrieval strategies should be evaluated against the same dataset.

This keeps the benchmark fair.

---

# 14. Why This Project Matters

A RAG system can appear to work while still retrieving poor context.

This project makes retrieval quality measurable.

Instead of saying:

> "The RAG system seems good."

we can say:

> "Strategy #3 achieved 78% semantic evaluation score on the same 50-question benchmark."

This makes it possible to:

* Compare retrieval strategies.
* Detect quality regressions.
* Experiment with chunk sizes.
* Experiment with embedding models.
* Experiment with vector databases.
* Add automated CI quality gates.

---

# 15. Future Improvements

Planned improvements include:

### Evaluation

* Add an LLM-based answer evaluator.
* Separate retrieval quality from answer-generation quality.
* Add precision/recall metrics.
* Evaluate different `top_k` values.

### Retrieval

* Hybrid BM25 + vector search.
* Reranking.
* Metadata filtering.
* Query expansion.

### Chunking

* Sentence-aware chunking.
* Heading-aware chunking.
* Recursive chunking.
* Overlap optimization.

### Engineering

* FastAPI service.
* Automated benchmark pipeline.
* GitHub Actions.
* Quality regression detection.

The eventual goal is:

```text
Code Change
    ↓
Run RAG Benchmark
    ↓
Compare Against Baseline
    ↓
Quality Improved?
    ↓
YES → Build Passes
NO  → Build Fails
```

---

# 16. Current Project Status

### Completed

* PDF ingestion
* Text extraction
* Chunking experiments
* Embedding generation
* ChromaDB vector storage
* Top-K retrieval
* 50-question evaluation dataset
* Semantic similarity evaluation
* Four retrieval strategies
* Benchmark comparison

### Current best result

```text
Strategy #3
500-character chunks
100-character overlap

Score: 78%
```

### Next milestone

Implement **automated evaluation and GitHub Actions quality regression detection** so that a change that decreases RAG quality can automatically fail the CI build.
