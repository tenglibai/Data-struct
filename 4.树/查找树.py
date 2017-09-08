class TreeNode:
	def __init__(self, key, val, left=None, right=None, parent=None, bal=0):
		self.key = key
		self.payload = val
		self.leftChild = left
		self.rightChild = right
		self.parent = parent
		self.balanceFactor = bal

	# __iter__ 覆盖 for x in操作，因此它是递归的

	def __iter__(self):
		if self:
			if self.hasLeftChild():
				for elem in self.leftChild:
					yield elem
			yield self
			if self.hasRightChild():
				for elem in self.rightChild:
					yield elem

	def hasLeftChild(self):
		return self.leftChild

	def hasRightChild(self):
		return self.rightChild

	def isLeftChild(self):
		return self.parent and self.parent.leftChild == self

	def isRightChild(self):
		return self.parent and self.parent.rightChild == self

	def isRoot(self):
		return not self.parent

	def isLeaf(self):
		return not (self.rightChild or self.leftChild)

	def hasAnyChildren(self):
		return self.rightChild or self.leftChild

	def hasBothChildren(self):
		return self.rightChild and self.leftChild

	def replaceNodeData(self, key, value, lc, rc):
		self.key = key
		self.payload = value
		self.leftChild = lc
		self.rightChild = rc
		if self.hasLeftChild():
			self.leftChild.parent = self
		if self.hasRightChild():
			self.rightChild.parent = self

	def spliceOut(self):
		if self.isLeaf():
			if self.isLeftChild():
				self.parent.leftChild = None
			else:
				self.parent.rightChild = None
		elif self.hasAnyChildren():
			if self.hasLeftChild():
				if self.isLeftChild():
					self.parent.leftChild = self.leftChild
				else:
					self.parent.rightChild = self.leftChild
				self.leftChild.parent = self.parent
			else:
				if self.isLeftChild():
					self.parent.leftChild = self.rightChild
				else:
					self.parent.rightChild = self.rightChild
				self.rightChild.parent = self.parent

	# 采用中序遍历,找下一个,分为如下三种情况:
	# 1.一个节点有右孩子，则在中序遍历中，该节点的后继是它的右子树的最左节点。
	# 2.这个节点是它父亲的左孩子，则该节点的后继节点是它的父亲
	# 3.这个节点是它父亲的右孩子，则需要一直向上搜索，直到它们n - 1
	#   代祖先是它第n代祖先的左孩子，则它的后继就是第n个祖先。如果一直搜索到根节点，也没有找到n - 1
	#   代祖先是它第n代祖先的左孩子，则该节点是整个树的中序遍历中的最后一个节点，即它没有后继。

	def findSuccessor(self):
		succ = None
		if self.hasRightChild():
			succ = self.rightChild.findMin()
		else:
			if self.parent:
				if self.isLeftChild():
					succ = self.parent
				else:
					self.parent.rightChild = None
					succ = self.parent.findSuccessor()
					self.parent.rightChild = self
		return succ

	def findMin(self):
		current = self
		while current.hasLeftChild():
			current = current.leftChild
		return current


class BinarySearchTree:
	def __init__(self):
		self.root = None
		self.size = 0

	def __iter__(self):
		if self:
			if self.root.hasLeftChild():
				for elem in self.root.leftChild:
					yield elem
			yield self.root
			if self.root.hasRightChild():
				for elem in self.root.rightChild:
					yield elem


	def length(self):
		return self.size

	def __len__(self):
		return self.size

	def put(self, key, val):
		if self.root:
			self._put(key, val, self.root)
		else:
			self.root = TreeNode(key, val)
		self.size = self.size + 1

	def _put(self, key, val, currentNode):
		if key < currentNode.key:
			if currentNode.hasLeftChild():
				self._put(key, val, currentNode.leftChild)
			else:
				currentNode.leftChild = TreeNode(key, val, parent=currentNode)
		elif key == currentNode.key:
			currentNode.payload = val
		else:
			if currentNode.hasRightChild():
				self._put(key, val, currentNode.rightChild)
			else:
				currentNode.rightChild = TreeNode(key, val, parent=currentNode)

	def __setitem__(self, k, v):
		self.put(k, v)

	def get(self, key):
		if self.root:
			res = self._get(key, self.root)
			if res:
				return res.payload
			else:
				return None
		else:
			return None

	def _get(self, key, currentNode):
		if not currentNode:
			return None
		elif currentNode.key == key:
			return currentNode
		elif key < currentNode.key:
			return self._get(key, currentNode.leftChild)
		else:
			return self._get(key, currentNode.rightChild)

	def __getitem__(self, key):
		return self.get(key)

	def __contains__(self, key):
		if self._get(key, self.root):
			return True
		else:
			return False

	def delete(self, key):
		if self.size > 1:
			nodeToRemove = self._get(key, self.root)
			if nodeToRemove:
				self.remove(nodeToRemove)
				self.size = self.size - 1
			else:
				raise KeyError('Error, key not in tree')
		elif self.size == 1 and self.root.key == key:
			self.root = None
			self.size = self.size - 1
		else:
			raise KeyError('Error, key not in tree')

	def __delitem__(self, key):
		self.delete(key)

	def remove(self, currentNode):
		if currentNode.isLeaf():  # leaf
			if currentNode == currentNode.parent.leftChild:
				currentNode.parent.leftChild = None
			else:
				currentNode.parent.rightChild = None
		elif currentNode.hasBothChildren():  # interior
			succ = currentNode.findSuccessor()
			succ.spliceOut()
			currentNode.key = succ.key
			currentNode.payload = succ.payload

		else:  # this node has one child
			if currentNode.hasLeftChild():
				if currentNode.isLeftChild():
					currentNode.leftChild.parent = currentNode.parent
					currentNode.parent.leftChild = currentNode.leftChild
				elif currentNode.isRightChild():
					currentNode.leftChild.parent = currentNode.parent
					currentNode.parent.rightChild = currentNode.leftChild
				else:
					currentNode.replaceNodeData(currentNode.leftChild.key,
					                            currentNode.leftChild.payload,
					                            currentNode.leftChild.leftChild,
					                            currentNode.leftChild.rightChild)
			else:
				if currentNode.isLeftChild():
					currentNode.rightChild.parent = currentNode.parent
					currentNode.parent.leftChild = currentNode.rightChild
				elif currentNode.isRightChild():
					currentNode.rightChild.parent = currentNode.parent
					currentNode.parent.rightChild = currentNode.rightChild
				else:
					currentNode.replaceNodeData(currentNode.rightChild.key,
					                            currentNode.rightChild.payload,
					                            currentNode.rightChild.leftChild,
					                            currentNode.rightChild.rightChild)


mytree = BinarySearchTree()
mytree[3] = "red"
mytree[4] = "blue"
mytree[6] = "yellow"
mytree[2] = "at"

for node in mytree.root:
	print('[{}]:[{}]'.format(node.key, node.payload))

mytree[3] = "test"

for node in mytree.root:
	print('[{}]:[{}]'.format(node.key, node.payload))

''''''''''''''
# 因实现了__iter__特殊方法
# for node in mytree.root:
# 	print('[{}]:[{}]'.format(node.key, node.payload))
# print()
# 相当于:

# lst_iterator = iter(mytree.root)  # this just calls `lst.__iter__()`
# while True:
# 	try:
# 		item = next(lst_iterator)  # lst_iterator.__next__()
# 	except StopIteration:
# 		break
# 	else:
# 		print(item.key)
