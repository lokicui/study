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
        self.size = 0
        self.elements = [0] * (max_elements + 1)
        self.elements[0] = -sys.maxint #min value
        #程序中树的下标都是从1开始用的,下标0处放置极小值

    def full(self):
        return self.size >= self.capacity

    def empty(self):
        return self.size <= 0

    def insert(self, x):
        '''
        插入操作的核心就是创建一个空穴,然后执行上虑操作(父节点的值一定要小于两个儿子节点的值)
        '''
        if self.full():
            return False

        self.size += 1
        #i指向新创建的一个空穴
        i = self.size
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
        '''

