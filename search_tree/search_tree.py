#encoding=utf8
import os
import sys
import pdb
import random

class TreeNode(object):
    '''
    tree node
    '''
    def __init__(self, element):
        self.element = element #存数据
        self.left = None #左子树
        self.right = None

    def __str__(self):
        return '%s' % self.element

class SearchTree(object):
    '''
    二叉搜索树, 每个节点的类型都是TreeNode
    '''
    def __init__(self):
        self.root = None

    def find(self, needle):
        root = self.root
        while root:
            if needle < root.element:
                root = root.left
            elif needle > root.element:
                root = root.right
            else:
                return root
        return None

    def find_min(self, root=None):
        root = root or self.root
        while root and root.left:
            root = root.left
        return root

    def find_max(self, root=None):
        root = root or self.root
        while root.right:
            root = root.right
        return root

    def insert(self, element):
        root = self.root
        if not root:
            self.root = TreeNode(element)
            return True
        while root:
            if element < root.element:
                if root.left:
                    root = root.left
                else:
                    root.left = TreeNode(element)
                    return True
            elif element > root.element:
                if root.right:
                    root = root.right
                else:
                    root.right = TreeNode(element)
                    return True
            else:
                #already exists
                return False

    def delete(self, element, node=None):
        '''
        delete的非递归版本不太好写,就用递归版本了
        '''
        node = node or self.root
        if element < node.element:
            node.left = self.delete(element, node.left)
        elif element > node.element:
            node.right = self.delete(element, node.right)
        else: #found element to be deleted
            #have two childrens
            if node.left and node.right:
                #find min node of right children
                min_node = self.find_min(node.right)
                node.element = min_node.element
                node.right = self.delete(node.element, node.right)
            #have left child
            elif node.left:
                node = node.left
            #have right child
            elif node.right:
                node = node.right
            #del leaves
            else:
                #need del root node
                if node == self.root:
                    self.root = None
                node = None
        return node

if __name__ == '__main__':
    tree = SearchTree()
    for i in range(100):
        j = random.randint(1, 1000)
        tree.insert(j)
    for i in [19,11,25,33,17]:
        print i,tree.insert(i),tree.find(i), tree.delete(i), tree.find(i)
