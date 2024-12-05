class Student:

	# Student constructor
	def __init__(self, startTime, timeNeeded, deadline, topic):
		self.waitingTime = 0
		self.startTime = startTime # Start time represents the time when the student will request tutoring
		self.timeNeeded = timeNeeded
		self.deadline = deadline
		self.topic = topic

