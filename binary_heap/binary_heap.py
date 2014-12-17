#encoding=utf8
import os
import sys
import pdb
import random

class BinaryHeap:
    '''
    二叉堆就是我们通常所指的 "堆"
    结构性质：
        堆是一颗完全二叉树，所以堆可以方便的用数组的方式来实现
    堆序性质：
        任意节点的值都应该小于它的所有后裔
    '''
    MAX = sys.maxint
    MIN = -sys.maxint
    def __init__(self, max_elements):
        assert max_elements > 0
        self.capacity = max_elements
        self._size = 0
        self.elements = [0] * (max_elements + 2) #下标0用来放置方便代码实现的一个极小值, MIN
        self.elements[0] = self.MIN #min value
        #程序中树的下标都是从1开始用的(下标1处放置了所有插入的数据的最小值),
        #另外为方便程序实现,下标0处放置一个极小值MIN

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
        last_element = self.elements[self.size()]
        self._size -= 1 #last element空间已经不复存在
        i = 1
        #从root节点（位置1）处开始执行下滤操作
        while i * 2 <= self.size():
            #find smaller child
            child = i * 2
            if child < self.size() and self.elements[child + 1] < self.elements[child]:
                #左儿子比右儿子大
                child += 1 #指向较小的那个儿子
            #只有一个左儿子, 直接选择child
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

    def delete_min_v2(self):
        '''
        另外一种巧妙的实现，始终保证你的算法把每一个节点都看成有两个儿子，
        为了实施这种解法，当堆的大小为偶数时(存在一个节点只有一个儿子)，
        在每个下滤开始时，
        可将其值大于堆中任何元素的标记放到堆的终端后面的位置上。
        你必须在深思熟虑以后再这么做，而且必须要判断你是否确实需要使用这种技巧。虽然这不再需要测试右儿子的存在性，
        但是你还是需要测试何时到达底层，因为对每一片树叶 算法将需要一个标记。
        '''
        assert not self.empty()
        min_element = self.elements[1]
        last_element = self.elements[self.size()]
        sign = (self.size() % 2 == 0)
        if sign:
            #尾巴上加了一个MAX
            self._size += 1
            self.elements[self.size()] = self.MAX

        i = 1
        #从root节点（位置1）处开始执行下滤操作
        while i * 2 <= self.size():
            #find smaller child
            child = i * 2
            #左儿子比右儿子大
            if self.elements[child + 1] < self.elements[child]:
                child += 1 #指向较小的那个儿子
            smaller = self.elements[child]
            if last_element > smaller:
                self.elements[i] = smaller
            else:
                self.elements[i] = last_element
                break
            i = child
        #处理只有root节点的情况
        self.elements[i] = last_element
        if sign:
            #把MAX干掉
            self._size -= 2
        else:
            self._size -= 1
        return min_element

    def pop(self):
        return self.delete_min_v2()

def test2():
    priority_queue = BinaryHeap(4)
    priority_queue._size = 4
    priority_queue.elements = [priority_queue.MIN, 3804, 8220, 5613, 8801, 0]
    print priority_queue.pop()
    print priority_queue.elements
    print priority_queue.pop()
    print priority_queue.pop()
    print priority_queue.pop()

def test1():
    threshold = 100000
    array1 = []
    priority_queue = BinaryHeap(threshold)
    for i in range(threshold):
        k = random.randint(0, 100000)
        array1.append(k)
        priority_queue.insert(k)

    #print priority_queue.elements
    array1 = sorted(array1)
    array2 = []
    for i in range(threshold):
        v1 = array1[i]
        v2 = priority_queue.pop()
        #if v1 != v2:
        #    print priority_queue.elements
        array2.append(v2)
    #print array1
    #print array2
    for i in range(threshold):
        v1 = array1[i]
        v2 = array2[i]
        assert v1 == v2, '%s vs %s' % (v1, v2)

if __name__ == '__main__':
    test1()
