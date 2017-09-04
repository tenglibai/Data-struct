def infixToPostfix(infixexpr):
	prec = {}
	prec["*"] = 3
	prec["/"] = 3
	prec["+"] = 2
	prec["-"] = 2
	prec["("] = 1
	Stack = []
	postfixList = []
	tokenList = infixexpr.replace(' ', '')

	for token in tokenList:
		if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
			postfixList.append(token)
		elif token == '(':
			Stack.append(token)
		elif token == ')':
			topToken = Stack.pop()
			while topToken != '(':
				postfixList.append(topToken)
				topToken = Stack.pop()
		else:
			while (not Stack == []) and (prec[Stack[len(Stack) - 1]] >= prec[token]):
				postfixList.append(Stack.pop())
			Stack.append(token)

	while not Stack == []:
		postfixList.append(Stack.pop())
	return "".join(postfixList)


assert infixToPostfix("A*B+C*D") == 'AB*CD*+'
assert infixToPostfix("(A+B)*C-(D-E)*(F+G)") == 'AB+C*DE-FG+*-'

'''
后缀表达式求值
'''


def postfixEval(postfixExpr):
	Stack = []
	tokenList = postfixExpr.replace(' ', '')

	for token in tokenList:
		if token in "0123456789":
			Stack.append(int(token))
		else:
			operand2 = Stack.pop()
			operand1 = Stack.pop()
			result = doMath(token, operand1, operand2)
			Stack.append(result)
	return Stack.pop()


def doMath(op, op1, op2):
	if op == "*":
		return op1 * op2
	elif op == "/":
		return op1 / op2
	elif op == "+":
		return op1 + op2
	else:
		return op1 - op2


print(postfixEval('7 8 + 3 2 + /'))
