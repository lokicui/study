// Copyright (c) 2015, lokicui@gmail.com. All rights reserved.
#ifndef DNF_EXPR_H
#define DNF_EXPR_H
#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <map>
#include <list>
#include <vector>
#include <iostream>
#include <string>
#include <tr1/functional>

template <typename T>
class TypeTraits
{
private:
    template<class U> struct PointerTraits
    {
        enum { result = false };
        typedef U* PointerType;
    };

    template<class U> struct PointerTraits<U*>
    {
        enum { result = true };
        typedef U* PointerType;
    };
public:
    enum { isPointer = PointerTraits<T>::result };
    typedef typename PointerTraits<T>::PointerType PointerType;
};

// 析取范式
template <typename U>
class DNFExpr
{
public:
    typedef typename TypeTraits<U>::PointerTraits T;
    typedef typename std::vector<T> pattern_t;
    typedef typename std::vector<T>::const_iterator pattern_iterator_type;
    typedef class Node
    {
    public:
        Node():data_(NULL), parent_(NULL), fail_(NULL), succ_(NULL), pattern_(NULL)
        {}
        Node(T t, Node* parent):data_(t), parent_(parent), fail_(NULL), succ_(NULL), pattern_(NULL)
        {}
        Node(T t, Node* parent, Node* succ, Node* fail):data_(t), parent_(parent), fail_(fail), succ_(succ), pattern_(NULL)
        {}
        ~Node()
        {
        }
        T get()
        {
            return data_;
        }
        T data_;
        Node *parent_;
        Node *fail_;
        Node *succ_;
        pattern_t *pattern_; // pattern_不为NULL, 代表这是一个pattern的ending point
    }node_t;

public:
    DNFExpr():root_(new node_t())
    {
        root_->parent_ = root_;
        root_->succ_ = root_;
    }

    ~DNFExpr()
    {
    }

    int32_t add(const pattern_t* pattern)
    {
        if (!pattern || pattern->empty())
            return -1;
        node_t *p(root_->succ_);
        size_t i(0);
        for (i = 0; i < pattern->size(); ++i)
        {
            const size_t t = hash(pattern->at(i));
            while (p != root_)
            {
                if (hash(p->get()) == t)
                {
                    p = p->succ_;
                }
                else
                {
                    // 本是同根生
                    if (p->fail_->parent_ == p->parent_)
                        p = p->fail_;
                    else
                        break;
                }
            }
        }
        p = p->parent_;
        node_t *next = p->succ_;
        for(; i < pattern->size(); ++i)
        {
            node_t *node = new node_t(pattern->at[i], p, next, next);
            p->succ_ = node;
            p = node;
        }
        // 除非加入了重复的pattern
        assert(p->pattern_ == NULL);
        p->pattern_ = const_cast<pattern_t*>(pattern);
        return 0;
    }

    int32_t remove(const pattern_t* pattern)
    {
        // @todo 还没完工
        // 确认存在这个pattern
        // 所有fail_指向这个node的都要改指向node->fail_
        if (!pattern || pattern->empty())
            return -1;
        return 0;
    }

    int32_t search(std::vector<const pattern_t*> *match_patterns, const pattern_t * pattern)
    {
        if (!pattern || !match_patterns || pattern->empty())
            return -1;
        return match_patterns->size();
    }
private:
    size_t hash(T v)
    {
        return hash_(v);
    }

private:
    node_t *root_;
    std::tr1::hash<T> hash_;
};
#endif // DNF_EXPR_H
