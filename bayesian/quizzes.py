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
        self.total_correct = 0  # Track total correct answers
        self.total_answered = 0  # Track total questions answered
        self.confidence_score = 1.0

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
        self.total_answered += 1  # Increment total questions answered
        if correct:
            self.total_correct += 1  # Increment total correct answers
            self.alpha_prior[self.current_difficulty] += 1
            self.scores_per_difficulty[self.current_difficulty] += 1
            self.score += 1
            self.confidence_score += 0.1  # Increase confidence on correct answers
            # Increase difficulty more aggressively if performance is good
            if self.score % 3 == 0 and self.current_difficulty < self.num_difficulties - 1:
                self.current_difficulty += 1
        else:
            self.beta_prior[self.current_difficulty] += 1
            self.confidence_score += 0.05
            # Decrease difficulty more aggressively if performance is poor
            if self.score % 3 == 0 and self.current_difficulty > 0:
                self.current_difficulty -= 1

    def get_proficiency_estimate(self):
        return self.alpha_prior / (self.alpha_prior + self.beta_prior)

    def predict_performance(self):
        proficiency_estimate = self.get_proficiency_estimate()[self.current_difficulty]
        adjusted_probability = proficiency_estimate * self.confidence_score  # Adjust by confidence
        adjusted_probability = min(adjusted_probability, 1.0)  # Cap at 1.0
        return np.random.rand() < adjusted_probability

    def assess_student(self):
        for question_id in range(self.num_questions):
            question = self.get_next_question()
            correct = self.predict_performance()
            self.update_proficiency(correct)

            proficiency_estimate = self.get_proficiency_estimate()[self.current_difficulty]
            self.proficiency_estimates_per_difficulty[self.current_difficulty].append(proficiency_estimate)

            if proficiency_estimate >= self.proficiency_threshold and self.total_answered > 20:
                break

        # Decay epsilon over time
        self.epsilon = max(0.01, self.epsilon * 0.95)
        # Calculate the grade as a percentage
        if self.total_answered > 0:
            grade_percentage = (self.total_correct / self.total_answered) * 100

def simulate_adaptive_assessment(num_students, num_questions, num_difficulties, strategies):
    results = {strategy['name']: [] for strategy in strategies}

    # Initialize overall accumulators
    overall_total_score = 0
    overall_total_proficiency = 0
    overall_total_grades = 0
    overall_count = 0

    for strategy in strategies:
        print(f"Testing strategy: {strategy['name']} (epsilon={strategy['epsilon']}, threshold={strategy['threshold']})")
        for student_id in range(num_students):
            assessment = AdaptiveAssessment(num_questions, num_difficulties, 
                                            epsilon=strategy['epsilon'], 
                                            proficiency_threshold=strategy['threshold'])
            assessment.assess_student()
            grade_percentage = (assessment.total_correct / assessment.total_answered) * 100 if assessment.total_answered > 0 else 0
            results[strategy['name']].append((assessment.scores_per_difficulty, assessment.proficiency_estimates_per_difficulty, grade_percentage))

    # Calculate and print averages and standard deviations for scores and proficiency estimates
    for strategy_name, scores_and_proficiencies in results.items():
        avg_scores = np.mean([s[0] for s in scores_and_proficiencies], axis=0)
        std_scores = np.std([s[0] for s in scores_and_proficiencies], axis=0)

        # Calculate average and std for proficiency estimates
        avg_proficiencies = np.zeros(num_difficulties)
        std_proficiencies = np.zeros(num_difficulties)

        for difficulty in range(num_difficulties):
            proficiency_estimates = [s[1][difficulty] for s in scores_and_proficiencies]
            proficiency_estimates_flat = [item for sublist in proficiency_estimates for item in sublist]
            avg_proficiencies[difficulty] = np.mean(proficiency_estimates_flat)
            std_proficiencies[difficulty] = np.std(proficiency_estimates_flat)

        # Calculate overall average score and proficiency
        overall_avg_score = np.mean([s[0].sum() for s in scores_and_proficiencies])  # Total score across difficulties
        overall_avg_proficiency = np.mean(avg_proficiencies)  # Average proficiency across all difficulties
        overall_avg_grades = np.mean([s[2] for s in scores_and_proficiencies])  # Average grades

        # Accumulate overall totals for final summary
        overall_total_score += overall_avg_score
        overall_total_proficiency += overall_avg_proficiency
        overall_total_grades += overall_avg_grades
        overall_count += 1

        print(f"\nResults for {strategy_name}:")
        print(f"  Overall Average Score: {overall_avg_score:.2f}")
        print(f"  Overall Average Proficiency: {overall_avg_proficiency:.2f}")
        print(f"  Overall Average Grade: {overall_avg_grades:.2f}")
        for difficulty in range(num_difficulties):
            print(f"  Difficulty Level {difficulty}:")
            print(f"    Average Score: {avg_scores[difficulty]:.2f}, Std Dev: {std_scores[difficulty]:.2f}")
            print(f"    Average Proficiency: {avg_proficiencies[difficulty]:.2f}, Std Dev: {std_proficiencies[difficulty]:.2f}")

    # Print overall summary
    if overall_count > 0:
        print("\nOverall Summary:")
        print(f"  Overall Average Score across all strategies: {overall_total_score / overall_count:.2f}")
        print(f"  Overall Average Proficiency across all strategies: {overall_total_proficiency / overall_count:.2f}")
        print(f"  Overall Average Grade across all strategies: {overall_total_grades / overall_count:.2f}")

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
    {'name': 'Epsilon-Greedy (0.5)', 'epsilon': 0.5, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.7)', 'epsilon': 0.7, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (0.9)', 'epsilon': 0.9, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (1.0)', 'epsilon': 1.0, 'threshold': 0.9},
    {'name': 'Epsilon-Greedy (2.0)', 'epsilon': 2.0, 'threshold': 0.9},
    {'name': 'Fixed Difficulty', 'epsilon': 0.0, 'threshold': 0.9},
    {'name': '0.6 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.6},
    {'name': '0.7 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.7},
    {'name': '0.8 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.8},
    {'name': '0.9 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.9},
    {'name': '0.95 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.95},
    {'name': '0.97 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.97},
    {'name': '0.99 Proficiency Threshold', 'epsilon': 0.1, 'threshold': 0.99},
    {'name': 'No Early Termination', 'epsilon': 0.1, 'threshold': 1.5},  # no early termination
]

# Run the simulation for all strategies
simulate_adaptive_assessment(num_students, num_questions, num_difficulties, strategies)
