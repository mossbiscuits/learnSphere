class TutoringQueueSimulator:

    # Simulator constructor
    def __init__ (self, students, tutors):
        self.students = students
        self.tutors = tutors
        self.time = 0
        self.studentQueue = []
        self.studentsHelped = 0
        self.studentsFailed = 0
        self.waitingTimeTotal = 0
        self.totalTutors = len(tutors)
        self.totalStudents = len(students)

    # Run the simulation
    def run(self):
        print("Running simulation...")
        while(self.time < 480):
            self.runMinute()
            self.time += 1

        for tutor in self.tutors:
            tutor.endSimulation

    # Print out results of simulation
    def report(self):
        print("------Report on simulation------")
        print("Total students: " + str(self.totalStudents))
        print("Total tutors: " + str(self.totalTutors))
        print("Percent of students successfully helped: " + str(float(self.studentsHelped/self.totalStudents) * 100) + "%")
        print("Total waiting time of all students: " + str(self.waitingTimeTotal) + " minutes")
        print("Average waiting time per student in queue: " + str(float(self.waitingTimeTotal/self.totalStudents)) + " minutes")

    # Simulate a specific minute
    def runMinute(self):
        self.addStudentsToQueue()
        for student in self.studentQueue:
            self.sortStudent(student)
            self.studentQueue.remove(student)
        self.runTutorQueues()

    # Add any students requesting a tutor at this point in time, onto the queue
    def addStudentsToQueue(self):
        for student in self.students:
            if(student.startTime == self.time):
                self.studentQueue.append(student)
                self.students.remove(student)

    # For the specific minute in the simulation, determine what is happening with each tutor
    def runTutorQueues(self):
        for tutor in self.tutors:
            tutor.nextMinute(self, self.time)
    
    # Sort the next student into the queue for the correct tutor
    def sortStudent(self, student):
        topic = student.topic
        tutor = self.pickTutor(topic)
        if tutor is None:
            print("uh oh there's no tutor that covers this student's topic")
            self.studentsFailed += 1
        else:
            tutor.insertStudent(student)

    # Identify a tutor that can help the student   
    def pickTutor(self, topic):
        options = []

        # get tutors that cover the topic
        for tutor in self.tutors:
            if tutor.expertise == topic:
                options.append(tutor)
        
        # none of the tutors are experts on the topic needed
        if(len(options) == 0):
            return None
        
        # pick the tutor with the shortest expected wait time
        shortestWait = options[0]
        for tutor in options:
            if tutor.expectedWaitTime < shortestWait.expectedWaitTime:
                shortestWait = tutor
        
        return shortestWait