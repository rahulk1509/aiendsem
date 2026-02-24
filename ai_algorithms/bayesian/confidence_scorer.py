"""
Bayesian Confidence Scorer - Unit III
======================================
Uses Bayesian probability for:
- OCR confidence estimation
- Partial marks calculation
- Answer correctness probability

Implements concepts from Unit III:
- Conditional probability
- Bayesian inference
- Probability tables (CPTs)
"""

import random


class ConfidenceScorer:
    """
    Bayesian confidence scoring for exam grading
    Implements Unit III: Uncertainty handling with Bayesian Networks
    """
    
    def __init__(self):
        # Prior probabilities
        self.P_correct_prior = 0.5  # Prior: 50% chance answer is correct
        
        # Conditional probability tables (CPTs)
        # P(feature | correct)
        self.cpt_keyword_match = {
            'high': {'correct': 0.9, 'incorrect': 0.3},
            'medium': {'correct': 0.6, 'incorrect': 0.5},
            'low': {'correct': 0.2, 'incorrect': 0.7}
        }
        
        self.cpt_similarity = {
            'high': {'correct': 0.95, 'incorrect': 0.1},
            'medium': {'correct': 0.6, 'incorrect': 0.4},
            'low': {'correct': 0.1, 'incorrect': 0.8}
        }
        
        self.cpt_length_appropriate = {
            True: {'correct': 0.8, 'incorrect': 0.4},
            False: {'correct': 0.3, 'incorrect': 0.6}
        }
        
    def categorize_score(self, score):
        """Categorize a 0-1 score into high/medium/low"""
        if score >= 0.7:
            return 'high'
        elif score >= 0.4:
            return 'medium'
        else:
            return 'low'
            
    def bayesian_update(self, prior, likelihood_correct, likelihood_incorrect):
        """
        Apply Bayes' theorem to update probability
        
        P(correct | evidence) = P(evidence | correct) * P(correct) / P(evidence)
        
        Args:
            prior: Prior probability P(correct)
            likelihood_correct: P(evidence | correct)
            likelihood_incorrect: P(evidence | incorrect)
            
        Returns:
            Posterior probability P(correct | evidence)
        """
        # P(evidence) = P(evidence|correct)*P(correct) + P(evidence|incorrect)*P(incorrect)
        p_evidence = (likelihood_correct * prior) + (likelihood_incorrect * (1 - prior))
        
        # Avoid division by zero
        if p_evidence == 0:
            return prior
            
        # Bayes' theorem
        posterior = (likelihood_correct * prior) / p_evidence
        
        return posterior
        
    def calculate_confidence(self, keyword_score, similarity_score, length_appropriate=True):
        """
        Calculate confidence that answer is correct using Bayesian inference
        
        Uses multiple evidence sources:
        1. Keyword match score
        2. Text similarity score
        3. Whether answer length is appropriate
        
        Args:
            keyword_score: 0-1 score for keyword matching
            similarity_score: 0-1 score for text similarity
            length_appropriate: Boolean for length check
            
        Returns:
            dict with confidence details
        """
        # Start with prior
        current_prob = self.P_correct_prior
        
        # Update with keyword evidence
        kw_category = self.categorize_score(keyword_score)
        current_prob = self.bayesian_update(
            current_prob,
            self.cpt_keyword_match[kw_category]['correct'],
            self.cpt_keyword_match[kw_category]['incorrect']
        )
        
        # Update with similarity evidence
        sim_category = self.categorize_score(similarity_score)
        current_prob = self.bayesian_update(
            current_prob,
            self.cpt_similarity[sim_category]['correct'],
            self.cpt_similarity[sim_category]['incorrect']
        )
        
        # Update with length evidence
        current_prob = self.bayesian_update(
            current_prob,
            self.cpt_length_appropriate[length_appropriate]['correct'],
            self.cpt_length_appropriate[length_appropriate]['incorrect']
        )
        
        return {
            'confidence': current_prob,
            'keyword_evidence': kw_category,
            'similarity_evidence': sim_category,
            'length_appropriate': length_appropriate,
            'interpretation': self.interpret_confidence(current_prob)
        }
        
    def interpret_confidence(self, confidence):
        """Interpret confidence score"""
        if confidence >= 0.9:
            return "Very High - Almost certainly correct"
        elif confidence >= 0.75:
            return "High - Likely correct"
        elif confidence >= 0.5:
            return "Medium - Possibly correct, needs review"
        elif confidence >= 0.25:
            return "Low - Likely incorrect"
        else:
            return "Very Low - Almost certainly incorrect"
            
    def calculate_partial_marks(self, max_marks, keyword_score, similarity_score, 
                                 completeness=1.0, has_steps=True):
        """
        Calculate partial marks using probability theory
        
        P(marks | evidence) based on multiple factors
        
        Args:
            max_marks: Maximum marks for question
            keyword_score: Keyword matching score (0-1)
            similarity_score: Text similarity score (0-1)
            completeness: How complete the answer is (0-1)
            has_steps: Whether working steps are shown
            
        Returns:
            dict with marks and breakdown
        """
        # Calculate confidence
        length_ok = completeness > 0.3
        confidence = self.calculate_confidence(keyword_score, similarity_score, length_ok)
        
        # Base marks from confidence
        base_marks = max_marks * confidence['confidence']
        
        # Adjust for completeness
        completeness_factor = 0.7 + (0.3 * completeness)  # 70% to 100%
        adjusted_marks = base_marks * completeness_factor
        
        # Bonus for showing steps (in math/science)
        if has_steps and confidence['confidence'] > 0.5:
            adjusted_marks = min(max_marks, adjusted_marks * 1.1)  # 10% bonus
            
        # Round to nearest 0.5
        final_marks = round(adjusted_marks * 2) / 2
        final_marks = max(0, min(max_marks, final_marks))
        
        return {
            'marks': final_marks,
            'max_marks': max_marks,
            'percentage': (final_marks / max_marks * 100) if max_marks > 0 else 0,
            'confidence': confidence['confidence'],
            'breakdown': {
                'keyword_contribution': keyword_score * 0.3,
                'similarity_contribution': similarity_score * 0.4,
                'completeness_contribution': completeness * 0.2,
                'steps_bonus': 0.1 if has_steps else 0
            },
            'interpretation': confidence['interpretation']
        }
        
    def ocr_confidence(self, image_quality='medium', handwriting_clarity='medium'):
        """
        Calculate OCR reading confidence using Bayesian network
        
        P(correct_reading | image_quality, handwriting_clarity)
        
        Args:
            image_quality: 'high', 'medium', 'low'
            handwriting_clarity: 'high', 'medium', 'low'
            
        Returns:
            Confidence score for OCR accuracy
        """
        # CPT for OCR accuracy
        quality_probs = {'high': 0.95, 'medium': 0.80, 'low': 0.50}
        clarity_probs = {'high': 0.90, 'medium': 0.70, 'low': 0.40}
        
        # Combined probability (assuming independence)
        p_quality = quality_probs.get(image_quality, 0.8)
        p_clarity = clarity_probs.get(handwriting_clarity, 0.7)
        
        # P(correct) = P(quality) * P(clarity) with some base success
        base_success = 0.6
        combined = base_success + (1 - base_success) * (p_quality * p_clarity)
        
        return {
            'ocr_confidence': combined,
            'image_quality_factor': p_quality,
            'handwriting_factor': p_clarity,
            'recommendation': self.ocr_recommendation(combined)
        }
        
    def ocr_recommendation(self, confidence):
        """Recommend action based on OCR confidence"""
        if confidence >= 0.85:
            return "High confidence - proceed with auto-grading"
        elif confidence >= 0.65:
            return "Medium confidence - review flagged answers"
        else:
            return "Low confidence - manual review recommended"


# For testing
if __name__ == "__main__":
    scorer = ConfidenceScorer()
    
    print("Testing Bayesian Confidence Scorer")
    print("=" * 60)
    
    # Test confidence calculation
    print("\n1. Answer Confidence Test:")
    result = scorer.calculate_confidence(
        keyword_score=0.8,
        similarity_score=0.75,
        length_appropriate=True
    )
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Interpretation: {result['interpretation']}")
    
    # Test partial marks
    print("\n2. Partial Marks Test:")
    marks = scorer.calculate_partial_marks(
        max_marks=10,
        keyword_score=0.7,
        similarity_score=0.6,
        completeness=0.8,
        has_steps=True
    )
    print(f"   Marks: {marks['marks']}/{marks['max_marks']}")
    print(f"   Percentage: {marks['percentage']:.1f}%")
    print(f"   Confidence: {marks['confidence']:.2%}")
    
    # Test OCR confidence
    print("\n3. OCR Confidence Test:")
    ocr = scorer.ocr_confidence(
        image_quality='medium',
        handwriting_clarity='high'
    )
    print(f"   OCR Confidence: {ocr['ocr_confidence']:.2%}")
    print(f"   Recommendation: {ocr['recommendation']}")
