# username - nirorlansky
# id1      - 209510908
# name1    - nir orlansky
# id2      - 207765181
# name2    - omer shalev

"""A class represnting a node in an AVL tree"""
# import random  #for tests

class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key=None, value=None):
        #AVLNode builder. initialize a node in O(1).
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child (if self is virtual)
    """

    def get_left(self):
        #time complexity O(1)
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child (if self is virtual)
    """

    def get_right(self):
        #time complexity O(1)
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def get_parent(self):
        #time complexity O(1)
        return self.parent

    """returns the key

    @rtype: int or None
    @returns: the key of self, None if the node is virtual
    """

    def get_key(self):
        #time complexity O(1)
        return self.key

    """returns the value

    @rtype: any
    @returns: the value of self, None if the node is virtual
    """

    def get_value(self):
        #time complexity O(1)
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def get_height(self):
        #time complexity O(1)
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        #time complexity O(1)
        self.left = node
        return None

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        #time complexity O(1)
        self.right = node
        return None

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        #time complexity O(1)
        self.parent = node
        return None

    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        #time complexity O(1)
        self.key = key
        return None

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        #time complexity O(1)
        self.value = value
        return None

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        #time complexity O(1)
        self.height = h
        return None

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        #time complexity O(1)
        return self.key != None


"""
A class implementing the ADT Dictionary, using an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        #AVLTree builder. initialize an empty tree with a virtual Node as root in O(1).
        self.root = AVLNode()
        self.tree_size = 0

    # add your fields here

    """searches for a AVLNode in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: the AVLNode corresponding to key or None if key is not found.
    """

    def search(self, key):
        # Search for key in tree. calls the function searchNode which does binary search. Time complexity O(logn).
        node = self.searchNode(self.root, key)
        return node if node.is_real_node() else None

    def searchNode(self, node, key):
        # Search a key in subtree. if key exists return node, if not, return the the virtual node that in the key's position.
        #Using binary search. time complexity O(logn)
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
        #time complexity O(logn) for insertBST and at most 1 gilgul O(1) hence in total O(logn)
        self.tree_size += 1
        node = self.insertBST(key, val)
        parent = node.get_parent()
        cnt_gilgul = 0
        #checking if the new tree after the insertion is a valid AVL tree.
        while parent is not None:
            parent_height = self.calcHeight(parent)
            parent_bf = self.bf(parent)
            if parent_height == parent.get_height() and abs(parent_bf) < 2:
                return cnt_gilgul
            elif abs(parent_bf) < 2:
                parent.set_height(parent_height)
                cnt_gilgul += 1
                parent = parent.get_parent()
            else:
                #As mentioned in class, after one gilgul at most, the tree will be a valid AVL tree.
                cnt_gilgul += self.gilgul(parent, parent_bf)
                return cnt_gilgul
        return cnt_gilgul

    def insertBST(self, key, val):
        #Search the location where the new node should be inserted.returns a Virtual node in this position. O(logn).
        node = self.searchNode(self.root, key)
        #updating the virtual node's values and adding two virtual sons.
        node.set_key(key)
        node.set_value(val)
        node.set_right(AVLNode())
        node.set_left(AVLNode())
        node.get_right().set_parent(node)
        node.get_left().set_parent(node)
        node.set_height(node.get_height() + 1)
        return node

    def bf(self, node):
        # Calculates the balance factor of a node. O(1)
        return node.get_left().get_height() - node.get_right().get_height()

    def calcHeight(self, node):
        #Calculate the height of a node based on the heights of its sons. O(1)
        return (max(node.get_left().get_height(), node.get_right().get_height()) + 1)

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def gilgul(self, node, node_bf):
        #making rotations to fix problematic nodes with big BF. maximum rotations number is 2, time complexity O(1)
        cnt = 0
        if node_bf == 2:
            left_son = node.get_left()
            left_son_bf = self.bf(left_son)
            #Checking if two rotations are needed.
            if left_son_bf < 0:
                cnt += self.gilgulLeft(left_son)
            cnt += self.gilgulRight(node)
        if node_bf == -2:
            right_son = node.get_right()
            right_son_bf = self.bf(right_son)
            #checking if two rotations are needed.
            if right_son_bf > 0:
                cnt += self.gilgulRight(right_son)
            cnt += self.gilgulLeft(node)
        return cnt

    def gilgulRight(self, node):
		#changing pointers, the number of changes is fixed. time complexity O(1)
        left_son = node.get_left()
        node.set_left(left_son.get_right())
        node.get_left().set_parent(node)
        left_son.set_right(node)
        left_son.set_parent(node.get_parent())
        # check if left son is a right or left son of node's parent
        if left_son.get_parent() is not None and left_son.get_key() < left_son.get_parent().get_key():
            left_son.get_parent().set_left(left_son)
        elif left_son.get_parent() is not None:
            left_son.get_parent().set_right(left_son)
        else:
            self.root = left_son
        node.set_parent(left_son)
        node.set_height(self.calcHeight(node))
        left_son.set_height(self.calcHeight(left_son))
        return 1

    def gilgulLeft(self, node):
        #changing pointers, the number of changes is fixed. time complexity O(1)
        right_son = node.get_right()
        node.set_right(right_son.get_left())
        node.get_right().set_parent(node)
        right_son.set_left(node)
        right_son.set_parent(node.get_parent())
        # check if right son is a right or left son of node's parent
        if right_son.get_parent() is not None and right_son.get_key() < right_son.get_parent().get_key():
            right_son.get_parent().set_left(right_son)
        elif right_son.get_parent() is not None:
            right_son.get_parent().set_right(right_son)
        else:
            self.root = right_son
        node.set_parent(right_son)
        node.set_height(self.calcHeight(node))
        right_son.set_height(self.calcHeight(right_son))
        return 1

    def delete(self, node):
        #deleting a node from the tree. using BSTdelete to delete the correct node, time complexity O(logn)
        #go up the tree from the deleted node and calling gilgul to fix problems that may have happened.O(logn)
        #return the number of adjusments made to correct the tree.
        #Time complexity O(logn)
        self.tree_size -= 1
        cnt_gilgul = 0
        parent = self.BSTdelete(node)
        while parent is not None:
            parent_bf = self.bf(parent)
            parent_height = self.calcHeight(parent)
            if abs(parent_bf) < 2 and parent.get_height() == parent_height:
                return cnt_gilgul
            elif abs(parent_bf) < 2:
                parent.set_height(parent_height)
                cnt_gilgul += 1
                parent = parent.get_parent()
            else:
                tmp_parent = parent.get_parent()
                cnt_gilgul += self.gilgul(parent, parent_bf)
                parent = tmp_parent
        return cnt_gilgul

    def minSubTree(self, node):
        #find the minimum key in the sub tree where node is the root. Time complexity O(h) = O(logn)
        while node.get_left().is_real_node():
            node = node.get_left()
        return node

    def maxSubTree(self, node):
        #find the maximum key in the sub tree where node is the root. time complexity O(h) = O(logn)
        while node.get_right().is_real_node():
            node = node.get_right()
        return node

    def succesor(self, node):
        #find the successor of a given node in a tree.
        #Going up or down the tree to find the successor key.
        #calling the function minSubTree which is O(logn)
        #Time complexity O(h) = O(logn)
        if node.get_right().is_real_node():
            return self.minSubTree(node.get_right())
        parent = node.get_parent()
        while parent is not None and node == parent.get_right():
            node = parent
            parent = node.get_parent()
        return parent

    def BSTdelete(self, node):
        #deleting a node from the tree.
        #changes a fixed amount of pointers, calling the function succesor which is O(logn)
        #time complexity O(logn)

        #the node has two real sons.
        if node.get_left().is_real_node() and node.get_right().is_real_node():
            suc = self.succesor(node)
            #deleting the successor of node from the tree. suc cannot have two children.
            parent = self.deleteEasy(suc)
            #placing suc in the location of node in the tree.
            suc.set_right(node.get_right())
            suc.set_left(node.get_left())
            node.get_left().set_parent(suc)
            node.get_right().set_parent(suc)
            #if deleting the root.
            if node.get_parent() is None:
                self.root = suc
            elif node.get_parent().get_key() < suc.get_key():
                node.get_parent().set_right(suc)
            else:
                node.get_parent().set_left(suc)
            suc.set_parent(node.get_parent())
            suc.set_height(node.get_height())
        #the node has less than 2 real children
        else:
            parent = self.deleteEasy(node)
        if parent is node:
            suc.set_height(node.get_height())
            parent = suc
        return parent

    def deleteEasy(self, node):
        #handeling deleting a node when it has only one or zero childs.
        #returns the parent of the deleted node.
        #only changes a fixed number of pointers and therefore the time complexity is O(1)
        left = node.get_left().is_real_node()
        parent = node.get_parent()
        #only has right child or no childs
        if not left:
            #the node is the root of a tree
            if parent is None:
                self.root = node.get_right()
                node.get_right().set_parent(None)
                node.set_right(None)
            #the node is not the root
            else:
                #the node is left son of his parent
                if node.get_key() < parent.get_key():
                    parent.set_left(node.get_right())
                    node.get_right().set_parent(parent)
                    node.set_right(None)
                    node.set_parent(None)
                #the node is right son of his parent
                else:
                    parent.set_right(node.get_right())
                    node.get_right().set_parent(parent)
                    node.set_right(None)
                    node.set_parent(None)
        #has only left child. this function won't be called when node has 2 children.
        elif left:
            #node is the root of a tree
            if parent is None:
                self.root = node.get_left()
                node.get_left().set_parent(None)
                node.set_left(None)
            else:
                #node is the left son of his parent
                if node.get_key() < parent.get_key():
                    parent.set_left(node.get_left())
                    node.get_left().set_parent(parent)
                    node.set_left(None)
                    node.set_parent(None)
                #node is the right son of his parent
                else:
                    parent.set_right(node.get_left())
                    node.get_left().set_parent(parent)
                    node.set_left(None)
                    node.set_parent(None)
        return parent

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        #initalizing an empty array with the size of the tree.O(n)
        #calling minSubTree to find the minimum key in the tree O(logn)
        #calling successor for each node until going through all the nodes. As seen in class O(n+h) = O(n+logn)
        #time complexity O(n)
        arr = [0 for i in range(self.tree_size)]
        node = self.minSubTree(self.root)
        i = 0
        while node is not None:
            arr[i] = (node.get_key(), node.get_value())
            i += 1
            node = self.succesor(node)
        if i != len(arr):
            arr = arr[:i]
        return arr

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
		#time complexity O(1)
        return self.tree_size

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
        #going up the tree from node. O(h) = O(logn)
        #in every iteration, calling join.
        #as we saw in class, time complexity is O(logn)
        key = node.get_key()
        left = AVLTree()
        left.root = node.get_left()
        left.root.set_parent(None)
        right = AVLTree()
        right.root = node.get_right()
        right.root.set_parent(None)
        parent = node.get_parent()
        node.set_parent(None)
        node.set_left(None)
        node.set_right(None)
        while parent is not None:
            next = parent.get_parent()
            if parent.get_key() < key:
                parent_left = AVLTree()
                parent_left.root = parent.get_left()
                parent_left.joinWithNode(parent, left)
                left = parent_left
            else:
                parent_right = AVLTree()
                parent_right.root = parent.get_right()
                right.joinWithNode(parent, parent_right)
            parent = next
            left.root.set_parent(None)
            right.root.set_parent(None)
        left.tree_size = self.size()
        right.tree_size = self.size()
        return left, right



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
        # creates a node with key and val and use it to call joinWithNode.
        #checks for the subtree with the bigger keys to stand in the requirments of joinWithNode.
        #time complexity O(abs(self.get_height() - tree2.get_height()) + 1))
        node = AVLNode(key,val)
        if not tree2.root.is_real_node() or tree2.root.get_key() > key:
            return self.joinWithNode(node, tree2)
        diff = tree2.joinWithNode(node, self)
        self.root = tree2.get_root()
        self.tree_size = tree2.size()
        tree2.root = AVLNode()
        tree2.tree_size = 0
        return diff

    def joinWithNode(self, node, tree2):
        #the function requires that tree2 will have smaller values than in self.
        #going down the heigher tree O(diff)
        #Joining the two subtrees with the same heights by changing pointers. O(1)
        #going up the joined tree and fix nodes if needed. O(diff)
        #time complexity O(diff) = O(abs(smaller.get_height() - bigger.get_height()) + 1)

        smaller = self.root
        bigger = tree2.root
        diff = abs(smaller.get_height() - bigger.get_height()) + 1
        #smaller is lower than bigger
        if smaller.get_height() < bigger.get_height():
            h = smaller.get_height()
            curr = bigger
            while curr.get_height() > h:
                curr = curr.get_left()
            node.set_left(smaller)
            node.set_right(curr)
            node.set_parent(curr.get_parent())
            smaller.set_parent(node)
            curr.set_parent(node)
            if node.get_parent() is not None:
                node.get_parent().set_left(node)
                self.root = bigger
            else:
                self.root = node
        # smaller and bigger have the same height
        elif smaller.get_height() == bigger.get_height():
            h = smaller.get_height()
            node.set_left(smaller)
            node.set_right(bigger)
            smaller.set_parent(node)
            bigger.set_parent(node)
            self.root = node
        # bigger is lower than smaller
        else:
            h = bigger.get_height()
            curr = smaller
            while curr.get_height() > h:
                curr = curr.get_right()
            node.set_right(bigger)
            node.set_left(curr)
            node.set_parent(curr.get_parent())
            bigger.set_parent(node)
            curr.set_parent(node)
            if node.get_parent() is not None:
                node.get_parent().set_right(node)
                self.root = smaller
            else:
                self.root = node
        self.root.set_parent(None)
        node.set_height(h+1)
        parent = node.get_parent()
        self.tree_size += tree2.tree_size + 1
        #checking for every node in the path from node to the root of the new joined tree if it is valid.
        #The number of nodes checked is at most diff.
        while parent is not None:
            parent_height = self.calcHeight(parent)
            parent_bf = self.bf(parent)
            if parent_height == parent.get_height() and abs(parent_bf) < 2:
                return diff
            elif abs(parent_bf) < 2:
                parent.set_height(parent_height)
                parent = parent.get_parent()
            else:
                self.gilgul(parent, parent_bf)
                return diff
        return diff


    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        #time complexity O(1)
        return self.root if self.root.is_real_node() else None


# def test():
#     treeArr = [None for i in range(10)]
#     treeArr2 = [None for i in range(10)]
#     for j in range(1,11):
#         tree = AVLTree()
#         tree2 = AVLTree()
#         keys = [i for i in range(1000*(2**j))]
#         for key in keys:
#             tree.insert(key,key)
#             tree2.insert(key,key)
#         treeArr[j-1] = tree
#         treeArr2[j-1] = tree2
#         print("tree added")
#     for tree in treeArr:
#         # node = tree.maxSubTree(tree.root.get_left())
#         num = random.randint(0,tree.size()-1)
#         node = tree.search(num)
#         tree.split(node)
#         print("")
