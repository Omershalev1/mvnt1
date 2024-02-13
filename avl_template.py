# username - nirorlansky
# id1      - 209510908
# name1    - nir orlansky
# id2      - 207765181
# name2    - omer shalev


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key=None, value=None):
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
        self.root = AVLNode()

    # add your fields here

    """searches for a AVLNode in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: the AVLNode corresponding to key or None if key is not found.
    """

    def search(self, key):
        # Searched for key in tree. Time complexity O(logn)
        node = self.searchNode(self.root, key)
        return node if node.is_real_node() else None

    def searchNode(self, node, key):
        # Search a key in subtree. if key exists return node, if not, return the the virtual node that in the key's position.
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
        node = self.insertBST(key, val)
        parent = node.get_parent()
        cnt_gilgul = 0
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
                cnt_gilgul += self.gilgul(parent, parent_bf)
                return cnt_gilgul
        return cnt_gilgul

    def insertBST(self, key, val):
        node = self.searchNode(self.root, key)
        node.set_key(key)
        node.set_value(val)
        node.set_right(AVLNode())
        node.set_left(AVLNode())
        node.get_right().set_parent(node)
        node.get_left().set_parent(node)
        node.set_height(node.get_height() + 1)
        return node

    def bf(self, node):
        # Calculates the balance factor of a node.
        return node.get_left().get_height() - node.get_right().get_height()

    def calcHeight(self, node):
        return (max(node.get_left().get_height(), node.get_right().get_height()) + 1)

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def gilgul(self, node, node_bf):
        cnt = 0
        if node_bf == 2:
            left_son = node.get_left()
            left_son_bf = self.bf(left_son)
            if left_son_bf < 0:
                cnt += self.gilgulLeft(left_son)
            cnt += self.gilgulRight(node)
        if node_bf == -2:
            right_son = node.get_right()
            right_son_bf = self.bf(right_son)
            if right_son_bf > 0:
                cnt += self.gilgulRight(right_son)
            cnt += self.gilgulLeft(node)
        return cnt

    def gilgulRight(self, node):
        left_son = node.get_left()
        node.set_left(left_son.get_right())
        node.get_left().set_parent(node)
        left_son.set_right(node)
        left_son.set_parent(node.get_parent())
        # check if left son id on right ot left son of node's parent
        if left_son.get_parent() is not None and left_son.get_key() < left_son.get_parent().get_key():
            left_son.get_parent().set_left(left_son)
        elif left_son.get_parent() is not None:
            left_son.get_parent().set_right(left_son)
        else:
            self.root = left_son
        node.set_parent(left_son)
        node.set_height(self.calcHeight(node))
        left_son.set_height(self.calcHeight(left_son))
        self.root.display()
        return 1

    def gilgulLeft(self, node):
        right_son = node.get_right()
        node.set_right(right_son.get_left())
        node.get_right().set_parent(node)
        right_son.set_left(node)
        right_son.set_parent(node.get_parent())
        # check if right son id on right ot left son of node's parent
        if right_son.get_parent() is not None and right_son.get_key() < right_son.get_parent().get_key():
            right_son.get_parent().set_left(right_son)
        elif right_son.get_parent() is not None:
            right_son.get_parent().set_right(right_son)
        else:
            self.root = right_son
        node.set_parent(right_son)
        node.set_height(self.calcHeight(node))
        right_son.set_height(self.calcHeight(right_son))
        self.root.display()
        return 1

    def delete(self, node):
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
        while node.get_left().is_real_node():
            node = node.get_left()
        return node

    def succesor(self, node):
        if node.get_right().is_real_node():
            return self.minSubTree(node.get_right())
        parent = node.get_parent()
        while parent is not None and node == parent.get_right():
            node = parent
            parent = node.get_parent()
        return parent

    def BSTdelete(self, node):
        if node.get_left().is_real_node() and node.get_right().is_real_node():
            suc = self.succesor(node)
            parent = self.deleteEasy(suc)
            suc.set_right(node.get_right())
            suc.set_left(node.get_left())
            node.get_left().set_parent(suc)
            node.get_right().set_parent(suc)
            if node.get_parent() is None:
                self.root = suc
            elif node.get_parent().get_key() < suc.get_key():
                node.get_parent().set_right(suc)
            else:
                node.get_parent().set_left(suc)
            suc.set_parent(node.get_parent())
            suc.set_height(node.get_height())
        else:
            parent = self.deleteEasy(node)
        return parent if parent != node else suc

    def deleteEasy(self, node):
        left = node.get_left().is_real_node()
        parent = node.get_parent()
        if not left:
            if parent is None:
                self.root = node.get_right()
                node.get_right().set_parent(None)
                node.set_right(None)
            else:
                if node.get_key() < parent.get_key():
                    parent.set_left(node.get_right())
                    node.get_right().set_parent(parent)
                    node.set_right(None)
                    node.set_parent(None)
                else:
                    parent.set_right(node.get_right())
                    node.get_right().set_parent(parent)
                    node.set_right(None)
                    node.set_parent(None)
        elif left:
            if parent is None:
                self.root = node.get_left()
                node.get_left().set_parent(None)
                node.set_left(None)
            else:
                if node.get_key() < parent.get_key():
                    parent.set_left(node.get_left())
                    node.get_left().set_parent(parent)
                    node.set_left(None)
                    node.set_parent(None)
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
        return None


def test():
    tree = AVLTree()
    tree.insert(8, "a")
    tree.root.display()
    tree.insert(4, "b")
    tree.root.display()
    tree.insert(5, "c")
    tree.root.display()
    tree.insert(10, "d")
    tree.root.display()
    tree.insert(9, "e")
    tree.root.display()
    tree.insert(12, "4")
    tree.insert(11, "e")
    tree.root.display()
    tree.insert(13, "e")
    tree.root.display()

    print(tree.delete(tree.search(9)))
    print(tree.root.height)
    tree.root.display()


test()
