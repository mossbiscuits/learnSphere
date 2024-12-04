import numpy as np
import matplotlib.pyplot as plt
import random

# Define constants
num_students = 1000
num_simulations = 100
passing_threshold = 0.7  # 70% of course material
refund_rate = 0.5  # 0% of students who don't pass get a refund
profit_margin = 0.15  # 15% profit margin
operating_cost_per_student = 1000  # base operating cost per student

# mean of 0.75 (barely passing) and a standard deviation of 0.21
mean_grade = 0.75
stdev_grade = 0.21


# Simulate student behavior using a normal distribution
student_performance = np.random.normal(mean_grade, stdev_grade, (num_simulations, num_students))

# Clip student performance to be between 0 and 1
student_performance = np.clip(student_performance, 0, 1)

# Calculate the number of students who pass
num_passing_students = np.sum(student_performance >= passing_threshold, axis=1)

# Calculate the number of students who don't pass and get a refund
num_refunded_students = np.sum(student_performance < passing_threshold, axis=1) * refund_rate

# Calculate the total operating cost
total_operating_cost = np.sum(student_performance * operating_cost_per_student, axis=1)

# Calculate the total revenue required to cover operating costs and profit margin
total_revenue_required = total_operating_cost / (1 - profit_margin)

# Calculate the price per student
price_per_student = total_revenue_required / num_students

# Adjust the price per student based on the refund rate
price_per_student *= (1 + refund_rate)

# Plot the distribution of student performance
plt.figure(figsize=(10, 6))
plt.hist(np.mean(student_performance, axis=0), bins=20, alpha=0.5, label='Student Performance')
plt.axvline(x=passing_threshold, color='r', linestyle='--', label='Passing Threshold')
plt.legend()
plt.title('Distribution of Student Performance')
plt.xlabel('Student Performance')
plt.ylabel('Frequency')
plt.savefig("insurance/distribution_of_performance.png")
plt.show()

# Plot the number of passing students over multiple simulations
plt.figure(figsize=(10, 6))
plt.hist(num_passing_students, bins=20, alpha=0.5, label='Number of Passing Students')
plt.axvline(x=np.mean(num_passing_students), color='r', linestyle='--', label='Mean Number of Passing Students')
plt.legend()
plt.title('Number of Passing Students Over Multiple Simulations')
plt.xlabel('Number of Passing Students')
plt.ylabel('Frequency')
plt.savefig("insurance/num_passing_students.png")
plt.show()

# Plot the price per student over multiple simulations
plt.figure(figsize=(10, 6))
plt.hist(price_per_student, bins=20, alpha=0.5, label='Price Per Student')
plt.axvline(x=np.mean(price_per_student), color='r', linestyle='--', label='Mean Price Per Student')
plt.legend()
plt.title('Price Per Student Over Multiple Simulations')
plt.xlabel('Price Per Student')
plt.ylabel('Frequency')
plt.savefig("insurance/price_per_student.png")
plt.show()

print(f"Mean number of passing students: {np.mean(num_passing_students):.2f}")
print(f"Mean number of refunded students: {np.mean(num_refunded_students):.2f}")
print(f"Mean total operating cost: ${np.mean(total_operating_cost):.2f}")
print(f"Mean total revenue required: ${np.mean(total_revenue_required):.2f}")
print(f"Mean price per student: ${np.mean(price_per_student):.2f}")
