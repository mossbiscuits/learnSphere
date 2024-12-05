from student import Student

class Tutor:

    # Tutor constructor
    def __init__(self, expertise):
        self.queue = []
        self.expertise = expertise
        self.currentStudent = None
        self.expectedWaitTime = 0

    # Handles everything for this tutor when the simulation moves to the next second
    def nextMinute(self, simulator, time):
        if(self.currentStudent is None):
            self.moveToNextStudent(simulator)
        elif(time == self.currentStudent.deadline):
            if(self.currentStudent.timeNeeded == 1):
                simulator.studentsHelped += 1
            else:
                simulator.studentsFailed += 1
            self.moveToNextStudent(simulator)
        elif(self.currentStudent.timeNeeded == 1):
            self.moveToNextStudent(simulator)
            simulator.studentsHelped += 1
        else:
            self.currentStudent.timeNeeded -= 1

        for student in self.queue:
            student.waitingTime += 1
            if(student.deadline <= time):
                self.queue.remove(student)
                simulator.studentsFailed += 1
                simulator.waitingTimeTotal += student.waitingTime
    
    # Handles moving to the next student
    def moveToNextStudent(self, simulator):
        if(len(self.queue) > 0):
            if self.currentStudent is not None:
                self.expectedWaitTime -= self.currentStudent.timeNeeded
            self.currentStudent = self.queue.pop(0)
            simulator.waitingTimeTotal += self.currentStudent.waitingTime
        else:
            self.currentStudent = None        

    # Determines which student has higher priority
    # True means student1 has higher priority than student2
    def insertHere(self, student1, student2):
        if student1.deadline < student2.deadline:
            return True
        elif student1.timeNeeded > student2.timeNeeded:
            return True
        else:
            return False
    
    # Uses Earliest Deadline First algorithm to insert a student to the queue according to their priority
    def insertStudent(self, student):
        self.expectedWaitTime += student.timeNeeded
        for i in range(len(self.queue)):
            nextStudent = self.queue[i]
            if self.insertHere(student, nextStudent):
                self.queue.insert(i, student)
                return
            
        # if the student has the lowest priority of all, add them to the end of the queue
        self.queue.append(student)

    # Finishes the simulation, mostly by reporting students lef unhelped
    def endSimulation(self, simulator):
        self.nextMinute()
        if self.currentStudent is not None:
            simulator.studentsFailed += 1
        simulator.studentsFailed += len(self.queue)