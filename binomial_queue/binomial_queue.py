#encoding=utf8
import os
import sys
import pdb
import random

class BinNode:
    '''
    二项树节点
    '''
    def __init__(self, e):
        self.element = e
        self.left_child = None
        self.next_sibling = None

class BinQueue:
    '''
    二项队列
    一些二项树组成的森林
    二项队列的NB之处在于：
        插入操作O(N), 最坏O(logN)
        DeleteMin   O(logN)
        Merge       O(logN)
    '''
    MAX = sys.maxint
    MIN = -sys.maxint
    def __init__(self, max_trees=1024):
        self._trees = [None] * max_trees #bin trees
        self._size = 0

    def empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def insert(self, x):
        node = BinNode(x)
        H = BinQueue()
        H._size = 1
        H._trees[0] = node
        self.__merge(self, H)
        return True

    def __combine_trees(self, T1, T2):
        '''
        值大的树作为值小的树的儿子
        '''
        ##这种实现对出现两个相同值的情况就会死循环
        #if (T1.element < T2.element):
        #    T1->next_sibling = T2
        #return self.__combine_trees(T2, T1)

        #链表插入
        if (T2.element > T1.element):
            return self.__combine_trees(T2, T1)
        T2.next_sibling = T1.left_child
        T1.left_child = T2
        return T1

    def __merge(self, H1, H2):
        '''
        其实现跟二进制的加法器差不多
        '''
        H1._size += H2._size
        carry = None #进位
        i = 0
        j = 1
        while j <= H1.size():
            T1 = H1._trees[i]
            T2 = H2._trees[i]
            k = (not not carry) << 2 | (not not T2) << 1 | (not not T1)
            if k in (0, 1): #0 means no trees, 1 means only H1
                pass
            elif k == 2: #Only H2
                H1._trees[i] = T2
                H2._trees[i] = None
            elif k == 3: # H1 and H2
                carry = self.__combine_trees(T1, T2)
                H1._trees[i] = H2._trees[i] = None
            elif k == 4: #Only carry
                H1._trees[i] = carry
                carry = None
            elif k == 5:# H1 and carry
                carry = self.__combine_trees(T1, carry)
                H1._trees[i] = None
            elif k == 6: #H2 and carry
                carry = self.__combine_trees(T2, carry)
                H2._trees[i] = None
            elif k == 7: #H1 and H2 and carry
                H1._trees[i] = carry
                carry = self.__combine_trees(T1, T2)
                H2._trees[i] = None
            i += 1
            j *= 2
        return H1

    def delete_min(self):
        '''
        二项队列H中关键字最小的二项树为Bk
        H' = H - Bk
        H'' = Bk 弹出关键字最小的节点
        H' + H''即为所求
        '''
        assert not self.empty()
        min_item = self.MAX
        min_tree_idx = None
        for i in range(self.size()):
            if self._trees[i] and self._trees[i].element < min_item:
                min_item = self._trees[i].element
                min_tree_idx = i
        deleted_tree = self._trees[min_tree_idx].left_child  #min_tree_idx 删除关键字最小的节点,相当于H''
        #删除了root，还得把tree拆开成多颗二项树,
        deleted_queue = BinQueue()
        deleted_queue._size = 2 ** min_tree_idx  - 1 # min_tree的节点数量是2^min_tree_idx,然后删除了一个元素
        for i in range(min_tree_idx - 1, -1, -1): #(min_tree_idx, 0]
            deleted_queue._trees[i] = deleted_tree
            deleted_tree = deleted_tree.next_sibling
            deleted_queue._trees[i].next_sibling = None
        self._trees[min_tree_idx] = None        #H'
        self._size -= deleted_queue.size() + 1
        self.__merge(self, deleted_queue)    #H' + H''
        return min_item

if __name__ == '__main__':
    queue = BinQueue()
    threshold = 10
    for i in range(threshold):
        v = random.randint(0, 1000)
        queue.insert(v)

    for i in range(threshold):
        print queue.delete_min()

