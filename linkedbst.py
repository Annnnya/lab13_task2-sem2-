"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import log
from time import time
from random import sample
from sys import setrecursionlimit
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue



class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            ss1 = ""
            if node != None:
                ss1 += recurse(node.right, level + 1)
                ss1 += "| " * level
                ss1 += str(node.data) + "\n"
                ss1 += recurse(node.left, level + 1)
            return ss1

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def is_leaf(self, node: BSTNode):
        """is leaf?"""
        if node.left is None and node.right is None:
            return True
        else:
            return False

    def yield_children(self, node: BSTNode):
        """yield children"""
        if node.left != None:
            yield node.left
        if node.right != None:
            yield node.right

    def num_nodes(self):
        """number of nodes"""
        self.num = 0
        def recursion(top):
            if top != None:
                self.num += 1
                for child in self.yield_children(top):
                    recursion(child)
        recursion(self._root)
        return self.num

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmalxineftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentode = top.left
            while not currentode.right == None:
                parent = currentode
                currentode = currentode.right
            top.data = currentode.data
            if parent == top:
                top.left = currentode.left
            else:
                parent.right = currentode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itememoved = None
        preoot = BSTNode(None)
        preoot.left = self._root
        parent = preoot
        direction = 'L'
        currentode = self._root
        while not currentode == None:
            if currentode.data == item:
                itememoved = currentode.data
                break
            parent = currentode
            if currentode.data > item:
                direction = 'L'
                currentode = currentode.left
            else:
                direction = 'R'
                currentode = currentode.right

        # Return None if the item is absent
        if itememoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentode.left == None \
                and not currentode.right == None:
            liftmalxineftsubtreetotop(currentode)
        else:

            # Case 2: The node has no left child
            if currentode.left == None:
                newhild = currentode.right

                # Case 3: The node has no right child
            else:
                newhild = currentode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newhild
            else:
                parent.right = newhild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preoot.left
        return itememoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top = self._root):
            '''
            Helper function
            :param top:
            :return:
            '''
            if self.is_leaf(top):
                return 0
            else:
                return 1 + max(height1(child) for child in self.yield_children(top))

        return height1()

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height()+1<2*log(self.num_nodes()+1, 2) - 1:
            # print(self.height())
            # print(2*log(self.num_nodes()+1, 2) - 1)
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        for elem in self.inorder():
            if elem >= low:
                res.append(elem)
            if elem == high:
                break
        return res

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        lyst = [i for i in self.inorder()]
        self.clear()
        def recur_add_list(part):
            if len(part) != 0:
                self.add(part[len(part)//2])
                recur_add_list(part[:len(part)//2])
                recur_add_list(part[len(part)//2+1:])
        recur_add_list(lyst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for elem in self.inorder():
            if elem > item:
                return elem
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        pastel=None
        for elem in self.inorder():
            if elem < item:
                pastel = elem
            elif elem==item:
                return pastel

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        print('\n>>> Comparison of time which takes finding 10000 elements\
in different data structures <<<\n')
        print("Reading file...")
        self.file_to_list(path)
        words10000 = sample(self.word_list, 10000)
        # print(words10000)
        # print(len(self.word_list))
        print('Calculating time for list...')
        list_time = self.list_time(words10000)
        print(f"In list 10000 elements are found in {round(list_time, 3)} seconds")
        print('Calculating time for binary tree in alphabetic order...')
        alphbin_time = self.bin_search_alph(words10000)
        print(f"In alphabetic tree 10000 elements are found in {round(alphbin_time, 3)} seconds")
        print('Calculating time for binary tree in random order...')
        notalphbin_time = self.bin_search_not_alph(words10000)
        print(f"In non-alphabetic tree 10000 elements are found in {round(notalphbin_time, 3)} seconds")
        print('Calculating time for balanced binary tree...')
        bal_time = self.bin_search_balanced(words10000)
        print(f"In balanced tree 10000 elements are found in {round(bal_time, 3)} seconds")

    def file_to_list(self, path):
        """read file"""
        res=list()
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                res.append(line.strip())
        self.word_list = res
        self.word_set = set(res)

    def list_time(self, words10000):
        """
        час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику
        """
        res = set()
        time1 = time()
        for num, word in enumerate(words10000):
            print('\r', str(num)+'/10000', end = '')
            res.add(self.word_list.index(word))
        print('\r', end = '')
        time2 = time()
        return time2-time1

    def no_recur_find(self, elem):
        """
        idk why you needed to make a task which crashes nomal search but here we are
        """
        cur = self._root
        while cur is not None:
            if cur.data == elem:
                return cur.data
            cur = cur.right

    def bin_search_alph(self, words10000):
        """
        час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку.
        Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника,
        який впорядкований за абеткою.
        """
        res = set()
        self.clear()
        num = 0
        for wd in self.word_list:
            if self._root is None:
                self._root = BSTNode(wd)
                cur = self._root
            else:
                cur.right = BSTNode(wd)
                cur = cur.right
        time1 = time()
        for word in words10000:
            res.add(self.no_recur_find(word))
            num+=1
            print('\r', str(num)+'/10000', end = '')
        print('\r', end = '')
        time2 = time()
        return time2-time1

    def bin_search_not_alph(self, words10000):
        """
        час пошуку 10000 випадкових слів у словнику, який представлений у вигляді бінарного дерева пошуку.
        Бінарне дерево пошуку будується на основі послідовного додавання в дерево слів зі словника який
        не впорядкований за абеткою (слова у дерево додаються випадковим чином).
        """
        res = set()
        self.clear()
        num=0
        for wd in self.word_set:
            self.add(wd)
        time1 = time()
        for word in words10000:
            res.add(self.find(word))
            num+=1
            print('\r', str(num)+'/10000', end = '')
        print('\r', end = '')
        time2 = time()
        return time2-time1

    def bin_search_balanced(self, words10000):
        """
        час пошуку 10000 випадкових слів у словнику,
        який представлений у вигляді бінарного дерева пошуку після його балансування.
        """
        num=0
        res = set()
        self.rebalance()
        time1 = time()
        for word in words10000:
            res.add(self.find(word))
            num+=1
            print('\r', str(num)+'/10000', end = '')
        print('\r', end = '')
        time2 = time()
        return time2-time1


if __name__=="__main__":
    setrecursionlimit(250000)
    tre= LinkedBST()
    # tre.add('an')
    # tre.add('ab')
    # tre.add('bc')
    # tre.add('d')
    # tre.add('l')
    # tre.add('f')
    # tre.add('ac')
    # tre.add('da')
    tre.demo_bst('./words.txt')
    # print(tre)
    # print(tre.rangeFind('ac','f'))
    # print(tre.predecessor('l'))
    # print(tre.is_balanced())
    # tre.rebalance()
    # print(tre)
    # print(tre.is_balanced())
    # print(tre.height())
    # print(tre.is_balanced())
    # print(tre.rangeFind('an', 'l'))
