# 依然有bug, 后续需更新.

''''''''''''''''''''''''''''''
# 节点的平衡因子:
#     balanceFactor = height(leftSubTree) - height(rightSubTree)
# 确保树总是具有 -1,0或1 的平衡因子，我们可以获得更好的操作性能的关键操作。
# 经推导, 在任何时候，我们的AVL树的高度等于树中节点数目的对数的常数（1.44）倍。将搜索限制为O(logN）
import bintrees
from 查找树 import BinarySearchTree, TreeNode


class AVLBinarySearchTree(BinarySearchTree):
	def _put(self, key, val, currentNode):
		if key < currentNode.key:
			if currentNode.hasLeftChild():
				self._put(key, val, currentNode.leftChild)
			else:
				currentNode.leftChild = TreeNode(key, val, parent=currentNode)
				self.addUpdateBalance(currentNode.leftChild)
		elif key == currentNode.key:
			currentNode.payload = val
		else:
			if currentNode.hasRightChild():
				self._put(key, val, currentNode.rightChild)
			else:
				currentNode.rightChild = TreeNode(key, val, parent=currentNode)
				self.addUpdateBalance(currentNode.rightChild)

	def addUpdateBalance(self, node):
		if node.balanceFactor > 1 or node.balanceFactor < -1:
			self.rebalance(node)
			return
		if node.parent != None:
			if node.isLeftChild():
				node.parent.balanceFactor += 1
			elif node.isRightChild():
				node.parent.balanceFactor -= 1

			if node.parent.balanceFactor != 0:
				self.addUpdateBalance(node.parent)

	def delUpdateBalance(self, node):
		if node.balanceFactor > 1 or node.balanceFactor < -1:
			self.rebalance(node)
			return
		if node.parent != None:
			if node.isLeftChild():
				node.parent.balanceFactor -= 1
			elif node.isRightChild():
				node.parent.balanceFactor += 1

			if node.parent.balanceFactor != 0:
				self.delUpdateBalance(node.parent)

	def rebalance(self, node):
		if node.balanceFactor < 0:
			if node.rightChild.balanceFactor > 0:
				self.rotateRight(node.rightChild)
				self.rotateLeft(node)
			else:
				self.rotateLeft(node)
		elif node.balanceFactor > 0:
			if node.leftChild.balanceFactor < 0:
				self.rotateLeft(node.leftChild)
				self.rotateRight(node)
			else:
				self.rotateRight(node)

	# 根节点平衡因子为负数.
	# 提升右孩子（B）成为子树的根。
	# 将旧根（A）移动为新根的左子节点。
	# 如果新根（B）已经有一个左孩子，那么使它成为新左孩子（A）的右孩子。注意：由于新根（B）是A的右孩子，A的右孩子在这一点上保证为空。这允许我们添加一个新的节点作为右孩子，不需进一步的考虑。

	def rotateLeft(self, rotRoot):
		newRoot = rotRoot.rightChild
		rotRoot.rightChild = newRoot.leftChild
		if newRoot.leftChild != None:
			newRoot.leftChild.parent = rotRoot
		newRoot.parent = rotRoot.parent
		if rotRoot.isRoot():
			self.root = newRoot
		else:
			if rotRoot.isLeftChild():
				rotRoot.parent.leftChild = newRoot
			else:
				rotRoot.parent.rightChild = newRoot
		newRoot.leftChild = rotRoot
		rotRoot.parent = newRoot
		rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
		newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)

	def rotateRight(self, rotRoot):
		newRoot = rotRoot.leftChild
		rotRoot.leftChild = newRoot.rightChild
		if newRoot.rightChild != None:
			newRoot.rightChild.parent = rotRoot
		newRoot.parent = rotRoot.parent
		if rotRoot.isRoot():
			self.root = newRoot
		else:
			if rotRoot.isLeftChild():
				rotRoot.parent.leftChild = newRoot
			else:
				rotRoot.parent.rightChild = newRoot
		newRoot.rightChild = rotRoot
		rotRoot.parent = newRoot
		rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
		newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(0, rotRoot.balanceFactor)

	def remove(self, currentNode):
		if currentNode.isLeaf():
			self.delUpdateBalance(currentNode)
			currentNode.spliceOut()

		elif currentNode.hasBothChildren():
			succ = currentNode.findSuccessor()
			currentNode.key = succ.key
			currentNode.payload = succ.payload
			self.delUpdateBalance(succ)
			succ.spliceOut()

		else:  # this node has one child
			if currentNode.hasLeftChild():
				if not currentNode.isRoot():
					self.delUpdateBalance(currentNode)
					currentNode.spliceOut()
				else:
					currentNode.replaceNodeData(currentNode.leftChild.key,
					                            currentNode.leftChild.payload,
					                            currentNode.leftChild.leftChild,
					                            currentNode.leftChild.rightChild)
					currentNode.balanceFactor -= 1

			else:
				if not currentNode.isRoot():
					self.delUpdateBalance(currentNode)
					currentNode.spliceOut()
				else:
					currentNode.replaceNodeData(currentNode.rightChild.key,
					                            currentNode.rightChild.payload,
					                            currentNode.rightChild.leftChild,
					                            currentNode.rightChild.rightChild)
					currentNode.balanceFactor += 1


def height_node(tree_node):
	if not tree_node:
		return 0
	else:
		return 1 + max(height_node(tree_node.leftChild), height_node(tree_node.rightChild))


def is_balanced(tree_node):
	return abs(height_node(tree_node.leftChild) - height_node(tree_node.rightChild)) <= 1


val = AVLBinarySearchTree()
val[1] = 'a'
val[2] = 'b'
val[4] = 'c'
val[7] = 'd'
val[8] = 'a'
val[9] = 'b'
val[10] = 'c'
val[17] = 'd'
val[21] = 'a'
val[42] = 'b'
val[54] = 'c'
val[37] = 'd'
val[71] = 'a'
val[82] = 'b'
val[94] = 'c'
val[47] = 'd'

val.delete(7)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(7, 'a')
val.delete(54)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(54, 'a')
val.delete(37)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(37, 'a')
val.delete(71)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(71, 'a')
val.delete(82)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(82, 'a')
val.delete(94)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(94, 'a')
val.delete(47)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(47, 'a')
val.delete(8)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)
val.put(8, 'a')
val.delete(17)
print('is_balanced->', is_balanced(val.root))
print('height_node->', height_node(val.root))
print('val.root.key', val.root.key)


# 					       17
# 			  7			                42
# 	 2               9           37              71
# 1    4          8     10    21    47       54      82
# 		                                               94
