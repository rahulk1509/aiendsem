"""
CSP Rubric Grader - Unit II
============================
Constraint Satisfaction Problem approach to grading.

Implements:
- Variables: Score components (content, accuracy, completeness)
- Domains: Possible mark values
- Constraints: Grading rules and rubric requirements
- Backtracking search to find valid grade assignment
"""


class RubricCSP:
    """
    Constraint Satisfaction Problem for Rubric-based Grading
    Implements Unit II: CSP concepts with backtracking search
    """
    
    def __init__(self):
        # Define grading components (variables)
        self.variables = ['content_score', 'accuracy_score', 'completeness_score', 'presentation_score']
        
    def get_domain(self, max_marks, granularity=0.5):
        """
        Get domain of possible values for a variable
        
        Args:
            max_marks: Maximum possible marks
            granularity: Step size (0.5 = half marks allowed)
            
        Returns:
            List of possible mark values
        """
        domain = []
        current = 0
        while current <= max_marks:
            domain.append(current)
            current += granularity
        return domain
        
    def check_constraint(self, assignment, constraint_type, **kwargs):
        """
        Check if an assignment satisfies a constraint
        
        Constraint types:
        - 'total_max': Total score must not exceed maximum
        - 'dependency': If accuracy is 0, content can't be full
        - 'minimum': All scores must be >= 0
        - 'consistency': Related scores should be consistent
        """
        if constraint_type == 'total_max':
            total = sum(assignment.values())
            max_allowed = kwargs.get('max_marks', 10)
            return total <= max_allowed
            
        elif constraint_type == 'dependency':
            # If accuracy is 0, content can't be higher than 50% max
            accuracy = assignment.get('accuracy_score', 0)
            content = assignment.get('content_score', 0)
            max_content = kwargs.get('max_content', 5)
            
            if accuracy == 0:
                return content <= max_content * 0.5
            return True
            
        elif constraint_type == 'minimum':
            return all(v >= 0 for v in assignment.values())
            
        elif constraint_type == 'consistency':
            # High accuracy should mean decent content
            accuracy = assignment.get('accuracy_score', 0)
            content = assignment.get('content_score', 0)
            max_accuracy = kwargs.get('max_accuracy', 5)
            
            if accuracy >= max_accuracy * 0.8:
                return content >= 1
            return True
            
        return True
        
    def is_consistent(self, assignment, max_marks=10):
        """
        Check if current assignment is consistent with all constraints
        """
        constraints = [
            ('total_max', {'max_marks': max_marks}),
            ('minimum', {}),
            ('dependency', {'max_content': max_marks * 0.4}),
            ('consistency', {'max_accuracy': max_marks * 0.4})
        ]
        
        return all(
            self.check_constraint(assignment, ctype, **params)
            for ctype, params in constraints
        )
        
    def backtracking_grade(self, evidence, max_marks=10):
        """
        Use backtracking search to find valid grade assignment
        
        This is the main CSP solving algorithm from Unit II.
        
        Args:
            evidence: Dict with evidence about answer quality
                - keyword_match: 0-1 score
                - similarity: 0-1 score
                - length_appropriate: boolean
                - has_steps: boolean (for math)
            max_marks: Maximum total marks
            
        Returns:
            Valid assignment of marks to components
        """
        # Calculate target scores based on evidence
        keyword_score = evidence.get('keyword_match', 0.5)
        similarity = evidence.get('similarity', 0.5)
        length_ok = evidence.get('length_appropriate', True)
        has_steps = evidence.get('has_steps', False)
        
        # Define component weights
        weights = {
            'content_score': 0.35,
            'accuracy_score': 0.40,
            'completeness_score': 0.15,
            'presentation_score': 0.10
        }
        
        # Initial assignment based on evidence
        assignment = {}
        
        # Accuracy based on similarity
        max_accuracy = max_marks * weights['accuracy_score']
        assignment['accuracy_score'] = round(similarity * max_accuracy, 1)
        
        # Content based on keywords
        max_content = max_marks * weights['content_score']
        assignment['content_score'] = round(keyword_score * max_content, 1)
        
        # Completeness based on length
        max_completeness = max_marks * weights['completeness_score']
        completeness_factor = 1.0 if length_ok else 0.5
        assignment['completeness_score'] = round(completeness_factor * max_completeness, 1)
        
        # Presentation (bonus for showing steps in math)
        max_presentation = max_marks * weights['presentation_score']
        presentation_factor = 1.0 if has_steps else 0.5
        assignment['presentation_score'] = round(presentation_factor * max_presentation, 1)
        
        # Backtracking adjustment if constraints violated
        assignment = self._backtrack_adjust(assignment, max_marks)
        
        return assignment
        
    def _backtrack_adjust(self, assignment, max_marks):
        """
        Adjust assignment using backtracking if constraints violated
        """
        max_iterations = 100
        iteration = 0
        
        while not self.is_consistent(assignment, max_marks) and iteration < max_iterations:
            iteration += 1
            
            # Check total constraint
            total = sum(assignment.values())
            if total > max_marks:
                # Reduce scores proportionally
                factor = max_marks / total
                for key in assignment:
                    assignment[key] = round(assignment[key] * factor, 1)
                    
            # Check dependency constraint
            if assignment.get('accuracy_score', 0) == 0:
                max_content = max_marks * 0.35 * 0.5
                if assignment.get('content_score', 0) > max_content:
                    assignment['content_score'] = max_content
                    
        return assignment
        
    def grade_with_rubric(self, evidence, rubric=None, max_marks=10):
        """
        Grade using rubric-based CSP
        
        Args:
            evidence: Evidence about answer quality
            rubric: Custom rubric (optional)
            max_marks: Maximum marks
            
        Returns:
            Grading result with breakdown
        """
        # Get assignment using backtracking
        assignment = self.backtracking_grade(evidence, max_marks)
        
        # Calculate total
        total_marks = sum(assignment.values())
        total_marks = min(max_marks, total_marks)  # Cap at max
        
        # Round to nearest 0.5
        total_marks = round(total_marks * 2) / 2
        
        return {
            'total_marks': total_marks,
            'max_marks': max_marks,
            'breakdown': assignment,
            'percentage': (total_marks / max_marks * 100) if max_marks > 0 else 0,
            'constraints_satisfied': self.is_consistent(assignment, max_marks),
            'method': 'CSP Backtracking'
        }


