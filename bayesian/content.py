import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
import os

# Function to generate random student preferences
def generate_student_preferences(num_content_types):
    # Random true proficiency for each content type (between 0.4 and 0.9)
    return np.random.uniform(0.4, 0.9, num_content_types)

# Number of students and content types
num_students = 100
content_types = ['Video', 'Article', 'Quiz', 'Interactive', 'Podcast']
num_content_types = len(content_types)

# Create a directory to save student plots
os.makedirs("content", exist_ok=True)

# Store results for all students
all_mean_preferences = np.zeros((num_students, num_content_types))
all_likes = np.zeros((num_students, num_content_types))

# Simulate data for each student
for student_id in range(num_students):
    # Generate random true preferences for this student
    true_preferences = generate_student_preferences(num_content_types)
    
    # Simulate a student's interaction history with each content type
    interactions = np.random.randint(5, 20, num_content_types)  # Random interactions between 5 and 20
    
    # Simulate the number of positive interactions (likes)
    likes = np.array([
        np.random.binomial(interactions[0], true_preferences[0]),  # Likes for Video
        np.random.binomial(interactions[1], true_preferences[1]),  # Likes for Article
        np.random.binomial(interactions[2], true_preferences[2]),  # Likes for Quiz
        np.random.binomial(interactions[3], true_preferences[3]),  # Likes for Interactive
        np.random.binomial(interactions[4], true_preferences[4])   # Likes for Podcast
    ])
    
    # Prior belief about the student's preference for each content type (Beta distribution)
    alpha_prior = np.ones(num_content_types)  # Prior successes
    beta_prior = np.ones(num_content_types)   # Prior failures

    # Bayesian updating for each content type
    alpha_post = alpha_prior + likes
    beta_post = beta_prior + (interactions - likes)

    # Calculate the mean preference for each content type
    mean_preferences = alpha_post / (alpha_post + beta_post)
    
    # Store results
    all_mean_preferences[student_id] = mean_preferences
    all_likes[student_id] = likes

    # Plotting the posterior distribution for the current student
    x = np.linspace(0, 1, 100)
    plt.figure(figsize=(12, 8))
    for i in range(num_content_types):
        posterior = beta.pdf(x, alpha_post[i], beta_post[i])
        plt.plot(x, posterior, label=f'Posterior for {content_types[i]}')

    plt.title(f'Posterior Distributions of Preferences for Student {student_id + 1}')
    plt.xlabel('Preference Probability')
    plt.ylabel('Density')
    plt.legend()
    plt.grid()
    
    # Save the plot for the current student
    plt.savefig(f"bayesian/content/student{student_id + 1}.png")
    plt.close()  # Close the plot to free memory

    print(f"Student {student_id}")
    print("  True Preferences: " + ", ".join(f"{t:.3f}" for t in true_preferences))
    print("  Mean Preferences: " + ", ".join(f"{t:.3f}" for t in mean_preferences))
    print("  Difference:       " + ", ".join(f"{abs(t):.3f}" for t in true_preferences-mean_preferences))


# Plotting the mean preferences for all students
plt.figure(figsize=(12, 8))
for i in range(num_content_types):
    plt.hist(all_mean_preferences[:, i], bins=10, alpha=0.5, label=f'{content_types[i]} Preferences')

plt.title('Distribution of Mean Preferences for Content Types Across 100 Students')
plt.xlabel('Mean Preference Probability')
plt.ylabel('Number of Students')
plt.legend()
plt.grid()
plt.savefig("bayesian/content/preferences.png")
plt.close()

# Plotting the average likes for each content type
average_likes = np.mean(all_likes, axis=0)
plt.figure(figsize=(12, 6))
plt.bar(content_types, average_likes, color='skyblue')
plt.title('Average Likes for Each Content Type Across 100 Students')
plt.xlabel('Content Type')
plt.ylabel('Average Likes')
plt.grid(axis='y')
plt.savefig("bayesian/content/likes.png")
plt.close()
