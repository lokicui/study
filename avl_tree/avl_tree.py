#encoding=utf8
import os
import sys
import pdb

class AvlNode(object):
    '''
    AVL Node
    '''
    def __init__(self, element):
        self.element = element
        self.left = None
        self.right = None
        self.height = 0

class AvlTree(object):
    '''
    AVL Tree
    '''
    def __init__(self):
        self.root = None

    def get_height(self, n=None):
        if not n:
            return -1
        return n.height

    def single_rotate_with_left(self, k2):
        '''
        LL单旋转

              k2
             / \
            k1  Z
           / \
          X   Y

          ==>

            k1
           / \
          X  K2
            /  \
           Y    Z
        '''
        k1 = k2.left
        k2.left = k1.right
        k1.right = k2
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        return k1

    def single_rotate_with_right(self, k2):
        '''
        RR单旋转

            k2
           /  \
          X   k1
             /  \
            Y    Z

         ===>

            k1
           /  \
          k2   Z
         /  \
        X    Y
        '''
        k1 = k2.right
        k2.right = k1.left
        k1.left = k2
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        return k1

    def double_rotate_with_left(self, k3):
        '''
        LR双旋转
        若按LL单旋转的思路把K1往上提一层,发现仍然不能满足要求
        说白了k2是介于k1和k3中间的
        选择k1作为root, k2会挂在k3的左子树下,导致k3的高度差为1,然后k1的高度差就不能满足AVL的要求了

              k3
             /  \
            k1   D
           /  \
          A   k2
              / \
             B   C

          =========>

             k2
           /    \
          k1     k3
         / \     / \
        A   B   C   D
        '''
        k1 = k3.left
        k2 = k1.right
        k1.right = k2.left
        k3.left = k2.right
        k2.left = k1
        k2.right = k3
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        k3.height = max(self.get_height(k3.left), self.get_height(k3.right)) + 1
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1

        #########另外一种实现###################
        ## Rotate between k1 and k2
        #k3.left = self.single_rotate_with_right(k3.left)
        ## Rotate between k3 and k2
        #return self.single_rotate_with_left(k3)
        #########################################
        return k2

    def double_rotate_with_right(self, k3):
        '''
        RL双旋转

              k3
             /  \
            A   k1
               /  \
              k2   D
              / \
             B   C

          ==========>

             k2
           /    \
          k3     k1
         / \     / \
        A   B   C   D

        '''
        k1 = k3.right
        k2 = k1.left
        k3.right = k2.left
        k1.left = k2.right
        k2.left = k3
        k2.right = k1
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        k3.height = max(self.get_height(k3.left), self.get_height(k3.right)) + 1
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1

        #########另外一种实现###################
        ## Rotate between k1 and k2
        #k3.left = self.single_rotate_with_left(k3.right)
        ## Rotate between k3 and k2
        #return self.single_rotate_with_right(k3)
        #########################################
        return k2

    def __insert(self, e, n):
        if not n:
            n = AvlNode(e)
        elif e < n.element:
            n.left = self.__insert(e, n.left)
            if self.get_height(n.left) - self.get_height(n.right) == 2:
                if e < n.left.element:
                    #LL单旋转
                    n = self.single_rotate_with_left(n)
                else:
                    #LR双双旋转
                    n = self.double_rotate_with_left(n)
        elif e > n.element:
            n.right = self.__insert(e, n.right)
            if self.get_height(n.right) - self.get_height(n.left) == 2:
                if e > n.right.element:
                    #RR单旋转
                    n = self.single_rotate_with_right(n)
                else:
                    #RL双旋转
                    n = self.double_rotate_with_right(n)
        else:
            pass
            #do nothing , e already exists
        n.height = max(self.get_height(n.left), self.get_height(n.right)) + 1
        return n

    def insert(self, e):
        if not self.root:
            self.root = AvlNode(e)
        else:
            self.root = self.__insert(e, self.root)
        return self.root

    def __DFS(self, T):
        '''
        深度优先遍历
        '''
        if T:
            print T.element
            self.__DFS(T.left)
            print '/'
            self.__DFS(T.right)

    def __BFS(self, nodes):
        '''
        广度优先遍历
        '''
        if not nodes:
            return
        print [n.element for n in nodes if n]
        l = []
        for n in nodes:
            if n.left:
                l.append(n.left)
            if n.right:
                l.append(n.right)
        self.__BFS(l)

    def DFS(self):
        return self.__DFS(self.root)

    def BFS(self):
        return self.__BFS([self.root])


if __name__ == '__main__':
    tree = AvlTree()
    for i in range(10,20):
        tree.insert(i)
    tree.BFS()
    tree.DFS()