class MCQGraderCSP:
    """
    CSP approach for MCQ grading
    Simple constraint: student_answer == correct_answer
    """
    
    def __init__(self):
        pass
        
    def grade_mcq(self, student_answers, answer_key, marks_per_question=1):
        """
        Grade MCQ using constraint satisfaction
        
        Each question is a constraint:
        - Variable: student_answer[i]
        - Domain: {A, B, C, D}
        - Constraint: student_answer[i] == correct_answer[i]
        """
        results = []
        total_marks = 0
        max_marks = len(answer_key) * marks_per_question
        
        for q_num, correct in answer_key.items():
            student_ans = student_answers.get(q_num, '')
            
            # Check constraint
            is_correct = student_ans.upper() == correct.upper()
            marks = marks_per_question if is_correct else 0
            
            results.append({
                'question': q_num,
                'student_answer': student_ans,
                'correct_answer': correct,
                'is_correct': is_correct,
                'marks': marks
            })
            
            total_marks += marks
            
        return {
            'results': results,
            'total_marks': total_marks,
            'max_marks': max_marks,
            'percentage': (total_marks / max_marks * 100) if max_marks > 0 else 0
        }


# For testing
if __name__ == "__main__":
    csp = RubricCSP()
    
    print("Testing CSP Rubric Grader (Unit II)")
    print("=" * 60)
    
    # Test case 1: Good answer
    evidence1 = {
        'keyword_match': 0.8,
        'similarity': 0.85,
        'length_appropriate': True,
        'has_steps': True
    }
    
    result1 = csp.grade_with_rubric(evidence1, max_marks=10)
    print("\nTest 1: Good Answer")
    print(f"  Total: {result1['total_marks']}/{result1['max_marks']}")
    print(f"  Breakdown: {result1['breakdown']}")
    print(f"  Constraints OK: {result1['constraints_satisfied']}")
    
    # Test case 2: Partial answer
    evidence2 = {
        'keyword_match': 0.5,
        'similarity': 0.4,
        'length_appropriate': True,
        'has_steps': False
    }
    
    result2 = csp.grade_with_rubric(evidence2, max_marks=10)
    print("\nTest 2: Partial Answer")
    print(f"  Total: {result2['total_marks']}/{result2['max_marks']}")
    print(f"  Breakdown: {result2['breakdown']}")
    
    # Test MCQ grader
    print("\n" + "=" * 60)
    print("Testing MCQ CSP Grader")
    
    mcq_grader = MCQGraderCSP()
    answer_key = {'Q1': 'B', 'Q2': 'A', 'Q3': 'C', 'Q4': 'D'}
    student_answers = {'Q1': 'B', 'Q2': 'A', 'Q3': 'B', 'Q4': 'D'}  # Q3 wrong
    
    mcq_result = mcq_grader.grade_mcq(student_answers, answer_key)
    print(f"  Score: {mcq_result['total_marks']}/{mcq_result['max_marks']}")
    print(f"  Percentage: {mcq_result['percentage']}%")
