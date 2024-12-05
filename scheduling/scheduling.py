import random
from student import Student
from tutor import Tutor
from tutoringQueueSimulator import TutoringQueueSimulator

def main():
    topics = ["Math", "History", "English", "Science", "Art"]
    tutorCountPerTopic = 500

    students = generateStudents(topics)
    tutors = generateTutors(topics, tutorCountPerTopic)
    simulator = TutoringQueueSimulator(students, tutors)
    simulator.run()
    simulator.report()

# Generate the students for the simulation
def generateStudents(topics):
    students = []

    for i in range(20000): # number of students to be generated is the range
        student = createStudent(topics, 480, 90, 15) # 480 represents the minutes in 8 hours
        students.append(student)

    return students

# Randomly determine the values for a student
def createStudent(topics, maxDeadline, maxTime, minTime):
    startTime = random.randrange(0, (maxDeadline - minTime))

    # Don't let the student have a deadline past the end of the simulation
    timeRemaining = maxDeadline - startTime 
    if(timeRemaining < maxTime):
        maxTime = timeRemaining

    timeNeeded = random.randrange(minTime, maxTime)
    deadline = random.randrange(startTime + timeNeeded, maxDeadline)

    topicIndex = random.randrange(len(topics))
    topic = topics[topicIndex]

    return Student(startTime, timeNeeded, deadline, topic)

# Generate the tutors for the simulation
def generateTutors(topics, count): 
    tutors = []
    for i in range(len(topics)): 
        for j in range(count):
            tutor = Tutor(topics[i])
            tutors.append(tutor)
    return tutors

if __name__ == '__main__':
    main()
