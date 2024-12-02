import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

np.random.seed(42)  # For reproducibility


# Simulate 100 students
num_students = 100

for i in range(num_students):

    # Simulate assignment scores: 1 for pass, 0 for fail
    num_assignments = max(0,int(np.random.normal(50,35)))
    true_proficiency = max(0.0,min(np.random.normal(0.7,0.3), 1.0))
    assignments = np.random.binomial(1, true_proficiency, num_assignments)

    print(f"Student {i}")
    print(f"  Assignments: {num_assignments}")
    print(f"  True proficiency: {true_proficiency:.2f}")

    # Number of correct answers
    correct_answers = np.sum(assignments)
    total_assignments = len(assignments)

    # Prior belief about the student's proficiency (Beta distribution)
    alpha_prior = 1  # Prior successes
    beta_prior = 1   # Prior failures

    # Bayesian updating
    # Update the parameters of the Beta distribution
    alpha_post = alpha_prior + correct_answers
    beta_post = beta_prior + (total_assignments - correct_answers)

    # Generate a range of proficiency values
    x = np.linspace(0, 1, 100)

    # Calculate the posterior distribution
    posterior = beta.pdf(x, alpha_post, beta_post)

    # Plotting the posterior distribution
    plt.figure()
    plt.plot(x, posterior, label='Posterior Distribution', color='blue')
    plt.title('Posterior Distribution of Student Proficiency')
    plt.xlabel('Proficiency')
    plt.ylabel('Density')
    plt.legend()
    plt.grid()
    plt.savefig(f"bayesian/pathways/student{i}.png")
    plt.close()

    # Calculate the mean proficiency
    mean_proficiency = alpha_post / (alpha_post + beta_post)
    print(f'  Mean Proficiency: {mean_proficiency:.2f}')

    # Suggest personalized learning pathway based on proficiency
    if mean_proficiency < 0.5:
        print("  Suggested Pathway: Focus on foundational topics.")
    elif 0.5 <= mean_proficiency < 0.8:
        print("  Suggested Pathway: Intermediate topics with some advanced challenges.")
    else:
        print("  Suggested Pathway: Advanced topics and projects.")
