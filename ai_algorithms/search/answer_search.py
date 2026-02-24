"""
Answer Search Algorithms - Unit I
=================================
Implements BFS, DFS, A*, Greedy search for answer matching.

This module finds the best matching answer from an answer bank
using various search algorithms.

Syllabus Coverage:
- BFS: Breadth-first search through answer space
- DFS: Depth-first exploration of answer variations
- A*: Optimal answer matching with heuristics
- Greedy: Quick keyword-based matching
"""

import re
import heapq
from collections import deque
from difflib import SequenceMatcher


class AnswerSearcher:
    """
    Search algorithms for finding best matching answers
    Implements Unit I concepts: BFS, DFS, A*, Greedy Search
    """
    
    def __init__(self):
        self.nodes_explored = 0
        
    def similarity(self, str1, str2):
        """Calculate similarity between two strings (0 to 1)"""
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        return SequenceMatcher(None, str1, str2).ratio()
        
    def keyword_overlap(self, text, keywords):
        """Calculate keyword overlap score"""
        text_lower = text.lower()
        found = sum(1 for kw in keywords if kw.lower() in text_lower)
        return found / len(keywords) if keywords else 0
        
    # =========================================
    # BFS - Breadth First Search (Unit I)
    # =========================================
    def bfs_search(self, student_answer, answer_bank):
        """
        BFS Search for best matching answer
        
        Explores all answers at current similarity level before
        moving to less similar answers.
        
        Args:
            student_answer: Student's answer text
            answer_bank: List of correct answers
            
        Returns:
            (best_match, similarity_score, nodes_explored)
        """
        self.nodes_explored = 0
        queue = deque()
        
        # Initialize queue with all possible answers
        for answer in answer_bank:
            queue.append(answer)
            
        best_match = None
        best_score = 0
        
        while queue:
            current_answer = queue.popleft()
            self.nodes_explored += 1
            
            # Calculate similarity
            score = self.similarity(student_answer, current_answer)
            
            if score > best_score:
                best_score = score
                best_match = current_answer
                
            # If perfect match found, stop
            if score >= 0.95:
                break
                
        return best_match, best_score, self.nodes_explored
        
    # =========================================
    # DFS - Depth First Search (Unit I)
    # =========================================
    def dfs_search(self, student_answer, answer_bank):
        """
        DFS Search for matching answer
        
        Explores answer variations depth-first.
        Good for finding any valid match quickly.
        
        Args:
            student_answer: Student's answer text
            answer_bank: List of correct answers
            
        Returns:
            (best_match, similarity_score, nodes_explored)
        """
        self.nodes_explored = 0
        stack = list(answer_bank)
        
        best_match = None
        best_score = 0
        
        while stack:
            current_answer = stack.pop()
            self.nodes_explored += 1
            
            score = self.similarity(student_answer, current_answer)
            
            if score > best_score:
                best_score = score
                best_match = current_answer
                
            # Early termination for good match
            if score >= 0.9:
                break
                
        return best_match, best_score, self.nodes_explored
        
    # =========================================
    # A* Search - Best First with Heuristic (Unit I)
    # =========================================
    def astar_search(self, student_answer, answer_bank, keywords=None):
        """
        A* Search for optimal answer matching
        
        Uses heuristic: keyword overlap + partial string match
        f(n) = g(n) + h(n)
        - g(n): Cost so far (1 - similarity found)
        - h(n): Heuristic (estimated similarity based on keywords)
        
        Args:
            student_answer: Student's answer text
            answer_bank: List of correct answers
            keywords: Important keywords to match
            
        Returns:
            (best_match, similarity_score, nodes_explored, path)
        """
        self.nodes_explored = 0
        
        if keywords is None:
            # Extract keywords from student answer
            keywords = self.extract_keywords(student_answer)
            
        # Priority queue: (f_score, answer, g_score)
        # Using negative because heapq is min-heap
        open_set = []
        
        for answer in answer_bank:
            # Heuristic: keyword overlap
            h_score = self.keyword_overlap(answer, keywords)
            # Initial g_score is 0
            f_score = -h_score  # Negative for max-heap behavior
            heapq.heappush(open_set, (f_score, answer, 0))
            
        best_match = None
        best_score = 0
        path = []  # Track exploration path
        
        while open_set:
            f_score, current_answer, g_score = heapq.heappop(open_set)
            self.nodes_explored += 1
            path.append(current_answer[:50] + "...")
            
            # Calculate actual similarity
            similarity_score = self.similarity(student_answer, current_answer)
            
            if similarity_score > best_score:
                best_score = similarity_score
                best_match = current_answer
                
            # If we found a great match, return
            if similarity_score >= 0.85:
                break
                
        return best_match, best_score, self.nodes_explored, path
        
    # =========================================
    # Greedy Search (Unit I)
    # =========================================
    def greedy_search(self, student_answer, answer_bank, keywords=None):
        """
        Greedy Best-First Search
        
        Always picks the answer that looks most promising based on
        keyword heuristic, without considering actual similarity cost.
        
        Args:
            student_answer: Student's answer text
            answer_bank: List of correct answers
            keywords: Keywords to match
            
        Returns:
            (best_match, similarity_score, nodes_explored)
        """
        self.nodes_explored = 0
        
        if keywords is None:
            keywords = self.extract_keywords(student_answer)
            
        # Sort answers by heuristic (keyword overlap)
        scored_answers = []
        for answer in answer_bank:
            h_score = self.keyword_overlap(answer, keywords)
            scored_answers.append((h_score, answer))
            
        scored_answers.sort(reverse=True)
        
        # Greedily pick best heuristic match
        best_match = None
        best_score = 0
        
        for h_score, answer in scored_answers:
            self.nodes_explored += 1
            
            similarity_score = self.similarity(student_answer, answer)
            
            if similarity_score > best_score:
                best_score = similarity_score
                best_match = answer
                
            # Greedy: take first "good enough" match
            if similarity_score >= 0.7:
                break
                
        return best_match, best_score, self.nodes_explored
        
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                      'would', 'could', 'should', 'may', 'might', 'must', 'shall',
                      'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
                      'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
                      'through', 'during', 'before', 'after', 'above', 'below',
                      'between', 'under', 'again', 'further', 'then', 'once',
                      'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
                      'neither', 'not', 'only', 'own', 'same', 'than', 'too',
                      'very', 'just', 'also', 'now', 'it', 'its', 'this', 'that',
                      'these', 'those', 'what', 'which', 'who', 'whom', 'whose'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter stop words and return unique keywords
        keywords = [w for w in words if w not in stop_words]
        return list(set(keywords))
        
    def search(self, student_answer, answer_bank, algorithm="A* Search", keywords=None):
        """
        Main search method - delegates to specific algorithm
        
        Args:
            student_answer: Student's answer
            answer_bank: List of correct answers
            algorithm: Which algorithm to use
            keywords: Optional keywords for matching
            
        Returns:
            dict with match results and statistics
        """
        if algorithm == "BFS":
            match, score, nodes = self.bfs_search(student_answer, answer_bank)
            path = None
        elif algorithm == "DFS":
            match, score, nodes = self.dfs_search(student_answer, answer_bank)
            path = None
        elif algorithm == "Greedy":
            match, score, nodes = self.greedy_search(student_answer, answer_bank, keywords)
            path = None
        else:  # A* Search (default)
            match, score, nodes, path = self.astar_search(student_answer, answer_bank, keywords)
            
        return {
            "best_match": match,
            "similarity_score": score,
            "nodes_explored": nodes,
            "algorithm": algorithm,
            "search_path": path
        }


# For testing
if __name__ == "__main__":
    searcher = AnswerSearcher()
    
    # Test answer bank
    answer_bank = [
        "Artificial Intelligence is the simulation of human intelligence by machines",
        "AI refers to machines that can perform tasks requiring human intelligence",
        "AI is computer systems able to perform tasks normally requiring human intelligence",
        "Machine learning is a subset of AI that enables systems to learn from data",
        "Deep learning uses neural networks with multiple layers"
    ]
    
    student_answer = "AI is the simulation of human intelligence in machines"
    
    print("Testing Search Algorithms")
    print("=" * 60)
    print(f"Student Answer: {student_answer}")
    print()
    
    # Test each algorithm
    for algo in ["BFS", "DFS", "Greedy", "A* Search"]:
        result = searcher.search(student_answer, answer_bank, algo)
        print(f"\n{algo}:")
        print(f"  Best Match: {result['best_match'][:60]}...")
        print(f"  Similarity: {result['similarity_score']:.2%}")
        print(f"  Nodes Explored: {result['nodes_explored']}")
