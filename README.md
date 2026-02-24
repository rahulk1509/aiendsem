# 📝 AI Exam Paper Corrector

## Introduction to Artificial Intelligence - End Semester Project

An intelligent system that automatically grades exam papers using AI techniques from all 4 units of the AI course syllabus.

---

## 🎯 Project Overview

This project demonstrates practical application of AI concepts:

| Unit | Topic | Implementation |
|------|-------|----------------|
| **Unit I** | Search Algorithms | A*, BFS, DFS for answer matching |
| **Unit II** | CSP | Rubric constraints, backtracking |
| **Unit III** | Bayesian Inference | Confidence scoring, partial marks |
| **Unit IV** | Q-Learning | Adaptive grading, learning from feedback |

---

## 🚀 Quick Start

### Run the Application

```bash
cd ai_exam_corrector
python main.py
```

### Run Demo (No Image Required)

1. Launch the application
2. Click "Use Sample" button
3. Click "ANALYZE & GRADE"
4. View results with AI algorithm details

---

## 📁 Project Structure

```
ai_exam_corrector/
├── main.py                          # Main application entry point
├── requirements.txt                 # Dependencies
├── README.md                        # This file
│
├── image_processing/
│   ├── __init__.py
│   └── ocr_engine.py               # OCR text extraction (Unit III)
│
├── grading_engine/
│   ├── __init__.py
│   └── grader.py                   # Main grading logic
│
├── ai_algorithms/
│   ├── __init__.py
│   ├── search/
│   │   ├── __init__.py
│   │   └── answer_search.py        # BFS, DFS, A*, Greedy (Unit I)
│   ├── csp/
│   │   ├── __init__.py
│   │   └── rubric_csp.py           # CSP rubric grader (Unit II)
│   ├── bayesian/
│   │   ├── __init__.py
│   │   └── confidence_scorer.py    # Bayesian inference (Unit III)
│   └── rl/
│       ├── __init__.py
│       └── qlearning_grader.py     # Q-Learning agent (Unit IV)
│
└── gui/
    ├── __init__.py
    └── results_view.py              # Results display window
```

---

## 🧠 AI Algorithms Implemented

### Unit I: Search Algorithms

#### A* Search (Primary)
```python
# Finds optimal answer match using heuristic
f(n) = g(n) + h(n)
- g(n): Cost so far (1 - similarity)
- h(n): Heuristic (keyword overlap estimation)
```

#### BFS (Breadth-First Search)
- Explores all answers at current similarity level
- Guarantees finding best match
- Uses queue data structure

#### DFS (Depth-First Search)
- Deep exploration of answer variations
- Uses stack data structure
- Good for finding any valid match quickly

#### Greedy Search
- Picks most promising answer based on keywords
- Fastest but may miss optimal

### Unit II: Constraint Satisfaction Problem

#### Rubric-Based Grading
```python
Variables = [content_score, accuracy_score, completeness_score]
Domains = [0, 0.5, 1, 1.5, ..., max_marks]
Constraints:
  - Total ≤ max_marks
  - If accuracy = 0, content ≤ 50%
  - All scores ≥ 0
```

#### Backtracking Search
- Finds valid mark assignment satisfying all constraints
- Adjusts if constraints violated

### Unit III: Bayesian Inference

#### Confidence Scoring
```python
P(correct | keywords, similarity, length)
= Bayesian update using:
  - P(keywords | correct)
  - P(similarity | correct)  
  - P(length | correct)
```

#### OCR Confidence
```python
P(accurate_reading | image_quality, handwriting)
```

### Unit IV: Q-Learning

#### Adaptive Grading Agent
```python
State = (quality_level, question_type, confidence_level)
Actions = [full_marks, high_partial, low_partial, zero, review]
Reward = Based on teacher feedback

Q(s,a) ← Q(s,a) + α[r + γ·max(Q(s',a')) - Q(s,a)]
```

---

## 📊 Features

### 1. Multiple Question Types
- **MCQ**: Multiple choice grading
- **Short Answer**: Text matching with keywords
- **Math Problems**: Equation verification
- **Definitions**: Concept explanation matching

### 2. Algorithm Selection
Choose which AI algorithm to use:
- A* Search (recommended)
- BFS Matching
- CSP Rubric
- Bayesian Scoring
- Q-Learning

### 3. Detailed Feedback
- Similarity percentage
- Keyword match score
- Confidence level
- Improvement suggestions

### 4. Export Report
Generate detailed PDF/TXT reports with:
- Question-wise breakdown
- Marks and feedback
- Algorithm statistics

---

## 🔬 Lab Experiments Covered

| # | Experiment | Covered |
|---|------------|---------|
| 1 | BFS/DFS for path planning | ✅ |
| 2 | Greedy search | ✅ |
| 3 | A* search | ✅ |
| 5 | Backtracking CSP | ✅ |
| 8 | Bayesian inference | ✅ |
| 12 | Q-Learning | ✅ |
| 13 | Policy-based RL | ✅ |
| 14 | Bayesian belief update | ✅ |

**Total: 8 out of 14 lab experiments (57%)**

---

## 📖 How It Works

### Step 1: Input
Upload answer sheet image or use sample data

### Step 2: OCR Processing
Extract text using OCR (with Bayesian confidence)

### Step 3: Question Parsing
Identify Q&A pairs from extracted text

### Step 4: Answer Matching
Use search algorithms to find best matching answer

### Step 5: Grading
Apply CSP rubric + Bayesian + Q-Learning

### Step 6: Results
Display detailed results with feedback

---

## 🎓 For Presentation

### Key Points to Highlight:

1. **Unit I Coverage**: 
   - "We implemented A*, BFS, DFS for answer matching"
   - "Heuristic function uses keyword overlap"

2. **Unit II Coverage**:
   - "Rubric is modeled as CSP with constraints"
   - "Backtracking ensures valid grade assignment"

3. **Unit III Coverage**:
   - "Bayesian inference calculates answer confidence"
   - "P(correct | evidence) updated using Bayes' theorem"

4. **Unit IV Coverage**:
   - "Q-Learning agent learns optimal grading policy"
   - "Improves with teacher feedback over time"

---

## 👥 Team

- AI Course End Semester Project
- Introduction to Artificial Intelligence

---

## 📚 References

1. Russell & Norvig - Artificial Intelligence: A Modern Approach
2. Graesser & Keng - Foundations of Deep Reinforcement Learning

---

## 🔧 Future Enhancements

- [ ] Deep Learning OCR
- [ ] Multi-language support
- [ ] Handwriting analysis
- [ ] Plagiarism detection
- [ ] Mobile app version

---

*Generated for AI Course - Phase 1 Submission*
