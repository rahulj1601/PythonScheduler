import comedian
import demographic
import ReaderWriter
import timetable
import random
import math

class Scheduler:

	def __init__(self,comedian_List, demographic_List):
		self.comedian_List = comedian_List
		self.demographic_List = demographic_List

	#Using the comedian_List and demographic_List, the this class will create a timetable of slots for each of the 5 work days of the week.
	#The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
	#	timetableObj.addSession("Monday", 1, comedian_Obj, demographic_Obj, "main")
	#This line will set the session slot '1' on Monday to a main show with comedian_obj, which is being marketed to demographic_obj.
	#Note here that the comedian and demographic are represented by objects, not strings.
	#The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
	#The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in Task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in Tasks 2 and 3.
	#Comedian (3rd argument) and Demographic (4th argument) can be assigned any value, but if the comedian or demographic are not in the original lists,
	#	your solution will be marked incorrectly.
	#The final, 5th argument, is the show type. For Task 1, all shows should be "main". For Tasks 2 and 3, you should assign either "main" or "test" as the show type.
	#In Tasks 2 and 3, all shows will either be a 'main' show or a 'test' show

	#demographic_List is a list of Demographic objects. A Demographic object, 'd' has the following attributes:
	# d.reference  - the reference code of the demographic
	# d.topics - a list of strings, describing the topics that the demographic like to see in their comedy shows e.g. ["Politics", "Family"]

	#comedian_List is a list of Comedian objects. A Comedian object, 'c', has the following attributes:
	# c.name - the name of the Comedian
	# c.themes - a list of strings, describing the themes that the comedian uses in their comedy shows e.g. ["Politics", "Family"]

	#For Task 1:
	#Keep in mind that a comedian can only have their show marketed to a demographic
	#	if the comedian's themes contain every topic the demographic likes to see in their comedy shows.
	#Furthermore, a comedian can only perform one main show a day, and a maximum of two main shows over the course of the week.
	#There will always be 25 demographics, one for each slot in the week, but the number of comedians will vary.
	#In some problems, demographics will have 2 topics and in others 3 topics.
	#A comedian will have between 3-8 different themes.

	#For Tasks 2 and 3:
	#A comedian can only have their test show marketed to a demographic if the comedian's themes contain at least one topic
	#	that the demographic likes to see in their comedy shows.
	#Comedians can only manage 4 hours of stage time a week, where main shows are 2 hours and test shows are 1 hour.
	#A Comedian cannot be on stage for more than 2 hours a day.

	#You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
	#Furthermore, you should not import anything else beyond what has been imported above.
	#To reiterate, the five calls are timetableObj.addSession, d.reference, d.topics, c.name, c.themes

	#checking the constraints for task 1
	def checkConstraintsTask1(self, schedule, usedDemographics):

		#check that each demographic has only been used once
		if len(usedDemographics) != len(set(usedDemographics)):
			return False

		#iterate through each day of the week
		for i in range(0,5):
			tempSet = set([])
			tempList = []

			#form temporary set of names of comedians performing on that day
			for j in range(i*5, (i*5)+5):
				if schedule[j] == 0:
					return True
				else:
					tempSet.add(schedule[j][1].name)
					tempList.append(schedule[j][1].name)

			#check if the comedians performing during the day are all different 
			if len(tempList) != len(tempSet):
				return False

		return True

	#checking the constraints for task 2
	def checkConstraintsTask2(self, schedule):

		#check that each demographic has only been used once within the schedule/timetable
		demographics = []
		for i in range(len(schedule)):
			if schedule[i] == 0:
				break
			elif (schedule[i][0].reference + schedule[i][1]) in demographics:
				return False
			else:
				demographics.append(schedule[i][0].reference + schedule[i][1])

		#iterate through each day of the week
		#make sure a single comedian peforms at most 4 hours a week and 2 hours in a day
		totalComedianHours = {}
		for i in range(0,5):
			
			dailyComedianHours = {}
			#form temporary set of names of comedians performing on that day
			for j in range(i*10, (i*10)+10):
				if schedule[j] == 0:
					return True

				#add the comedian to the respective dictionary if they are not already in it
				if schedule[j][2].name not in dailyComedianHours:
					dailyComedianHours.update({schedule[j][2].name:0})
				if schedule[j][2].name not in totalComedianHours:
					totalComedianHours.update({schedule[j][2].name:0})

				#increase count of hours for the current comedian depending on test or main show
				if schedule[j][1] == "main":
					dailyComedianHours[schedule[j][2].name] += 2
					totalComedianHours[schedule[j][2].name] += 2
				else:
					dailyComedianHours[schedule[j][2].name] += 1
					totalComedianHours[schedule[j][2].name] += 1

				#check against constraints for the current comedian
				if dailyComedianHours[schedule[j][2].name] > 2:
					return False
				if totalComedianHours[schedule[j][2].name] > 4:
					return False

		return True

	#This function is used to see whether a comedian is compatible with a demographic as a test show or main show
	def canMarket(self, comedian, demographic, isTest):
		#if it is not a test show, we make sure every one of the demographics' topics is matched by the comedian's themes.
		if not isTest:
			topics = demographic.topics
			i = 0
			for t in topics:
				if t not in comedian.themes:
					return False
			return True
		#if it is a test show, we make sure the comedian has at least one theme that matches a topic of the demographic.
		else:
			topics = demographic.topics
			i = 0
			for t in topics:
				if t in comedian.themes:
					return True
			return False

	#Selects the index of the first position encountered where the value in the schedule is 0
	#Least Constraining Value (LCV) - choose the least constraining value which is the one that rules out the 
	#fewest values in the remaining variables, this would be the next available position in the schedule
	def selectUnassignedPosition(self, schedule):
		for i in range(len(schedule)):
			if schedule[i] == 0:
				return i
		return 0

	#recursive backtracking function
	def recursiveBacktracking(self, schedule, demographicComedianPairs):
		#if the schedule has been completed and follows all of the constraints then it can be returned
		if self.checkConstraintsTask2(schedule) and schedule[49]!=0:
			return schedule

		#select the next available position in the schedule by calling the selectUnassignedPosition function
		position = self.selectUnassignedPosition(schedule)

		#iterates through the demographic comedian pairs
		for pair in demographicComedianPairs:
			tempSchedule = schedule
			tempSchedule[position] = pair
			#creates a temporary schedule to see if adding the new demographic-comedian pair works
			if self.checkConstraintsTask2(tempSchedule):
				#if the demographic-comedian pair works in the schedule then the schedule is updated
				schedule = tempSchedule
				#recursion is used to continue and update the next positions in the schedule
				result = self.recursiveBacktracking(schedule, demographicComedianPairs)
				if result != False:
					return result
			schedule[position] = 0
		
		#false is returned if there are no items suitable for the current position
		return False

	### PREAMBLE FOR TASK 1
	#For this task I decided to make use of backtracking. Before entering the backtracking algorithm, I decided to pair each demographic 
	#with a single comedian. When doing so, there were two constraints I had to follow which were that one comedian can only be paired
	#with at most 2 different demographics. And also that the comedian must be compatible with the demographic, meaning that the comedians 
	#themes must include all of the themes the demographic requires. When matching each demographic to one comedian, I used a degree 
	#heuristic where I began with the demographics that had the fewest number of comedians to choose from. By doing this I was able to 
	#successfully match each demographic with a comedian. Then once this had been complete I would begin backtracking which would iterate 
	#through each empty slot in the schedule and allocate a demographic-comedian pair. To allocate a slot, I had to allocate the least 
	#constraining value, which would always be the next available empty slot. The algorithm would go through each of the 5 slots for each 
	#day until all slots are filled and the constraints are followed. The constraints that would be checked against would be that each 
	#demographic only performs once during the week and each comedian performing during the course of the day is different.
	#I chose to make use of backtracking because it systematically goes through each different possible path (combination of 
	#demographic-comedian pairs) to find the first combination which works, therefore it is efficient at solving this sort of algorithm.
	#However, I had to use heuristics (which I previously stated) to make it more efficient because if the solution was one of the last 
	#combinations it chose then this would have quite a long run time.

	#This method should return a timetable object with a schedule that is legal according to all constraints of Task 1.
	def createSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(1)

		#Generating the comedians compatible with the demographic - comedian must cover all themes of the demographic topics 
		#to be compatible with that demographic
		demographicComedianPairs = []
		for d in self.demographic_List:
			demographic = []
			demographic.append(d)
			for c in self.comedian_List:
				if (set(d.topics).issubset(set(c.themes))):
					demographic.append(c)
			demographicComedianPairs.append(demographic)

		#sorts list elements from shortest to longest
		#degree heuristic - we are going to pair up each demographic with one comedian starting with the demographic that 
		#has the least number of comedians to choose from (these are the demographics with the most constraints)
		demographicComedianPairs.sort(key=len)

		#Isolating one comedian for each demographic to form a demographic-comedian pair
		#Counting the number of times the comedian is paired up with a demographic - can only be paired up twice to perform 
		#at most twice during the week
		comedianCount = {}
		for i in range(25):
			for nameIndex in range(1, len(demographicComedianPairs[i])):
				#Iterates through the comedians that were compatible with each demographic and stores the name in comedianName
				comedianName = demographicComedianPairs[i][nameIndex].name

				#if the comedian has not been put in the schedule then it can be paired with the current demographic
				if comedianName not in comedianCount:
					demographicComedianPairs[i] = [ demographicComedianPairs[i][0], demographicComedianPairs[i][nameIndex] ]
					#Count the number of times the comedian performs during the week
					comedianCount.update({comedianName:1})
					break

				#must increment the number of times the comedian performs per week and pair the comedian with the current demographic
				#first must check if the comedian performs less than 2 times a week because they cannot perform more than twice a week
				elif comedianCount[comedianName] < 2:
					demographicComedianPairs[i] = [ demographicComedianPairs[i][0], demographicComedianPairs[i][nameIndex] ]
					comedianCount[comedianName] += 1
					break

		#forms the schedule - uses empty zeros to indicate blank slots in the schedule
		schedule = [0,0,0,0,0,
					0,0,0,0,0,
					0,0,0,0,0,
					0,0,0,0,0,
					0,0,0,0,0]

		#backtracking algorithm uses while loop - used to generate a correct schedule
		position = 0
		#usedDemographics list keeps track of the demographics which we have already added to the schedule
		usedDemographics = []
		while True:
			##ALLOCATING VALUES INTO THE SCHEDULE
			#if the position needs to be allocated something we try the first possible demographic-comedian pair
			if schedule[position] == 0:
				schedule[position] = demographicComedianPairs[0]
				usedDemographics.append(demographicComedianPairs[0][0].reference)

			#continue at current position go to next possible demographic unless all possibilities have been tested
			elif (isinstance(schedule[position],int) == False) and (schedule[position] != demographicComedianPairs[24]):
				usedDemographics.remove(schedule[position][0].reference)
				schedule[position] = demographicComedianPairs[ demographicComedianPairs.index(schedule[position])+1 ]
				usedDemographics.append(schedule[position][0].reference)				

			##CHECKING VALIDITY OF THE SCHEDULE
			#if the schedule doesn't follow constraints when all values have been exhausted we need to backtrack
			if self.checkConstraintsTask1(schedule,usedDemographics) == False:
				while schedule[position] == demographicComedianPairs[24]:
					usedDemographics.remove( schedule[position][0].reference )
					schedule[position] = 0
					position-=1

			#if the schedule follows constraints we either move to the next free position in the schedule or if the final position
			#in the schedule doesn't have a 0 in the slot then it has been fully filled and adheres to constraints
			elif self.checkConstraintsTask1(schedule,usedDemographics) == True:
				if schedule[24] != 0:
					break
				else:
					position+=1
		
		#forming the final timetable using the schedule
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		index = 0
		for day in days:
			for i in range(1,6):
				timetableObj.addSession(day, i, schedule[index][1], schedule[index][0], "main")
				index+=1

		#Do not change this line
		return timetableObj
	
	### PREAMBLE FOR TASK 2
	#For this task the main aspect which allows my program to compile and return an answer quickly is the use of heuristics. I made use
	#of minimum remaining values (MRV) when choosing a value to next test in the schedule. This was because it would allow my program to
	#fail quickly if there was an issue and try the next demographic in the list. So when assigning the next demographic-comedian pair in 
	#the schedule, I would choose the demographic with fewest compatible comedians as these were likely to cause failure quickly. By doing
	#so my program could backtrack quickly when needed instead of getting all the way to the end of the schedule and needing to backtrack
	#which would take far longer due to the failure being later on. Therefore, by ordering my demographic-comedian pairs in this way before
	#they would be passed into the backtracking function allowed me to keep the tree small and fail quickly to improve the efficiency.
	#Ordering the demographic-comedian pairs in this way also meant that the program could succeed sooner, and also by choosing the least
	#constraining value first meant that fewer values in the remaining variables could be ruled out. My algorithm would choose the least 
	#constraining value by always picking the next available slot in the schedule and systematically going through each of them whilst 
	#also backtracking if it is necessary. 
	#For this task I decided to use a recursive backtracking algorithm because it is much quicker than the backtracking method I used in 
	#task 1. This was essential for task 2 because there were double the number of slots in the schedule and so my algorithm would need 
	#to be faster when backtracking, so a recursive approach would be neater and also does work a bit faster than using a while loop.

	#Now, for Task 2 we introduce test shows. Each day now has ten sessions, and we want to market one main show and one test show
	#	to each demographic.
	#All slots must be either a main or a test show, and each show requires a comedian and a demographic.
	#A comedian can have their test show marketed to a demographic if the comedian's themes include at least one topic the demographic likes.
	#We are also concerned with stage hours. A comedian can be on stage for a maximum of four hours a week.
	#Main shows are 2 hours long, test shows are 1 hour long.
	#A comedian cannot be on stage for more than 2 hours a day.
	def createTestShowSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(2)

		#forming all possible pairs of demographic and comedian and assigning test/main depending on which show they are elegible for
		demographicComedianPairs = []
		#keeping count of the number of comedians compatible with each demographic
		demographicCount = {}
		for d in self.demographic_List:
			demographicCount.update({d.reference + "test":0})
			demographicCount.update({d.reference + "main":0})
			for c in self.comedian_List:
				if self.canMarket(c,d,1):
					demographicComedianPairs.append([d,"test",c])
					demographicCount[d.reference+"test"]+=1
				if self.canMarket(c,d,0):
					demographicComedianPairs.append([d,"main",c])
					demographicCount[d.reference+"main"]+=1

		#sorting the demographics in order of fewest number of compatible comedians to highest number of compatible comedians
		demographicCount = dict(sorted(demographicCount.items(), key=lambda item: item[1]))

		#organising the demographicComedianPairs with the demographics that have the fewest number of compatible comedians first
		#then the demographics with the highest number of compatible comedians after
		#degree heuristic - we are selecting from the demographics which don't have much choice first as these are the more constraining
		#demographics and hence by doing this we are reducing the branching factor for future choices
		#This method allows us to succeed sooner, as the main shows with only 1 compatible comedian can be prioritised
		temp = []
		demographicList = list(demographicCount)
		for demographic in demographicList:
			for i in range(demographicCount[demographic]):
				for j in range(len(demographicComedianPairs)):
					if demographicComedianPairs[j][0].reference + demographicComedianPairs[j][1] == demographic:
						temp.append(demographicComedianPairs[j])
						del demographicComedianPairs[j]
						break
		
		#added to a temporary list and now copy to the demographicComedianPairs list which is passed into the backtracking function
		demographicComedianPairs = temp

		#forms the schedule - zeros mark slots in the schedule which have not been assigned a show and must be assigned a show
		schedule = [0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0]

		#calling recursive backtracking which will return the first possible schedule that it finds which follows all constraints
		schedule = self.recursiveBacktracking(schedule, demographicComedianPairs)

		#forming the final timetable using the schedule
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		index = 0
		for day in days:
			for i in range(1,11):
				timetableObj.addSession(day, i, schedule[index][2], schedule[index][0], schedule[index][1])
				index+=1

		#Do not change this line
		return timetableObj

	#calculates the overall cost of a schedule - utility method for task 3
	def calculateCost(self, schedule):
		#intialise variables which help us to calculate the overall cost of the schedule
		dayShows = {1:[], 2:[], 3:[], 4:[], 5:[]}
		comedianShowCount = {}
		totalCost = 0
		#iterate through each item in the schedule
		for s in schedule:
			#need to calculate the current day number and also the previous day number
			currentDay = schedule.index(s) // 10 + 1
			previousDay = currentDay - 1
			#obtain the comedian and the show type on our current iteration
			currentComedianShow = s[2].name + s[1]
			if currentComedianShow not in comedianShowCount:
				comedianShowCount.update({currentComedianShow:0})
			#if the show type is main then we increment the total cost accordingly
			if s[1] == "main":
				#if this is the second main show by the comedian on the day after the other main show they perform
				if previousDay > 0 and comedianShowCount[currentComedianShow] >= 1 and currentComedianShow in dayShows[previousDay]:
					totalCost += 100
				#if this main show is the second main show performed by the comedian during the week
				elif comedianShowCount[currentComedianShow] >= 1:
					totalCost += 300
				else:
					totalCost += 500
			#if the show type is test then we increment the total cost accordingly
			elif s[1] == "test":
				#if this is the second test show performed by the comedian during the day
				if comedianShowCount[currentComedianShow] >= 1 and currentComedianShow in dayShows[currentDay]:
					totalCost -= 25
				#if this is either the 2nd, 3rd or 4th test show performed by the comedian during the week
				elif comedianShowCount[currentComedianShow] >= 1:
					count = comedianShowCount[currentComedianShow]
					totalCost += (250 - 50 * count)					
				else:
					totalCost += 250

			dayShows[currentDay].append(currentComedianShow)
			comedianShowCount[currentComedianShow] += 1

		#return the final result for the total cost
		return totalCost

	### PREAMBLE FOR TASK 3
	#For task 3, I decided to take the approach of using my answer from task 2 where I developed a solution using a recursive backtracking
	#algorithm and improving that solution to reduce the cost. In order to reduce the cost, I made use of the hill climbing algorithm which
	#iterates through the schedule and tests each slot to see if there is a better demographic-comedian pair (one which reduces the cost) 
	#which can be swapped with what is currently in the schedule. If there is one then we swap them and make a change to the schedule. Then
	#we repeat this process repeatedly and iterate through the schedule several times until we have iterated through the schedule once with 
	#no changes being made. This process allows us to reach close to the optimal solution and reduce the cost. However, the issue with this 
	#approach is that we may only reach a local maximum rather than the actual maximum with the lowest possible cost. Therefore, in order
	#to get to the actual maximum we would need to introduce some sort of randomness to get even closer to the optimal solution if possible.
	#Therefore, this would be something that could be improved with this solution I have made. But overall, the solution I have provided will
	#still be able to come fairly close to the optimal solution in most circumstances using the hill climbing algorithm.

	#Now, in Task 3 it costs £500 to hire a comedian for a single main show.
	#If we hire a comedian for a second show, it only costs £300. (meaning 2 shows cost £800 compared to £1000)
	#If those two shows are run on consecutive days, the second show only costs £100. (meaning 2 shows cost £600 compared to £1000)

	#It costs £250 to hire a comedian for a test show, and then £50 less for each extra test show (£200, £150 and £100)
	#If a test shows occur on the same day as anything else a comedian is in, then its cost is halved.

	#Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
	#You are not expected to always find the optimal solution, but you should be as close as possible.
	#You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
	def createMinCostSchedule(self):
		#Do not change this line
		timetableObj = timetable.Timetable(3)

		#START OF TASK 2 CODE - THIS CODE RUNS THE SAME PROCESS AS WE HAVE RUN IN TASK 2 TO FIND A SOLUTION WHICH IS THEN FURTHER OPTIMISED
		#forming all possible pairs of demographic and comedian and assigning test/main depending on which show they are elegible for
		demographicComedianPairs = []
		#keeping count of the number of comedians compatible with each demographic
		demographicCount = {}
		for d in self.demographic_List:
			demographicCount.update({d.reference + "test":0})
			demographicCount.update({d.reference + "main":0})
			for c in self.comedian_List:
				if self.canMarket(c,d,1):
					demographicComedianPairs.append([d,"test",c])
					demographicCount[d.reference+"test"]+=1
				if self.canMarket(c,d,0):
					demographicComedianPairs.append([d,"main",c])
					demographicCount[d.reference+"main"]+=1

		#sorting the demographics in order of fewest number of compatible comedians to highest number of compatible comedians
		demographicCount = dict(sorted(demographicCount.items(), key=lambda item: item[1]))

		#organising the demographicComedianPairs with the demographics that have the fewest number of compatible comedians first
		#then the demographics with the highest number of compatible comedians after
		#degree heuristic - we are selecting from the demographics which don't have much choice first as these are the more constraining
		#demographics and hence by doing this we are reducing the branching factor for future choices
		#This method allows us to succeed sooner, as the main shows with only 1 compatible comedian can be prioritised
		temp = []
		demographicList = list(demographicCount)
		for demographic in demographicList:
			for i in range(demographicCount[demographic]):
				for j in range(len(demographicComedianPairs)):
					if demographicComedianPairs[j][0].reference + demographicComedianPairs[j][1] == demographic:
						temp.append(demographicComedianPairs[j])
						del demographicComedianPairs[j]
						break
		
		#added to a temporary list and now copy to the demographicComedianPairs list which is passed into the backtracking function
		demographicComedianPairs = temp

		#forms the schedule - zeros mark slots in the schedule which have not been assigned a show and must be assigned a show
		schedule = [0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0,
					0,0,0,0,0,0,0,0,0,0]

		#calling recursive backtracking which will return the first possible schedule that it finds which follows all constraints
		schedule = self.recursiveBacktracking(schedule, demographicComedianPairs)
		##END OF TASK 2 CODE

		#optimise the schedule look for replacements where possible then when every pair has been tested in every slot of the schedule
		#and no slot is changed we will return the solution because this should be close to the most optimal solution
		position = 0
		while True:
			#reset the count variable once a single iteration of the schedule has been complete
			if position%len(schedule) == 0:
				count = 0

			#runs the function to calculate the cost of the schedule currently
			currentScheduleCost = self.calculateCost(schedule)
			#iterates through each pair of the demographicComedianPairs list which contains all compatible demographics and comedians
			for pair in demographicComedianPairs:
				#need to do position%50 because we will iterate through the schedule several times to ensure we are as close as possible to 
				#the optimal value
				oldValue = schedule[position%50]
				schedule[position%50] = pair
				isCorrect = self.checkConstraintsTask2(schedule)
				newScheduleCost = self.calculateCost(schedule)
				if (isCorrect == False) or (isCorrect and newScheduleCost >= currentScheduleCost):
					#if value doesn't work in the schedule then return to the old schedule
					schedule[position%50] = oldValue
					#the counter keeps track of when a value doesn't work in that specific slot in the schedule
					count+=1
				else:
					currentScheduleCost = newScheduleCost
			
			#increment the position variable to go to the next position in the schedule
			position+=1

			#if no values in the demographicComedianPairs list can be replaced with any item in the schedule
			#then this means the schedule has been optimised
			#in this situation the counter should equal the length of the schedule x length of demographicComedianPairs because this means
			#every single possible value has been tested in every slot of the schedule and no replacements were made
			if count == (len(demographicComedianPairs) * len(schedule)):
				break

		#forming the final timetable using the schedule
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		index = 0
		for day in days:
			for i in range(1,11):
				timetableObj.addSession(day, i, schedule[index][2], schedule[index][0], schedule[index][1])
				index+=1

		#Do not change this line
		return timetableObj


	#This simplistic approach merely assigns each demographic and comedian to a random slot, iterating through the timetable.
	def randomMainSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 6:
				sessionNumber = 1
				dayNumber = dayNumber + 1

	#This simplistic approach merely assigns each demographic to a random main and test show, with a random comedian, iterating through the timetable.
	def randomMainAndTestSchedule(self,timetableObj):

		sessionNumber = 1
		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
		dayNumber = 0
		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "main")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1

		for demographic in self.demographic_List:
			comedian = self.comedian_List[random.randrange(0, len(self.comedian_List))]

			timetableObj.addSession(days[dayNumber], sessionNumber, comedian, demographic, "test")

			sessionNumber = sessionNumber + 1

			if sessionNumber == 11:
				sessionNumber = 1
				dayNumber = dayNumber + 1
