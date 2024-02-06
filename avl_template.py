#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

from re import search


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type key: int or None
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		
	def display(self):
		lines, *_ = self._display_aux()
		for line in lines:
			print(line)

	def _display_aux(self):
		"""Returns list of strings, width, height, and horizontal coordinate of the root."""
		# No child.
		if self.right is None and self.left is None:
			line = '%s' % self.key + " " + str(self.parent.key) if self.parent is not None else '%s' % self.key
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

        # Only left child.
		if self.right is None:
			lines, n, p, x = self.left._display_aux()
			s = '%s' % self.key + " " + str(self.parent.key) if self.parent is not None else '%s' % self.key
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

		# Only right child.
		if self.left is None:
			lines, n, p, x = self.right._display_aux()
			s = '%s' % self.key + " " + str(self.parent.key) if self.parent is not None else '%s' % self.key
			u = len(s)
			first_line = s + x * '_' + (n - x) * ' '
			second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
			shifted_lines = [u * ' ' + line for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
		left, n, p, x = self.left._display_aux()
		right, m, q, y = self.right._display_aux()
		s = '%s' % self.key + " " + str(self.parent.key) if self.parent is not None else '%s' % self.key
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			left += [n * ' '] * (q - p)
		elif q < p:
			right += [m * ' '] * (p - q)
		zipped_lines = zip(left, right)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2


	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""
	def get_left(self):
		return self.left

	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent


	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node
		return None


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node
		return None


	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node
		return None



	def make_parent(self,parent, side = None):
		print(side)
		if side != None:
			if side == 'l':
				parent.get_left().set_parent(None)
				parent.set_left(self)
				if self.get_parent() is not None:
					self.get_parent().set_right(None)
			else:
				parent.get_right().set_parent(None)
				parent.set_right(self)
				if self.get_parent() is not None:
					self.get_parent().set_left(None)
		elif parent != None:
			if self.key < parent.get_key():
				if parent.get_left() is not None:
					parent.get_left().set_parent(None)
				parent.set_left(self)
			else:
				if parent.get_right() is not None:
					parent.get_right().set_parent(None)
				parent.set_right(self)
		self.parent = parent

	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key
		return None


	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value
		return None


	"""sets the height of the node

	@type h: int
	@param h: the height
	"""
	def set_height(self, h):
		self.height = h
		return None


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.key != None



"""
A class implementing the ADT Dictionary, using an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		# add your fields here

	"""searches for a AVLNode in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	"""
	def search(self, key):
		# Searched for key in tree. Time complexity O(logn)
		if self.root == None:
			return None
		node = self.searchNode(self.root, key)
		if node.is_real_node():
			return node
		return None

	def searchNode(self,node,key):
		#Search a key in subtree. if key exists return node, if not, return the the virtual node that in the key's position.
		while node.is_real_node():
			if node.key == key:
				return node
			if node.key > key:
				node = node.left
			else:
				node = node.right
		return node
	
	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		if self.root == None:
			node = AVLNode(None,None)
			self.root = node
		else:
			node = self.searchNode(self.root, key)
		self.initiateNode(node, key, val)
		counter = 0
		while (node.get_parent() != None):
			node = node.get_parent()
			curr_height = self.calcHeight(node)
			bf = self.bf(node)
			if node.get_height == curr_height and abs(bf) < 2:
				break
			if abs(bf) > 1:
				counter += self.gilgul(node)
				break
			node.set_height(curr_height)
		return counter
	
	def gilgul(self, criminalNode):
		gilgul_counter = 0
		bf = self.bf(criminalNode)
		if bf == 2:
			bf_left = self.bf(criminalNode.get_left())
			if bf_left == -1:
				self.gilgul_left(criminalNode.get_left())
				gilgul_counter += 1
			self.gilgul_right(criminalNode)
			gilgul_counter += 1

		if bf == -2:
			bf_right = self.bf(criminalNode.get_right())
			if bf_right == 1:
				self.gilgul_right(criminalNode.get_right())
				gilgul_counter += 1
			self.gilgul_left(criminalNode)
			gilgul_counter += 1
		
		return gilgul_counter

	def gilgul_left(self,criminalNode):
		#Do a gilgul to the left. time complexity O(1)
		right_son = criminalNode.get_right()
		right_son.get_left().make_parent(criminalNode,'r')
		right_son.display()
		criminalNode.display()
		right_son.make_parent(criminalNode.get_parent())
		right_son.display()
		criminalNode.display()
		criminalNode.make_parent(right_son)
		criminalNode.set_height(self.calcHeight(criminalNode))
		right_son.display()
		criminalNode.display()
		right_son.set_height(self.calcHeight(right_son))
		if self.root == criminalNode:
			self.root = right_son
		return
	
	def gilgul_right(self, criminalNode):
		#Do a gilgul to the right. time complexity O(1)
		left_son = criminalNode.get_left()
		left_son.get_right().make_parent(criminalNode,'l')
		left_son.make_parent(criminalNode.get_parent())
		criminalNode.make_parent(left_son)
		criminalNode.set_height(self.calcHeight(criminalNode))
		left_son.set_height(self.calcHeight(left_son))
		if self.root == criminalNode:
			self.root = left_son
		return

	
	def bf(self, node):
		#Calculates the balance factor of a node.
		return node.get_left().get_height() - node.get_right().get_height()

	def calcHeight(self, node):
		return (max(node.get_left().get_height(), node.get_right().get_height()) +1)

	def initiateNode(self,node,key,val):
		# Turns a virtual node into real node. time complexity O(1).
		node.set_key(key)
		node.set_value(val)
		leftChild = AVLNode(None,None)
		rightChild = AVLNode(None,None)
		node.set_left(leftChild)
		node.set_right(rightChild)
		node.set_height(node.height+1)
		leftChild.set_parent(node)
		rightChild.set_parent(node)
		return

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	# def delete(self, node):
	# 	parent = node.get_parent()
	# 	#node has exactly one child
	# 	if (node.get_left().is_real_node() and not node.get_right().is_real_node()) or (not node.get_left().is_real_node() and node.get_right().is_real_node()):
	# 		self.DeleteWithOne(node)
	# 	#node is root
	# 	if parent is None:
	# 		#node has zero sons
	# 		if not node.get_left().is_real_node() and not node.get_right().is_real_node():
	# 			self.root = None
	# 			return
	# 		#node has right son
	# 		elif not node.get_left().is_real_node():
	# 			self.root = node.get_right()
	# 			node.get_right().set_parent(None)
	# 			return
	# 		#node has left son
	# 		elif not node.get_right().is_real_node():
	# 			self.root = node.get_left()
	# 			node.get_left().set_parent(None)
	# 			return
	# 		#node has two children
	# 		else:
	# 			next = self.succesor(node)



	# 	node_key = node.get_key()
	# 	parent_key=parent.get_key()
	# 	is_left_child = parent_key > node_key


	# 			else:
	# 				if node_key < parent_key:
	# 					parent.set_left(node.get_left())
	# 				else:
	# 					parent.set_right(node.get_left())
	# 				node.get_left().set_parent(parent)
	# 			return
	# 		else:
	# 			#Only right son
	# 			if parent is None:
	# 				self.root = node.get_right()
	# 			else:
	# 				if parent_key > node_key

	# 	node.set_left(None)
	# 	node.set_right(None)
	# 	node.set_parent(None)

	# 	return -1


	# def DeleteWithOne(self,node):
	# 	parent = node.get_parent()
	# 	#node is root
	# 	if parent is None:
	# 		#node has right son
	# 		if not node.get_left().is_real_node():
	# 			self.root = node.get_right()
	# 			node.get_right().set_parent(None)
	# 			return
	# 		#node has left son
	# 		elif not node.get_right().is_real_node():
	# 			self.root = node.get_left()
	# 			node.get_left().set_parent(None)
	# 			return
	# 	#node is not root
	# 	else:

	
	def isLeftSon(self,parent,node):
		return node.get_key() < parent.get_key()

	def succesor(self,node):
		if node.get_right.is_real_node():
			return self.minSubTree(node.get_right())
		parent = node.get_parent()
		while parent is not None and node==parent.get_right():
			node = parent
			parent = node.get_parent()
		return parent
	
	def minSubTree(self,node):
		while node.get_left().is_real_node():
			node = node.get_left()
		return node

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		return None


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return -1	

	
	"""splits the dictionary at the i'th index

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		return None

	
	"""joins self with key and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree2
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def join(self, tree2, key, val):
		return None


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root
	

def test():
	tree = AVLTree()
	tree.insert(8, "a")
	tree.root.display()
	tree.insert(4, "b")
	tree.root.display()
	tree.insert(5, "c")
	tree.root.display()
	#tree.insert(10, "d")
	#tree.root.display()
	#tree.insert(9, "e")
	#tree.root.display()
	#tree.insert(11, "e")
	#tree.root.display()
	#tree.insert(13, "e")
	#tree.root.display()
test()					  