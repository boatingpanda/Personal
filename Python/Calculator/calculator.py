from collections import deque

def isNum(x):
	"""function that determines if input is number"""
	try:
		float(x)
		return True
	except ValueError:
		return False

"""functions that identifies what each operators are, including parenthesis"""
def isAdd(x):
	return x == "+"

def isSub(x):
	return x == "-"

def isMult(x):
	return x == "*"

def isDivid(x):
	return x == "/"

def isMod(x):
	return x == "%"

def isPower(x):
	return x == "^"

def isLeftParenthesis(x):
	return x == "("

def isRightParenthesis(x):
	return x == ")"

def isOperator(x):
	"""function that determines if input is an operator"""
	return isAdd(x) or isSub(x) or isMult(x) or isDivid(x) or isMod(x) or isPower(x)
	# alternatively, we might be able to use the any() function
	#return any(isAdd(x), isSub(x), isMult(x), isDivid(x), isMod(x), isPower(x))

def isParenthesis(x):
	"""a function that determines if input is a parenthesis"""
	return isLeftParenthesis(x) or isRightParenthesis(x)

def setPrecedence(x):
	"""sets the operation precedence of each operators, higher takes priority. parentheses has no precedence"""
	if isAdd(x) or isSub(x):
		return 1
	elif isMult(x) or isDivid(x) or isMod(x):
		return 2
	elif isPower(x):
		return 3
	else:
		return -1

# compare two operators' precedence and return 1, 0, or -1 if x is greater, equal to, or smaller than y
# serves the same function as cmp(x, y), will be using cmp instead
# def comparePrecedence(x, y):
# 	if setPrecedence(x) > setPrecedence(y):
# 		return 1
# 	elif setPrecedence(x) == setPrecedence(y):
# 		return 0
# 	else:
# 		return -1

def calculate(outputQueue, outputStack):
	"""function that calculates what needs to be done based on what's on the output queue"""
	
	while len(outputQueue) > 0:
		temp = outputQueue.popleft()
		
		# if popleft gives us a number, put it to the output stack
		if isNum(temp):
			outputStack.append(temp)
		
		# if popleft gives us an operator, pop off 2 elements off of the stack and carry out the appropriate mathematical operation
		if isOperator(temp):
			rightVal = outputStack.pop()
			leftVal = outputStack.pop()
			
			if isAdd(temp):
				outputStack.append(leftVal + rightVal)
			elif isSub(temp):
				outputStack.append(leftVal - rightVal)
			elif isMult(temp):
				outputStack.append(leftVal * rightVal)
			elif isDivid(temp):
				outputStack.append(leftVal / rightVal)
			elif isMod(temp):
				outputStack.append(leftVal % rightVal)
			else:
				outputStack.append(leftVal ** rightVal)
	
	return outputStack[0]

# main program starts here
if __name__ == "__main__":
	
	while 1:
		userInput = raw_input("Please enter mathematical expression in infix notation. To quit, enter \"stop\" or \"exit\": ")
		
		if userInput == "exit" or userInput == "stop":
			break
		
		# preprocess the input to replace any possible constants with a number instead of the word
		
		# remove any whitespaces if there are any
		userInput = userInput.replace(" ", "")
		
		# parse the string of input and put it in a list
		tempStr = ""
		inputList = []
		
		for i in range(0, len(userInput)):
			# takes care of all cases up until the last digit of input
			# if input is a number, concatenate it to tempString
			if isNum(userInput[i]) or userInput[i] == ".":
				tempStr += userInput[i]
				
				# takes care of the final case when we reach the end of an input, add tempStr to inputList and clear tempStr
				if i == len(userInput) - 1:
					inputList.append(tempStr)
			
			# if input is an arithmetic operator, add tempStr to inputList and then add the operator to inputList. Clear the tempStr for future inputs
			else:
				
				# if input is a minus sign and has an operator in front of it and a number behind it, add it to tempStr
				if isSub(userInput[i]) and (isOperator(userInput[i-1]) or isParenthesis(userInput[i-1])) and isNum(userInput[i+1]):
					tempStr += userInput[i]
				
				else:
					if len(tempStr) > 0:
						inputList.append(tempStr)
					
					inputList.append(userInput[i])
					tempStr = ""
		
		# sets up an empty output queue for SYA
		outputQueue = deque()
		# sets up an empty operator stack for SYA
		operatorStack = []
		
		# read in the input list
		# print inputList # debug only
		for inp in inputList:
			
			# if input token is a number, move it to the output queue
			if isNum(inp):
				outputQueue.append(float(inp))
			
			# if input a left parenthesis, move it to the operator stack
			elif isLeftParenthesis(inp):
				operatorStack.append(inp)
			
			# if input is a right parenthesis, pop everything off of the operator stack until we reach the left parenthesis. remove the left parenthesis from stack
			elif isRightParenthesis(inp):
				temp = operatorStack.pop()
				while not isLeftParenthesis(temp) and len(operatorStack) > 0:
					outputQueue.append(temp)
					temp = operatorStack.pop()
			
			# if input is an operator, check operator precedence with the operator on top of the operator stack
			else:
				if len(operatorStack) > 0:
					resultPrecedence = cmp(operatorStack[0], inp)
				else:
					resultPrecedence = -1
				
				# while there's an operator on top of the operator stack that has greater precidence than input operator, pop the operator from stack to queue
				while len(operatorStack) > 0 and setPrecedence(operatorStack[0]) > setPrecedence(inp):
					outputQueue.append(operatorStack.pop())
				
				operatorStack.append(inp)
		
		while len(operatorStack) > 0:
			outputQueue.append(operatorStack.pop())
		
		# print outputQueue
		outputStack = []
		
		result = calculate(outputQueue, outputStack)
		
		print result