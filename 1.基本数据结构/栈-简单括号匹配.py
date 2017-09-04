def parChecker(symbolString):
	stack = []
	balanced = True
	index = 0
	while index < len(symbolString) and balanced:
		symbol = symbolString[index]
		if symbol == '(':
			stack.append(symbol)
		else:
			if stack == []:
				balanced = False
			else:
				stack.pop()
		index += 1
	if stack == [] and balanced:
		return True
	else:
		return False


assert parChecker('((()))') == True
assert parChecker('(()') == False
