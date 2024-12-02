import numpy as np
import random

# Define a class for the Adaptive Assessment System
class AdaptiveAssessment:
    def __init__(self, num_questions, num_difficulties):
        self.num_questions = num_questions
        self.num_difficulties = num_difficulties
        self.question_pool = self.generate_question_pool()
        self.alpha_prior = np.ones(num_difficulties)  # Prior successes for each difficulty
        self.beta_prior = np.ones(num_difficulties)   # Prior failures for each difficulty
        self.current_difficulty = 0  # Start with the easiest difficulty
        self.past_performance = []  # Store past performance for tracking

    def generate_question_pool(self):
        # Generate a pool of questions with varying difficulties
        return {
            # difficulty: [f"Q{i+1}_d{difficulty}" for i in range(self.num_questions)]
            difficulty: [f"Q{i+1}d{difficulty}" for i in range(self.num_questions)]
            for difficulty in range(self.num_difficulties)
        }

    def get_next_question(self):
        # Get the next question based on the current difficulty
        return random.choice(self.question_pool[self.current_difficulty])

    def update_proficiency(self, correct):
        # Update the proficiency based on the student's answer and a random chance
        self.past_performance.append((self.current_difficulty, correct))
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

    def predict_performance(self):
        # Generate a random probability of success for the current difficulty level
        success_probability = np.random.uniform(0.5, 1.0)  # Random probability between 0.5 and 1.0
        return np.random.rand() < success_probability  # Simulate the answer based on the probability

# Simulate the adaptive assessment process
def simulate_adaptive_assessment(num_students, num_questions, num_difficulties):
    for student_id in range(num_students):
        print(f"\nStudent {student_id + 1} Assessment:")
        assessment = AdaptiveAssessment(num_questions, num_difficulties)
        
        for question_id in range(num_questions):
            question = assessment.get_next_question()
            # print("  ", end="")
            print(f"{question}", end="")
            
            # Use the random probability to predict the answer
            correct = assessment.predict_performance()
            # print(f"  Predicted Answer: {'Correct' if correct else 'Incorrect'}")
            print("+" if correct else "_", end=" ")
            
            # Update proficiency based on the predicted answer
            assessment.update_proficiency(correct)
        
        # Display proficiency estimates after the assessment
        proficiency_estimates = assessment.get_proficiency_estimate()
        print("\n  Proficiency Estimates:", proficiency_estimates)

# Parameters
num_students = 500
num_questions = 100
num_difficulties = 3

# Run the simulation
simulate_adaptive_assessment(num_students, num_questions, num_difficulties)
