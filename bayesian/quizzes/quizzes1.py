import numpy as np
import random
from scipy.stats import beta

# Define a class for the Adaptive Assessment System
class AdaptiveAssessment:
    def __init__(self, num_questions, num_difficulties):
        self.num_questions = num_questions
        self.num_difficulties = num_difficulties
        self.question_pool = self.generate_question_pool()
        self.alpha_prior = np.ones(num_difficulties)  # Prior successes for each difficulty
        self.beta_prior = np.ones(num_difficulties)   # Prior failures for each difficulty
        self.current_difficulty = 0  # Start with the easiest difficulty

    def generate_question_pool(self):
        # Generate a pool of questions with varying difficulties
        return {
            difficulty: [f"Question {i+1} (Difficulty {difficulty})" for i in range(self.num_questions)]
            for difficulty in range(self.num_difficulties)
        }

    def get_next_question(self):
        # Get the next question based on the current difficulty
        return random.choice(self.question_pool[self.current_difficulty])

    def update_proficiency(self, correct):
        # Update the proficiency based on the student's answer
        if correct:
            self.alpha_prior[self.current_difficulty] += 1
            # Move to a more difficult question if possible
            if self.current_difficulty < self.num_difficulties - 1:
                self.current_difficulty += 1
        else:
            self.beta_prior[self.current_difficulty] += 1
            # Move to an easier question if possible
            if self.current_difficulty > 0:
                self.current_difficulty -= 1

    def get_proficiency_estimate(self):
        # Calculate the mean proficiency for each difficulty level
        return self.alpha_prior / (self.alpha_prior + self.beta_prior)

# Simulate the adaptive assessment process
def simulate_adaptive_assessment(num_students, num_questions, num_difficulties):
    for student_id in range(num_students):
        print(f"\nStudent {student_id + 1} Assessment:")
        assessment = AdaptiveAssessment(num_questions, num_difficulties)
        
        for question_id in range(num_questions):
            question = assessment.get_next_question()
            print(f"  {question}")
            
            # Simulate a student's answer (randomly for demonstration)
            correct = random.choice([True, False])  # Randomly simulate correct/incorrect
            print(f"  Answer: {'Correct' if correct else 'Incorrect'}")
            
            # Update proficiency based on the answer
            assessment.update_proficiency(correct)
        
        # Display proficiency estimates after the assessment
        proficiency_estimates = assessment.get_proficiency_estimate()
        print("  Proficiency Estimates:", proficiency_estimates)

# Parameters
num_students = 5
num_questions = 10
num_difficulties = 3

# Run the simulation
simulate_adaptive_assessment(num_students, num_questions, num_difficulties)
