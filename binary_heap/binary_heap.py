#encoding=utf8
import os
import sys
import pdb

class BinaryHeap:
    '''
    二叉堆就是我们通常所指的 "堆"
    '''
    def __init__(self, max_elements):
        assert max_elements > 0
        self.capacity = max_elements
        self._size = 0
        self.elements = [0] * (max_elements + 1) #下标0用来放置方便代码实现的一个极小值, -maxint
        self.elements[0] = -sys.maxint #min value
        #程序中树的下标都是从1开始用的(下标1处放置了所有插入的数据的最小值),
        #另外为方便程序实现,下标0处放置一个极小值-maxint

    def full(self):
        return self._size >= self.capacity

    def empty(self):
        return self._size <= 0

    def size(self):
        return self._size

    def insert(self, x):
        '''
        插入操作的核心就是在self._size+1处创建一个空穴,然后执行上虑操作(父节点的值一定要小于两个儿子节点的值)
        '''
        if self.full():
            return False

        self._size += 1
        #i指向新创建的一个空穴
        i = self._size
        #判断i的父亲的值是否大于i的值(x) 由于位置0放了个极小值,所以这个循环到0位置一定会停止
        #若父节点的值大于儿子节点的值,儿子节点(空穴)上滤，替代父亲, 父亲往下放,替代儿子
        while self.elements[i/2] > x:
            self.elements[i] = self.elements[i/2]
            i /= 2
        self.elements[i] = x
        return True

    def delete_min(self):
        '''
        pop min 操作
        核心思想就是删除位置1处的元素(产生一个空穴)，用self._size处的元素执行下滤操作去补这个空穴
        注意考虑last_element的父亲点有一个儿子和两个儿子的情况
        '''
        assert not self.empty()
        min_element = self.elements[1]
        last_element = self.elements[self._size]
        self._size -= 1 #last element空间已经不复存在
        i = 1
        #从root节点（位置1）处开始执行下滤操作
        while i * 2 <= self._size:
            #find smaller child
            child = i * 2
            if child < self._size:
                #左儿子比右儿子大
                if self.elements[child] > self.elements[child + 1]:
                    child += 1 #指向较小的那个儿子
                smaller = min(self.elements[child], self.elements[child+1])
            else:#只有一个左儿子
                smaller = self.elements[child]
            if last_element > smaller:
                self.elements[i] = smaller
            else:
                self.elements[i] = last_element
                break
            ###这里容易出错#####
            #i *= 2  这相当于直接下滤到左儿子上了，不对，应该下滤到较小的那个儿子 i = child
            ###################
            i = child
        #处理只有root节点的情况
        self.elements[i] = last_element
        return min_element

    def pop(self):
        return self.delete_min()

if __name__ == '__main__':
    priority_queue = BinaryHeap(100)
    for i in range(1000, 990, -1):
        priority_queue.insert(i)
    for i in range(priority_queue.size()):
        print priority_queue.pop()
