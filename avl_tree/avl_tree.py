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
    性质：
        任意节点的左子树的高度和右子树的高度差都不能大于1
    '''
    def __init__(self):
        self.root = None

    def get_height(self, n=None):
        if not n:
            return -1
        return n.height

    def single_rotate_with_left(self, k2):
        '''
        N是新插入的元素,到底是作为左孩子还是右孩子根据N是否大于X来确定

        LL单旋转

              k2
             / \
            k1  Z
           / \
          X   Y
          |
          N
          ==>

             k1
           /   \
          X     K2
          |    /  \
          N   Y    Z
        '''
        k1 = k2.left
        k2.left = k1.right
        k1.right = k2
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        return k1

    def single_rotate_with_right(self, k2):
        '''
        N是新插入的元素,到底是作为左孩子还是右孩子根据N是否大于Z来确定

        RR单旋转

            k2
           /  \
          X   k1
             /  \
            Y    Z
                 |
                 N
         ===>

             k1
           /    \
          k2     Z
         /  \    |
        X    Y   N
        '''
        k1 = k2.right
        k2.right = k1.left
        k1.left = k2
        k2.height = max(self.get_height(k2.left), self.get_height(k2.right)) + 1
        k1.height = max(self.get_height(k1.left), self.get_height(k1.right)) + 1
        return k1

    def double_rotate_with_left(self, k3):
        '''
        B or C是新插入的元素, B代表新插入的数据小于k2

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
        B or C是新插入的元素, B代表新插入的数据小于k2

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

    def find_min(self, n):
        n = n or self.root
        while n and n.left:
            n = n.left
        return n

    def find_max(self, n):
        n = n or self.root
        while n and n.right:
            n = n.right
        return n

    def __delete(self, e, n):
        '''
        '''
        if not n:
            return None
        elif e < n.element:
            n.left = self.__delete(e, n.left)
            if self.get_height(n.right) - self.get_height(n.left) == 2:
                if self.get_height(n.right.left) > self.get_height(n.right.right):
                    #RL双旋转
                    n = self.double_rotate_with_right(n)
                else:
                    #RR单旋转
                    n = self.single_rotate_with_right(n)
        elif e > n.element:
            n.right = self.__delete(e, n.right)
            if self.get_height(n.left) - self.get_height(n.right) == 2:
                if self.get_height(n.left.right) > self.get_height(n.right.left):
                    #LR双旋转
                    n = self.double_rotate_with_right(n)
                else:
                    #LL单旋转
                    n = self.single_rotate_with_left(n)
        else:
            #find it
            #叶子节点,直接咔嚓掉
            if not n.left and not n.right:
                if n == self.root:
                    self.root = None
                n = None
            elif n.left:
                n = n.right
            elif n.right:
                n = n.left
            else:
                #最复杂的情况，两个孩子都健在
                #两种选择：
                #   1、if右子树高, then选择右子树中最小的节点Min来顶替当前节点，并递归删除Min节点
                #   2、if左子树高, then选择左子树中最大的节点Max来顶替当前节点，并递归删除Max节点
                if self.get_height(n.right) > self.get_height(n.left):
                    min_node = self.find_min(n.right)
                    n.element = min_node.element
                    n.right = self.__delete(n.element, n.right)
                else:
                    max_node = self.find_max(n.left)
                    n.element = max_node.element
                    n.left = self.__delete(n.element, n.left)
        if n:
            n.height = max(self.get_height(n.left), self.get_height(n.right)) + 1
        return n

    def delete(self, e):
        return self.__delete(e, self.root)

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
            self.__DFS(T.left)
            print T.element
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
    for i in range(10,30):
        tree.insert(i)
    tree.DFS()
    #tree.delete(10)
    print '---------------------'
    #tree.DFS()
    tree.BFS()
    #tree.DFS()
