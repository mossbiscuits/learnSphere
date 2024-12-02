import numpy as np
import random

class AdaptiveAssessment:
    def __init__(self, num_questions, num_difficulties, epsilon=0.1, proficiency_threshold=0.9):
        self.num_questions = num_questions
        self.num_difficulties = num_difficulties
        self.epsilon = epsilon
        self.proficiency_threshold = proficiency_threshold
        self.question_pool = self.generate_question_pool()
        self.alpha_prior = np.ones(num_difficulties)
        self.beta_prior = np.ones(num_difficulties)
        self.current_difficulty = 0
        self.past_performance = []
        self.scores_per_difficulty = np.zeros(num_difficulties)  # Store scores for each difficulty
        self.proficiency_estimates_per_difficulty = [[] for _ in range(num_difficulties)]  # Store proficiency estimates
        self.score = 0
        self.true_proficiency = min(0.95, np.random.normal(0.8, 0.1))

    def generate_question_pool(self):
        return {
            difficulty: [f"Q{i+1}d{difficulty}" for i in range(self.num_questions)]
            for difficulty in range(self.num_difficulties)
        }

    def get_next_question(self):
        if random.random() < self.epsilon:
            self.current_difficulty = random.randint(0, self.num_difficulties - 1)
        return random.choice(self.question_pool[self.current_difficulty])

    def update_proficiency(self, correct):
        if correct:
            self.alpha_prior[self.current_difficulty] += 1
            self.scores_per_difficulty[self.current_difficulty] += 1
            self.score += 1
            # Increase difficulty more aggressively if performance is good
            if self.score % 3 == 0 and self.current_difficulty < self.num_difficulties - 1:
                self.current_difficulty += 1
        else:
            self.beta_prior[self.current_difficulty] += 1
            # Decrease difficulty more aggressively if performance is poor
            if self.score % 3 == 0 and self.current_difficulty > 0:
                self.current_difficulty -= 1


    def get_proficiency_estimate(self):
        return self.alpha_prior / (self.alpha_prior + self.beta_prior)

    def predict_performance(self):
        proficiency_estimate = self.get_proficiency_estimate()[self.current_difficulty]
        return np.random.rand() < proficiency_estimate

    def assess_student(self):
        for question_id in range(self.num_questions):
            question = self.get_next_question()
            correct = self.predict_performance()
            self.update_proficiency(correct)

            proficiency_estimate = self.get_proficiency_estimate()[self.current_difficulty]
            self.proficiency_estimates_per_difficulty[self.current_difficulty].append(proficiency_estimate)

            if proficiency_estimate >= self.proficiency_threshold and self.score > 20:
                # print(f"  Early termination: Proficiency estimate {proficiency_estimate:.2f} reached.")
                break

        # Decay epsilon over time
        self.epsilon = max(0.01, self.epsilon * 0.95)


def simulate_adaptive_assessment(num_students, num_questions, num_difficulties, strategies):
    results = {strategy['name']: [] for strategy in strategies}

    for strategy in strategies:
        print(f"Testing strategy: {strategy['name']} (epsilon={strategy['epsilon']}, threshold={strategy['threshold']})")
        for student_id in range(num_students):
            assessment = AdaptiveAssessment(num_questions, num_difficulties, 
                                            epsilon=strategy['epsilon'], 
                                            proficiency_threshold=strategy['threshold'])
            assessment.assess_student()
            results[strategy['name']].append((assessment.scores_per_difficulty, assessment.proficiency_estimates_per_difficulty))

    # Calculate and print averages and standard deviations for scores and proficiency estimates
    for strategy_name, scores_and_proficiencies in results.items():
        avg_scores = np.mean([s[0] for s in scores_and_proficiencies], axis=0)
        std_scores = np.std([s[0] for s in scores_and_proficiencies], axis=0)

        # Calculate average and std for proficiency estimates
        avg_proficiencies = np.zeros(num_difficulties)
        std_proficiencies = np.zeros(num_difficulties)

        for difficulty in range(num_difficulties):
            # Extract proficiency estimates for the current difficulty level
            proficiency_estimates = [s[1][difficulty] for s in scores_and_proficiencies]
            # Flatten the list of proficiency estimates
            proficiency_estimates_flat = [item for sublist in proficiency_estimates for item in sublist]
            avg_proficiencies[difficulty] = np.mean(proficiency_estimates_flat)
            std_proficiencies[difficulty] = np.std(proficiency_estimates_flat)

        print(f"\nResults for {strategy_name}:")
        for difficulty in range(num_difficulties):
            print(f"  Difficulty Level {difficulty}:")
            print(f"    Average Score: {avg_scores[difficulty]:.2f}, Std Dev: {std_scores[difficulty]:.2f}")
            print(f"    Average Proficiency: {avg_proficiencies[difficulty]:.2f}, Std Dev: {std_proficiencies[difficulty]:.2f}")

# Parameters
num_students = 500
num_questions = 100
num_difficulties = 5

# Define different strategies to test
strategies = [
    {'name': 'Epsilon-Greedy (0.01)', 'epsilon': 0.01, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.02)', 'epsilon': 0.02, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.05)', 'epsilon': 0.05, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.1)', 'epsilon': 0.1, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.2)', 'epsilon': 0.2, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.3)', 'epsilon': 0.3, 'threshold': 0.9},
    {'name': 'Fixed Difficulty', 'epsilon': 0.0, 'threshold': 0.9},
    {'name': 'High Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.95},
    {'name': 'Low Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.85},
    {'name': 'No Proficiency Threshold', 'epsilon': 0.1, 'threshold': 1.5}, # no early termination
]

# Run the simulation for all strategies
simulate_adaptive_assessment(num_students, num_questions, num_difficulties, strategies)