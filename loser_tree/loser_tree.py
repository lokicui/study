#encoding=utf8
import os
import sys
import pdb

class LoserTree(object):
    '''
    败者树,数组方式实现
    '''

    def __init__(self, ways):
        #败者树至少需要两路数据,每一路数据都是升序排列的,并且每一路数据个数一样
        assert len(ways) > 1
        self.leaves = ways
        self.tree = [-1] * len(ways)
        #每一路数据已经取到哪了
        self.idx = [0] * len(ways)
        self.__init_tree()

    def __init_tree(self):
        for i in range(len(self.leaves) - 1, -1, -1):
            self.__ajust(i)

    def __ajust(self, i):
        #parent 是败者树上的节点,败者树的所有节点的值都是每一次比较中败者的索引index
        parent = (i + len(self.leaves)) / 2
        while parent > 0:
            if i == -1:
                #i==-1证明i是胜者,败者不用变
                pass
            elif self.tree[parent] == -1 or \
                self.leaves[i][self.idx[i]] > self.leaves[self.tree[parent]][self.idx[self.tree[parent]]]:
                    # self.tree[parent] == -1 初始化阶段, i永远都是败者(大)
                    #本局比赛, i 败了, self.tree[parent]是胜者，胜者要参与下一局比赛,败者直接记录到败者树节点中
                winner = self.tree[parent]
                self.tree[parent] = i
                #让i 指向胜者,参与下次比较
                i = winner
            parent >>= 1
        #tree[0] 指向的是最终的胜者
        self.tree[0] = i

    def next(self):
        min_i = self.tree[0]
        min_v = self.leaves[min_i][self.idx[min_i]]
        self.idx[min_i] += 1
        self.__ajust(min_i)
        print min_i, min_v
        return min_v

if __name__ == '__main__':
    ways = [[1,5,9,13], [2,6,10,14], [3,7,11,15], [4,8,12,16]]
    tree = LoserTree(ways)
    for i in range(10):
        tree.next()
