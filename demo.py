"""
Quick Demo Script - Run this to test the system
================================================
This script demonstrates all AI algorithms without needing
the full GUI or image upload.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_algorithms.search.answer_search import AnswerSearcher
from ai_algorithms.bayesian.confidence_scorer import ConfidenceScorer
from ai_algorithms.csp.rubric_csp import RubricCSP
from ai_algorithms.rl.qlearning_grader import get_pretrained_agent
from grading_engine.grader import ExamGrader


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_search_algorithms():
    """Demonstrate Unit I: Search Algorithms"""
    print_header("UNIT I: SEARCH ALGORITHMS")
    
    searcher = AnswerSearcher()
    
    # Test answer bank
    answer_bank = [
        "Artificial Intelligence is the simulation of human intelligence by machines",
        "AI refers to machines that can perform tasks requiring human intelligence",
        "Machine learning is a subset of AI",
    ]
    
    student_answer = "AI is the simulation of human intelligence in machines"
    
    print(f"\nStudent Answer: '{student_answer}'")
    print("\nSearching for best match using different algorithms:\n")
    
    for algo in ["BFS", "DFS", "Greedy", "A* Search"]:
        result = searcher.search(student_answer, answer_bank, algo)
        print(f"  {algo:12} | Match: {result['similarity_score']:.1%} | Nodes: {result['nodes_explored']}")
        
    print("\n✅ Search algorithms working correctly!")


def demo_csp():
    """Demonstrate Unit II: Constraint Satisfaction"""
    print_header("UNIT II: CSP - RUBRIC GRADING")
    
    csp = RubricCSP()
    
    # Test evidence
    evidence = {
        'keyword_match': 0.8,
        'similarity': 0.75,
        'length_appropriate': True,
        'has_steps': True
    }
    
    print(f"\nEvidence: {evidence}")
    
    result = csp.grade_with_rubric(evidence, max_marks=10)
    
    print(f"\nCSP Result:")
    print(f"  Total Marks: {result['total_marks']}/{result['max_marks']}")
    print(f"  Breakdown:")
    for component, value in result['breakdown'].items():
        print(f"    - {component}: {value}")
    print(f"  Constraints Satisfied: {result['constraints_satisfied']}")
    
    print("\n✅ CSP rubric grading working correctly!")


def demo_bayesian():
    """Demonstrate Unit III: Bayesian Inference"""
    print_header("UNIT III: BAYESIAN INFERENCE")
    
    scorer = ConfidenceScorer()
    
    # Test confidence calculation
    print("\nCalculating confidence using Bayes' theorem:")
    print("  P(correct | keyword_score, similarity, length)")
    
    test_cases = [
        (0.9, 0.85, True, "High quality answer"),
        (0.5, 0.6, True, "Partial answer"),
        (0.2, 0.1, False, "Poor answer"),
    ]
    
    for kw, sim, length, desc in test_cases:
        result = scorer.calculate_confidence(kw, sim, length)
        marks = scorer.calculate_partial_marks(10, kw, sim)
        
        print(f"\n  {desc}:")
        print(f"    Keywords: {kw:.0%}, Similarity: {sim:.0%}")
        print(f"    Confidence: {result['confidence']:.1%}")
        print(f"    Marks: {marks['marks']}/10")
        print(f"    {result['interpretation']}")
        
    print("\n✅ Bayesian inference working correctly!")


def demo_qlearning():
    """Demonstrate Unit IV: Q-Learning"""
    print_header("UNIT IV: Q-LEARNING")
    
    agent = get_pretrained_agent()
    
    print("\nQ-Learning Agent learns optimal grading policy:")
    print("  State: (quality_level, question_type, confidence_level)")
    print("  Actions: full_marks, high_partial, low_partial, zero, review")
    
    print("\nLearned Policy (after training):")
    policy = agent.get_policy_summary()
    for state, info in list(policy.items())[:5]:
        print(f"  {state} → {info['best_action']} (Q={info['q_value']:.1f})")
        
    print("\nTesting Q-Learning Agent:")
    
    test_cases = [
        {'sim': 0.9, 'kw': 0.85, 'type': 'definition', 'desc': 'Good answer'},
        {'sim': 0.5, 'kw': 0.5, 'type': 'definition', 'desc': 'Partial'},
        {'sim': 0.1, 'kw': 0.1, 'type': 'math', 'desc': 'Wrong'},
    ]
    
    for test in test_cases:
        result = agent.grade(test['sim'], test['kw'], test['type'], max_marks=5)
        print(f"\n  {test['desc']}:")
        print(f"    Input: sim={test['sim']}, kw={test['kw']}")
        print(f"    Action: {result['action']} → Marks: {result['marks']}/5")
        
    print("\n✅ Q-Learning agent working correctly!")


def demo_full_grading():
    """Demonstrate complete grading pipeline"""
    print_header("COMPLETE GRADING DEMO")
    
    grader = ExamGrader()
    
    # Sample exam
    exam_text = """
Q1: What is Artificial Intelligence?
A: AI is the simulation of human intelligence in machines.

Q2: Calculate: 15 + 27 = ?
A: 42

Q3: What is the capital of France?
A: Paris

Q4: Define BFS algorithm.
A: Breadth First Search explores all neighbors at current depth before moving to next level.

Q5: What is 2x + 3 = 11? Find x.
A: x = 4
    """
    
    print("\nGrading sample exam paper...")
    print("-" * 40)
    
    results = grader.grade(exam_text, algorithm="A* Search")
    
    print(f"\n📊 Results:")
    print(f"  Total: {results['total_marks']}/{results['total_max_marks']}")
    print(f"  Percentage: {results['percentage']}%")
    print(f"  Grade: {results['grade']}")
    
    summary = results['summary']
    print(f"\n  ✅ Correct: {summary['correct']}")
    print(f"  ⚠️ Partial: {summary['partial']}")
    print(f"  ❌ Incorrect: {summary['incorrect']}")
    
    print("\nQuestion-wise:")
    for q in results['questions']:
        print(f"  Q{q['question_number']}: {q['icon']} {q['marks']}/{q['max_marks']} - {q['status']}")
        
    print("\n✅ Full grading pipeline working!")


def main():
    print("\n" + "=" * 60)
    print("  🎓 AI EXAM CORRECTOR - DEMO")
    print("  Introduction to Artificial Intelligence")
    print("=" * 60)
    
    # Run all demos
    demo_search_algorithms()
    demo_csp()
    demo_bayesian()
    demo_qlearning()
    demo_full_grading()
    
    print("\n" + "=" * 60)
    print("  ✅ ALL DEMOS COMPLETED SUCCESSFULLY!")
    print("  All 4 units of the syllabus are covered.")
    print("=" * 60)
    
    print("\n📌 To run the full GUI application:")
    print("   python main.py")
    print()


if __name__ == "__main__":
    main()
