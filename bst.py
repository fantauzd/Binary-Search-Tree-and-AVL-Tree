# Name: Dominic Fantauzzo
# OSU Email: fantauzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 - BST/AVL Tree Implementation
# Due Date: 2/27/2024
# Description: Implementation of a BST class


import random
from queue_and_stack import *


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree. Duplicate values are allowed. If a node with
        that value is already in the tree, the new value should be added to the right subtree of that node.
        """
        # Ensure that the node has a root, or make one
        if self._root is None:
            self._root = BSTNode(value)
        # Find the location of the node we are adding and store its parent
        else:
            parent = None
            n = self._root
            while n is not None:
                parent = n
                if value < n.value:
                    n = n.left
                else:
                    n = n.right
            # Create a new node as the left or right child of the stored parent node
            if value < parent.value:
                parent.left = BSTNode(value)
            else:
                parent.right = BSTNode(value)

    def remove(self, value: object) -> bool:
        """
        This method removes a value from the tree. The method returns True if the value is
        removed. Otherwise, it returns False.
        """
        result = self.find_node_and_parent(value)
        # If there is no matching value to remove we return False
        if result:
            n, pn = result[0], result[1]
            children = self.count_children(n)
            # Use appropriate method for number of children and return True
            if children == 0:
                self._remove_no_subtrees(pn, n)
            elif children == 1:
                self._remove_one_subtree(pn, n)
            else:
                self._remove_two_subtrees(pn, n)
            n.left = n.right = None      # free n
            return True
        else:
            return False

    def find_node_and_parent(self, value: object) -> [BSTNode]:
        """
        Returns the first node with the same value as the value parameter, and its parent.
        If no node in the BST matches the value parameter or if the root of the BST
        matches the value parameter than the method returns None.

        :return: A list of the matching node and its parent, like [node, parent]
        """
        # If the BST is empty or the value is the root, then there is no parent node
        parent = None
        n = self._root
        # Searches for matching value in tree
        while n is not None:
            if n.value == value:
                return [n, parent]
            # parent trails one node behind n
            parent = n
            if value < n.value:
                n = n.left
            else:
                n = n.right
        return None

    def count_children(self, node: BSTNode) -> int:
        """
        Counts the number of children that a node in a BST has and returns an integer between [0, 2].
        """
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove node that has no subtrees (no left or right nodes).
        """
        # If the node we are removing is the root, parent will be None.
        if remove_parent:
            if remove_node.value < remove_parent.value:
                remove_parent.left = None
            else:
                remove_parent.right = None
        else:
            self._root = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove node that has a left or right subtree (only).
        """
        # If the node we are removing is the root, parent will be None.
        if remove_parent:
            # Replacing left path of parent node to whichever side of the removal node exists
            if remove_node.value < remove_parent.value:
                if remove_node.left:
                    remove_parent.left = remove_node.left
                else:
                    remove_parent.left = remove_node.right
            # Replacing right path of parent node to whichever side of the removal node exists
            else:
                if remove_node.left:
                    remove_parent.right = remove_node.left
                else:
                    remove_parent.right = remove_node.right
        # If there is no parent of the removal node, we update the root pointer instead
        else:
            if remove_node.left:
                self._root = remove_node.left
            else:
                self._root = remove_node.right

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Remove node that has two subtrees.
        """
        # Find the successor node and its parent
        result = self.find_successor_and_parent(remove_node)
        s, ps = result[0], result[1]
        # Update pointers to give the removal node's children to its successor
        s.left = remove_node.left
        if s is not remove_node.right:
            ps.left = s.right
            s.right = remove_node.right
        # Update the parent of the removal node to point to successor
        if remove_parent:
            if remove_node.value < remove_parent.value:
                remove_parent.left = s
            else:
                remove_parent.right = s
        # If there is no parent of the removal node, we update the root pointer instead
        else:
            self._root = s

    def find_successor_and_parent(self, remove_node: BSTNode) -> [BSTNode]:
        """
        Takes a node in a BST tree and returns its successor and the parent of its successor.
        Returns None for both successor and parent if the node parameter does not have a right subtree.

        :return: A list of the successor and its parent, like [successor, successor's parent]
        """
        # If there is no successor, s and ps are set to None
        ps = None
        s = remove_node.right
        # If successor exists, then initialize s to removal node's right and ps to the removal node
        if s:
            ps = remove_node
            while s is not None:
                if s.left is None:
                    return [s, ps]
                else:
                    ps = s
                    s = s.left
        return [s, ps]      # Only occurs when there is no successor

    def contains(self, value: object) -> bool:
        """
        This method returns True if the value is in the tree. Otherwise, it returns False. If the tree is
        empty, the method returns False.
        """
        n = self._root
        # Search using binary search in O(h)
        while n is not None:
            if n.value == value:
                return True
            elif value < n.value:
                n = n.left
            else:
                n = n.right
        return False

    def inorder_traversal(self) -> Queue:
        """
        This method will perform an inorder traversal of the tree and return a Queue object that
        contains the values of the visited nodes, in the order they were visited. If the tree is empty,
        the method returns an empty Queue.

        Note: I wanted to try an iterative method to have some fun with the stack class. A recursive versio would be
        logically equivalent as you would simply replace the stack below with a stack of function calls.
        """
        result = Queue()
        stack = Stack()
        n = self._root
        while True:
            # Push the current node and go left
            if n is not None:
                stack.push(n)
                n = n.left
            # Once we cannot go left or right, process the top of stack, and go right
            elif not stack.is_empty():
                n = stack.pop()
                result.enqueue(n.value)
                n = n.right
            else:
                return result

    def find_min(self) -> object:
        """
        This method returns the lowest value in the tree. If the tree is empty, the method should return None.
        """
        min = self._root
        while min and min.left:
            min = min.left
        if min is None:
            return None
        return min.value

    def find_max(self) -> object:
        """
        This method returns the highest value in the tree. If the tree is empty, the method should return None.
        """
        max = self._root
        while max and max.right:
            max = max.right
        if max is None:
            return None
        return max.value

    def is_empty(self) -> bool:
        """
        This method returns True if the tree is empty. Otherwise, it returns False.
        """
        return self._root is None

    def make_empty(self) -> None:
        """
        This method removes all the nodes from the tree.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
