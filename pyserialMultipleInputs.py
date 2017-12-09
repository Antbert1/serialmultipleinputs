"""
Author: Anthea Middleton
Setup serial port connection and read in data from Arduino
Format data, removing common errors and plot against time
"""

#Import the required libraries
import serial
import time
#This is very slow to load
import matplotlib.pyplot as plt
import numpy as np


#These variables are set at the start to be used later on in the plotting. As long as they are 'in scope' and are set before you try to use them, it doesn't matter where you set them. Being in scope means being declared where you are using them. An example of being out of scope would be if you had a "main" function, and a separate "graph" function that is called inside main. If you declare a variable min_val inside the graph function, and try to use it in the main, it won't work because main can't see it.
min_val = 0
max_val = 1024

#Prints a line to the terminal asking user to input the port number as 'COMx'. You can check the port number in device manager when the Arduino is plugged in
port = raw_input("Enter the port number (e.g. 'COM4'): \n")

#Creates a variable called 'ser' that we will use to communicate with the serial port. Gives it the port number, the baud rate and timeout (not sure what timeout does but it fixed that 0000s problem)
ser = serial.Serial(port, 57600, timeout=1)

#Some commented out stuff experimenting with weird data
#ser = serial.Serial('COM4', 9600, timeout=1)
#ser.flush()

#Sleep tells the programme to wait for x seconds. Useful in serial comms when you want to be sure something has happened
time.sleep(1)

#Flush flushes what's in the serial buffer. Not sure why this is recommended, but someone suggested it for fixing strange data
ser.flush()

#Tells the user to press 1 to start
start = input("Press 1 to start")

#This is an empty array of data that will be populated later with the values from the serial port
valList = []

#A function that checks if a number (s) valid number. Returns true if so, false if not. Used later on for sorting data
def RepresentsInt(s):
	try:
		float(s)
		return True
	#If user presses ctrl+c, loop will stop
	except ValueError:
		#break breaks out of loop
		return False



#This runs until the user cancels it (by pressing Ctrl+C)
def runLoop():
	while 1:
		try:
			#Append whatever is coming through on the serial port to valList array
			valList.append(ser.readline())
		#If user presses ctrl+c, loop will stop
		except KeyboardInterrupt:
			#break breaks out of loop
			break


#When user input 'start' (defined above) is equal to 1, write a command to the serial port that the Arduino will read. This is useful later for controlling
if start == 1:
	#'b'5'' means a byte string version of '5'
	ser.write(b'5')
	#This is a timer so I can see how long it took
	startTime = time.time()
	#Calls runLoop (defined above)
	runLoop()

#endTime fires when loop stops, so we can see how long the whole thing took (Python is sequential)
endTime = time.time()
totalTime = endTime - startTime

#Prints total time to screen
print(endTime - startTime)

#A for loop. Loops through all the values in our populated valList. 'point' refers to the value at the time
for index, point in enumerate(valList):
	#If it is a valid value (RepresentsInt defined above), go on to do more checks
	if RepresentsInt(point):
		pointNew = float(point)
		if pointNew <= max_val and pointNew >= min_val:
			#point is now valid
			valList[index] = pointNew
		else:
			#get average
			for x in range(index+1,len(valList)):
				if RepresentsInt(valList[x]):
					if float(valList[x]) <= max_val and float(valList[x]) >= min_val:
						avVal = valList[x]
						break
			newVal = (float(valList[index-1])+float(avVal))/2
			valList[index] = newVal
	#If not a number
	else:

		if index == len(valList):
			avVal = valList[index-1]
		else:
			for x in range(index+1,len(valList)):
				if RepresentsInt(valList[x]):
					if float(valList[x]) <= max_val and float(valList[x]) >= min_val:
						avVal = valList[x]
						break
		if index == 0:
			newVal = avVal
		else:
			newVal = (float(valList[index-1])+float(avVal))/2
		valList[index] = newVal

#Open a text file that is writable
file = open("testfile.txt","w")
for val in valList:
	#If number is invalid, write a 0
	if not val:
		file.write('0')
	#else write a string representation of the number to the file
	else:
		file.write(str(val))
		#\n means the end of the line. .txt files interpret this
		file.write('\n')

#Increments to plot your points on are the total time divided by the amount of points
inc = totalTime/len(valList)
#range for the plot: Start a 0.0, go to total time, in increments inc
t = np.arange(0.0, totalTime, inc)
#Plot time against valList
plt.plot(t, valList)
#Show plot
plt.show()

#Print the length of the valList to see how many got
print(len(valList))

#Close the serial port
ser.close()
