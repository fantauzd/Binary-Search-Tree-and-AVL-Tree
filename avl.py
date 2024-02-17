# Name: Dominic Fantauzzo
# OSU Email: fantauzd@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4 - BST/AVL Tree Implementation
# Due Date: 2/27/2024
# Description: Implementation of an AVL class, a subclass of BST that always remains balanced


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree while maintaining its AVL property. Duplicate
        values are not allowed. If the value is already in the tree, the method does not change
        the tree.
        """
        # Ensure that the node has a root, or make one
        if self._root is None:
            self._root = AVLNode(value)
        # Find the location of the node we are adding and store its parent
        else:
            parent = None
            n = self._root
            while n is not None:
                parent = n
                if value < n.value:
                    n = n.left
                # If we find the same value in the tree, return None (no duplicates)
                elif value == n.value:
                    return None
                else:
                    n = n.right
            # Create a new node as the left or right child of the stored parent node
            if value < parent.value:
                parent.left = AVLNode(value)
                parent.left.parent = parent
            else:
                parent.right = AVLNode(value)
                parent.right.parent = parent
            # Travel up the tree until we reach the node, rebalance (when needed to maintain AVL property)
            # and update height at each ancestor
            while parent:
                self._rebalance(parent)
                if parent.parent:
                    parent = parent.parent
                else:
                    parent = None

    def remove(self, value: object) -> bool:
        """
        TODO: Write your implementation
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
                pn = self._remove_two_subtrees(pn, n)
            n.left = n.right = None  # free n
            # Travel up the tree until we reach the node, rebalance (when needed to maintain AVL property)
            # and update height at each ancestor
            while pn:
                self._rebalance(pn)
                pn = pn.parent
            return True
        else:
            return False

    def _remove_no_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        Remove node that has no subtrees (no left or right nodes).
        """
        # If the node we are removing is the root, remove_parent will be None.
        if remove_parent:
            if remove_node.value < remove_parent.value:
                remove_parent.left = None
            else:
                remove_parent.right = None
        else:
            self._root = None

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        Remove node that has a left or right subtree (only).
        """
        # If the node we are removing is the root, parent will be None.
        if remove_parent:
            # Replacing left path of parent node to whichever side of the removal node exists
            if remove_node.value < remove_parent.value:
                if remove_node.left:
                    remove_parent.left = remove_node.left
                    remove_node.left.parent = remove_parent
                else:
                    remove_parent.left = remove_node.right
                    remove_node.right.parent = remove_parent
            # Replacing right path of parent node to whichever side of the removal node exists
            else:
                if remove_node.left:
                    remove_parent.right = remove_node.left
                    remove_node.left.parent = remove_parent
                else:
                    remove_parent.right = remove_node.right
                    remove_node.right.parent = remove_parent
        # If there is no parent of the removal node, we update the root pointer instead
        else:
            if remove_node.left:
                self._root = remove_node.left
                remove_node.left.parent = None
            else:
                self._root = remove_node.right
                remove_node.right.parent = None

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Remove AVL node that has two subtrees. Returns the parent of the successor node, which is used to
        replace the removed node. Rebalancing should begin at the parent of the successor node.
        """
        # Find the successor node and its parent
        result = self.find_successor_and_parent(remove_node)
        s, ps = result[0], result[1]
        # store the successor as the lowest modified node
        low_mod = s
        # Update pointers to give the removal node's children to its successor
        s.left = remove_node.left
        remove_node.left.parent = s
        if s is not remove_node.right:
            # If the parent of s is not being removed, then that is the lowest modified node (losing children)
            low_mod = ps
            ps.left = s.right
            if s.right:
                s.right.parent = ps
            s.right = remove_node.right
            remove_node.right.parent = s
        # Update the parent of the removal node to connect to successor
        if remove_parent:
            s.parent = remove_parent
            if remove_node.value < remove_parent.value:
                remove_parent.left = s
            else:
                remove_parent.right = s
        # If there is no parent of the removal node, we update the root pointer instead
        else:
            self._root = s
            s.parent = None
        # Return the lowest modified node as we will begin rebalancing here
        return low_mod

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Returns the balance factor of a node by examining the height of its children.
        """
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of a node. This is used to avoid access errors when updating
        the height of a leaf.
        """
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a leftward rotation on the root of a subtree. Returns the new root of the subtree.
        """
        c = node.right
        node.right = c.left
        if node.right:
            node.right.parent = node
        c.left = node
        node.parent = c
        self._update_height(node)
        self._update_height(c)
        return c

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a rightward rotation on the root of a subtree. Returns the new root of the subtree.
        """
        c = node.left
        node.left = c.right
        if node.left:
            node.left.parent = node
        c.right = node
        node.parent = c
        self._update_height(node)
        self._update_height(c)
        return c

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of a node. Used to keep the height attribute accurate after
        a change in the node's subtree.
        """
        left = self._get_height(node.left)
        right = self._get_height(node.right)
        if left > right:
            node.height = left + 1
        else:
            node.height = right + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Performs balancing on a node to ensure it meets the AVL property. Unbalanced nodes and their children are
        rotated as needed to bring the node's balance factor in the range [-1, 1].
        """
        # We have a left-heavy node and need to rotate rightward
        if self._balance_factor(node) < -1:
            # If it has a right-heavy left child then we must first rotate the left child leftward
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            # Save the current parent of node because the rotation will change node's parent to new root
            original_parent = node.parent
            newRoot = self._rotate_right(node)
            # Use original to connect newRoot to tree
            newRoot.parent = original_parent
            if original_parent is None:
                self._root = newRoot
            elif node.value < original_parent.value:
                original_parent.left = newRoot
            else:
                original_parent.right = newRoot
        # We have a right-heavy node and need to rotate leftward
        elif self._balance_factor(node) > 1:
            # If it has a left-heavy right child then we must first rotate the right child rightward
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            # Save the current parent of node because the rotation will change node's parent to new root
            original_parent = node.parent
            newRoot = self._rotate_left(node)
            # Use original to connect newRoot to tree
            newRoot.parent = original_parent
            if original_parent is None:
                self._root = newRoot
            elif node.value < original_parent.value:
                original_parent.left = newRoot
            else:
                original_parent.right = newRoot
        # If there is no imbalance then we just update height
        else:
            self._update_height(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
