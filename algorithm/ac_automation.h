#ifndef AC_AUTOMATION_H
#define AC_AUTOMATION_H
#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <map>
#include <vector>
#include <iostream>
#include <string>
#include <tr1/functional>
template <typename T>
// 实现T* T等版本
class ACAutomation
{
public:
    class Node;
    typedef typename std::vector<T*> pattern_t;
    typedef typename std::vector<T*>::const_iterator pattern_iterator_type;
    typedef typename std::map<size_t, Node*> next_t;
    typedef typename std::map<size_t, Node*>::iterator next_iterator_type;
    typedef class Node
    {
    public:
        Node():T_(NULL), parent_(NULL), fail_(NULL), next_(new next_t()), pattern_(NULL)
        {}
        Node(T* t, Node* parent):T_(t), parent_(parent), fail_(NULL), next_(new next_t()), pattern_(NULL)
        {}
        Node(T* t, Node* parent, Node* fail):T_(t), parent_(parent), fail_(fail), next_(new next_t()), pattern_(NULL)
        {}
        ~Node()
        {
            delete next_;
        }
        T * get()
        {
            return T_;
        }
        T * T_;
        Node *parent_;
        Node *fail_;
        next_t *next_;
        pattern_t *pattern_; // pattern_不为NULL, 代表这是一个pattern的ending point
    }node_t;

public:
    ACAutomation():root_(new node_t())
    {
        // root的fail指向自己
        root_->fail_ = root_;
        root_->parent_ = root_;
    }
    ~ACAutomation()
    {
        // @todo遍历删除
    }

    // pattern要求是有序的
    int32_t add(const pattern_t* pattern)
    {
        // 构造失败指针;
        // 构造失败指针的过程概括起来就一句话：
        //     设这个节点上的数据为T，沿着他父亲的失败指针走，直到走到一个节点，
        //     他的儿子中也有数据为T的节点(我们这里直接比较的指针)
        //     然后把当前节点的失败指针指向那个数据也为T的儿子
        //     如果一直走到了root都没找到，那就把失败指针指向root。
        //
        // 有两个规则：
        //     root的子节点的失败指针都指向root。
        //     节点(数据为T)的失败指针指向：从T节点的父节点的fail节点回溯直到找到某节点的子节点也是数据T，没有找到就指向root
        //
        if (!pattern || pattern->empty())
            return -1;
        node_t *p(root_);
        for (pattern_iterator_type k = pattern->begin(); k != pattern->end(); ++k)
        {
            const size_t t = hash(*k);
            next_iterator_type it = p->next_->find(t);
            if (it == p->next_->end())
            {
                node_t * fail(p->fail_);
                do
                {
                    it = fail->next_->find(t);
                    if ( it != fail->next_->end())
                    {
                        fail = it->second;
                        break;
                    }
                    else
                    {
                        fail = fail->fail_;
                    }
                } while (fail != root_);

                node_t * n = new node_t(*k, p, fail);
                (*(p->next_))[t] = n;
                p = n;
            }
            else
            {
                p = it->second;
            }
        }
        // 除非加入了重复的pattern
        assert(p->pattern_ == NULL);
        p->pattern_ = const_cast<pattern_t*>(pattern);
        return 0;
    }

    int32_t remove(const pattern_t* pattern)
    {
        if (!pattern || pattern->empty())
            return -1;
        node_t *p(root_);
        for (pattern_iterator_type k = pattern->begin(); k != pattern->end(); ++k)
        {
        }
        return 0;
    }

    int32_t search(std::vector<const pattern_t*> *match_patterns, const pattern_t * pattern)
    {
        // 根据AC自动机，搜索待处理的pattern, 返回命中的哪些pattern(match_patterns)
        //
        // 从root节点开始，每次根据读入的字符沿着自动机向下移动
        //      当读入的字符，在分支中不存在时，递归走失败路径
        //      如果走失败路径走到了root节点， 则跳过该字符，处理下一个字符
        //      (因为AC自动机是沿着输入文本的最长后缀移动的，
        //      所以在读取完所有输入文本后，最后递归走失败路径，直到到达根节点， 这样可以检测出所有的模式)
        //

        if (!pattern || !match_patterns || pattern->empty())
            return -1;
        node_t *p(root_);
        for (pattern_iterator_type k = pattern->begin(); k != pattern->end(); ++k)
        {
            const size_t t = hash(*k);
            do
            {
                next_iterator_type it = p->next_->find(t);
                if (it == p->next_->end())
                {
                    p = p->fail_;
                    if (p->pattern_)
                        match_patterns->push_back(p->pattern_);
                }
                else
                {
                    p = it->second;
                    node_t *tmp(p);
                    while (tmp != root_)
                    {
                        if (tmp->pattern_)
                            match_patterns->push_back(tmp->pattern_);
                        tmp = tmp->fail_;
                    }
                    break;
                }
            } while (p != root_);
        }
        return match_patterns->size();
    }
private:
    size_t hash(T* v)
    {
        return static_cast<size_t>(*v);
    }
private:
    node_t *root_;
    std::tr1::hash<T*> hash_;
};
#endif // AC_AUTOMATION_H
