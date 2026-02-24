"""
Q-Learning Grading Agent - Unit IV
===================================
Reinforcement Learning approach to improve grading accuracy over time.

Implements:
- State: (answer_quality, question_type, confidence_level)
- Actions: (full_marks, partial_marks, zero_marks, request_review)
- Rewards: Based on teacher feedback
- Q-Learning update rule
"""

import random
import json
import os


class QLearningGrader:
    """
    Q-Learning Agent for Adaptive Grading
    Implements Unit IV: Reinforcement Learning concepts
    
    The agent learns optimal grading policies through experience.
    """
    
    def __init__(self, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        """
        Initialize Q-Learning agent
        
        Args:
            learning_rate (alpha): How quickly to update Q-values
            discount_factor (gamma): Importance of future rewards
            epsilon: Exploration rate for epsilon-greedy
        """
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        
        # Q-table: Q[state][action] = value
        self.Q = {}
        
        # Define state space discretization
        self.quality_levels = ['low', 'medium', 'high']  # Answer quality
        self.question_types = ['factual', 'definition', 'math', 'essay']
        self.confidence_levels = ['low', 'medium', 'high']
        
        # Define actions
        self.actions = ['full_marks', 'high_partial', 'low_partial', 'zero', 'review']
        
        # Action to marks mapping (percentage of max)
        self.action_marks = {
            'full_marks': 1.0,
            'high_partial': 0.7,
            'low_partial': 0.4,
            'zero': 0.0,
            'review': 0.5  # Default for review
        }
        
        # Training history
        self.history = []
        self.total_reward = 0
        
    def discretize_state(self, similarity, keyword_score, question_type='definition'):
        """
        Convert continuous features to discrete state
        
        Args:
            similarity: 0-1 text similarity score
            keyword_score: 0-1 keyword match score
            question_type: Type of question
            
        Returns:
            Tuple representing discrete state
        """
        # Discretize quality (average of similarity and keywords)
        quality = (similarity + keyword_score) / 2
        if quality >= 0.7:
            quality_level = 'high'
        elif quality >= 0.4:
            quality_level = 'medium'
        else:
            quality_level = 'low'
            
        # Discretize confidence
        confidence = min(similarity, keyword_score)
        if confidence >= 0.7:
            confidence_level = 'high'
        elif confidence >= 0.4:
            confidence_level = 'medium'
        else:
            confidence_level = 'low'
            
        # Normalize question type
        if question_type not in self.question_types:
            question_type = 'definition'
            
        return (quality_level, question_type, confidence_level)
        
    def get_q_value(self, state, action):
        """Get Q-value for state-action pair"""
        if state not in self.Q:
            self.Q[state] = {a: 0.0 for a in self.actions}
        return self.Q[state][action]
        
    def choose_action(self, state):
        """
        Choose action using epsilon-greedy policy
        
        With probability epsilon: explore (random action)
        With probability 1-epsilon: exploit (best known action)
        """
        if random.random() < self.epsilon:
            # Explore: random action
            return random.choice(self.actions)
        else:
            # Exploit: best action based on Q-values
            if state not in self.Q:
                self.Q[state] = {a: 0.0 for a in self.actions}
            return max(self.Q[state], key=self.Q[state].get)
            
    def update(self, state, action, reward, next_state=None):
        """
        Update Q-value using Q-learning update rule
        
        Q(s,a) = Q(s,a) + α * (r + γ * max Q(s',a') - Q(s,a))
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state (optional, for terminal states)
        """
        # Initialize if needed
        if state not in self.Q:
            self.Q[state] = {a: 0.0 for a in self.actions}
            
        # Get current Q-value
        current_q = self.Q[state][action]
        
        # Get max future Q-value
        if next_state is None:
            max_future_q = 0  # Terminal state
        else:
            if next_state not in self.Q:
                self.Q[next_state] = {a: 0.0 for a in self.actions}
            max_future_q = max(self.Q[next_state].values())
            
        # Q-learning update
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        
        self.Q[state][action] = new_q
        
        # Record history
        self.history.append({
            'state': state,
            'action': action,
            'reward': reward,
            'q_value': new_q
        })
        
        self.total_reward += reward
        
    def grade(self, similarity, keyword_score, question_type='definition', max_marks=10):
        """
        Grade an answer using learned policy
        
        Args:
            similarity: Text similarity score
            keyword_score: Keyword match score
            question_type: Type of question
            max_marks: Maximum possible marks
            
        Returns:
            Grading result with marks and action taken
        """
        # Get state
        state = self.discretize_state(similarity, keyword_score, question_type)
        
        # Choose action
        action = self.choose_action(state)
        
        # Calculate marks
        marks_percentage = self.action_marks[action]
        marks = round(max_marks * marks_percentage, 1)
        
        return {
            'marks': marks,
            'max_marks': max_marks,
            'action': action,
            'state': state,
            'q_value': self.get_q_value(state, action),
            'method': 'Q-Learning'
        }
        
    def receive_feedback(self, state, action, teacher_marks, ai_marks, max_marks):
        """
        Learn from teacher feedback
        
        Reward function:
        - Positive reward if AI grade matches teacher grade
        - Negative reward if AI grade differs significantly
        """
        difference = abs(ai_marks - teacher_marks)
        max_difference = max_marks
        
        # Reward: Higher when difference is smaller
        # Range: -10 (completely wrong) to +10 (perfect match)
        normalized_diff = difference / max_difference
        reward = 10 * (1 - 2 * normalized_diff)
        
        # Update Q-value
        self.update(state, action, reward)
        
        return reward
        
    def train_on_examples(self, examples):
        """
        Train the agent on a batch of graded examples
        
        Args:
            examples: List of dicts with:
                - similarity, keyword_score, question_type
                - correct_marks, max_marks
        """
        for example in examples:
            state = self.discretize_state(
                example['similarity'],
                example['keyword_score'],
                example.get('question_type', 'definition')
            )
            
            # What action would give correct marks?
            correct_percentage = example['correct_marks'] / example['max_marks']
            
            # Find closest action
            if correct_percentage >= 0.9:
                correct_action = 'full_marks'
            elif correct_percentage >= 0.6:
                correct_action = 'high_partial'
            elif correct_percentage >= 0.3:
                correct_action = 'low_partial'
            else:
                correct_action = 'zero'
                
            # Train with positive reward for correct action
            # This is supervised learning disguised as RL
            for action in self.actions:
                if action == correct_action:
                    self.update(state, action, reward=10)
                else:
                    # Small negative reward for wrong actions
                    self.update(state, action, reward=-2)
                    
    def get_policy_summary(self):
        """Get summary of learned policy"""
        policy = {}
        
        for state in self.Q:
            best_action = max(self.Q[state], key=self.Q[state].get)
            policy[state] = {
                'best_action': best_action,
                'q_value': self.Q[state][best_action]
            }
            
        return policy
        
    def save_model(self, filepath):
        """Save Q-table to file"""
        # Convert tuple keys to strings for JSON
        serializable_Q = {}
        for state, actions in self.Q.items():
            state_str = str(state)
            serializable_Q[state_str] = actions
            
        with open(filepath, 'w') as f:
            json.dump(serializable_Q, f, indent=2)
            
    def load_model(self, filepath):
        """Load Q-table from file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                serializable_Q = json.load(f)
                
            # Convert string keys back to tuples
            self.Q = {}
            for state_str, actions in serializable_Q.items():
                state = eval(state_str)  # Convert string back to tuple
                self.Q[state] = actions
                
    def decay_epsilon(self, decay_rate=0.99):
        """Reduce exploration over time"""
        self.epsilon *= decay_rate
        self.epsilon = max(0.01, self.epsilon)  # Minimum exploration


# Pre-trained agent with some examples
def get_pretrained_agent():
    """Get a pre-trained Q-learning agent"""
    agent = QLearningGrader()
    
    # Training examples from AI course
    training_examples = [
        # Good answers - definition type
        {'similarity': 0.9, 'keyword_score': 0.85, 'question_type': 'definition', 
         'correct_marks': 5, 'max_marks': 5},
        {'similarity': 0.85, 'keyword_score': 0.9, 'question_type': 'definition', 
         'correct_marks': 5, 'max_marks': 5},
        
        # Partial answers
        {'similarity': 0.6, 'keyword_score': 0.7, 'question_type': 'definition', 
         'correct_marks': 3.5, 'max_marks': 5},
        {'similarity': 0.5, 'keyword_score': 0.5, 'question_type': 'definition', 
         'correct_marks': 2.5, 'max_marks': 5},
        
        # Poor answers
        {'similarity': 0.2, 'keyword_score': 0.3, 'question_type': 'definition', 
         'correct_marks': 1, 'max_marks': 5},
        {'similarity': 0.1, 'keyword_score': 0.1, 'question_type': 'definition', 
         'correct_marks': 0, 'max_marks': 5},
        
        # Math questions
        {'similarity': 1.0, 'keyword_score': 1.0, 'question_type': 'math', 
         'correct_marks': 3, 'max_marks': 3},
        {'similarity': 0.0, 'keyword_score': 0.0, 'question_type': 'math', 
         'correct_marks': 0, 'max_marks': 3},
        
        # Factual questions
        {'similarity': 0.95, 'keyword_score': 1.0, 'question_type': 'factual', 
         'correct_marks': 2, 'max_marks': 2},
        {'similarity': 0.0, 'keyword_score': 0.0, 'question_type': 'factual', 
         'correct_marks': 0, 'max_marks': 2},
    ]
    
    # Train multiple epochs
    for epoch in range(10):
        random.shuffle(training_examples)
        agent.train_on_examples(training_examples)
        agent.decay_epsilon()
        
    return agent


# For testing
if __name__ == "__main__":
    print("Testing Q-Learning Grader (Unit IV)")
    print("=" * 60)
    
    # Create and train agent
    agent = get_pretrained_agent()
    
    print("\nLearned Policy:")
    policy = agent.get_policy_summary()
    for state, info in policy.items():
        print(f"  State {state}: {info['best_action']} (Q={info['q_value']:.2f})")
        
    print("\n" + "-" * 60)
    print("\nTest Grading:")
    
    # Test cases
    test_cases = [
        {'similarity': 0.9, 'keyword_score': 0.85, 'q_type': 'definition'},
        {'similarity': 0.5, 'keyword_score': 0.6, 'q_type': 'definition'},
        {'similarity': 0.2, 'keyword_score': 0.1, 'q_type': 'math'},
    ]
    
    for i, test in enumerate(test_cases, 1):
        result = agent.grade(
            test['similarity'],
            test['keyword_score'],
            test['q_type'],
            max_marks=5
        )
        print(f"\nTest {i}:")
        print(f"  Input: sim={test['similarity']}, kw={test['keyword_score']}")
        print(f"  Action: {result['action']}")
        print(f"  Marks: {result['marks']}/{result['max_marks']}")
    
    print(f"\n\nTotal Episodes: {len(agent.history)}")
    print(f"Total Reward: {agent.total_reward:.1f}")
