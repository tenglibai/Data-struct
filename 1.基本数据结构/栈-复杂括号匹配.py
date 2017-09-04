def parChecker(symbolString):
	stack = []
	balanced = True
	index = 0
	while index < len(symbolString) and balanced:
		symbol = symbolString[index]
		if symbol in '([{':
			stack.append(symbol)
		else:
			if stack == []:
				balanced = False
			else:
				top = stack.pop()
				if not match(top, symbol):
					balanced = False
		index += 1
	if stack == [] and balanced:
		return True
	else:
		return False


def match(open, close):
	opens = '([{'
	closers = ')]}'
	return opens.index(open) == closers.index(close)


assert parChecker('{{([][])}()}') == True
assert parChecker('[{()]') == False
