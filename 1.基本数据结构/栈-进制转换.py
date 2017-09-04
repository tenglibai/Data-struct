def baseConverter(decNumber, base):
	digits = "0123456789ABCDEF"
	stack = []
	while decNumber > 0:
		rem = decNumber % base
		stack.append(rem)
		decNumber = decNumber // base
	newString = ""
	while not stack == []:
		newString = newString + digits[stack.pop()]
	return newString


assert baseConverter(25, 2) == '11001'
assert baseConverter(25, 16) == '19'
