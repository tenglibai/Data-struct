# 表示数学表达式
# 规则如下：
#
#     如果当前符号是 '('，添加一个新节点作为当前节点的左子节点，并下降到左子节点。
#     如果当前符号在列表 ['+'，' - '，'/'，'*'] 中，将当前节点的根值设置为由当前符号表示的运算符。
#  添加一个新节点作为当前节点的右子节点，并下降到右子节点。
#     如果当前符号是数字，请将当前节点的根值设置为该数字并返回到父节点。
#     如果当前令牌是 ')'，则转到当前节点的父节点。
import operator
from 二叉树 import BinaryTree, preorder, postorder, printexp


def buildParseTree(fpexp):
	fplist = fpexp.split()
	pStack = []
	eTree = BinaryTree('')
	pStack.append(eTree)
	currentTree = eTree
	for i in fplist:
		if i == '(':
			currentTree.insertLeft('')
			pStack.append(currentTree)
			currentTree = currentTree.getLeftChild()
		elif i not in ['+', '-', '*', '/', ')']:
			currentTree.setRootVal(int(i))
			parent = pStack.pop()
			currentTree = parent
		elif i in ['+', '-', '*', '/']:
			currentTree.setRootVal(i)
			currentTree.insertRight('')
			pStack.append(currentTree)
			currentTree = currentTree.getRightChild()
		elif i == ')':
			currentTree = pStack.pop()
		else:
			raise ValueError
	return eTree


pt = buildParseTree("( ( 10 + 5 ) * 3 )")
postorder(pt)
print()
preorder(pt)
print()
print(printexp(pt))


def evaluate(parseTree):
	opers = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}

	leftC = parseTree.getLeftChild()
	rightC = parseTree.getRightChild()

	if leftC and rightC:
		fn = opers[parseTree.getRootVal()]
		return fn(evaluate(leftC), evaluate(rightC))
	else:
		return parseTree.getRootVal()


print(evaluate(pt))
