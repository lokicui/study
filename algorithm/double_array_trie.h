#ifndef DOUBLE_ARRAY_TRIE_H
#define DOUBLE_ARRAY_TRIE_H
#pragma once
#include <cstdio>
#include <cstring>
#include <vector>

class DATrie {
public:
    DATrie(void);
    ~DATrie(void);

    // build double array trie with strings and their property
    // str_size -- string num
    // str -- strings
    // len -- strings' length
    // val -- strings' property
    // return true on success otherwise false
    bool Build(size_t str_size, const char* const* str, const size_t* len = 0,
               const int* val = 0);

    // save double array trie into file, return true on success otherwise false
    bool Save(const char* file, const char* mode = "wb", size_t offset = 0);

    // load double array trie from file, return true on success otherwise false
    bool Open(const char* file, const char* mode = "rb", size_t offset = 0,
            size_t _size = 0);

    // free allocated buffer
    void Clear(void);

    int LongestMatch(const char *key, size_t &match_len, size_t key_len = 0) const;

    // judge whether key exists in dictionary
    // return key's property value on exist otherwise return -1
    int ExactMatch(const char* key, size_t key_len = 0) const;

    // search all words sharing common prefix and get their properties
    // key -- string to be searched
    // result -- buffer used for storing string property
    // result_len -- buffer length
    // key_len -- string length
    size_t CommonPrefixSearch(const char* key, int* result, size_t result_len,
                            size_t key_len = 0) const;

    private:
    typedef struct Node_ {
        unsigned code; // code number plus one
        size_t depth; // current code's depth in element plus 1
        size_t left;  // current code's start position in str_ array
        size_t right; // current code's end position in str_ array
    } Node;

    // duoble array trie unit
    typedef struct Unit_ {
        // store a reasonable value for all edages jumped from current node
        int base_;
        // indicate current node jumped from which base element
        unsigned check_;
    } Unit;

    // base and check array
    Unit* array_;
    // used for indicating whether an node have been used
    size_t* used_;
    // current max used index in array
    size_t size_;
    // buffer 'array' and 'used' 's size
    size_t alloc_size_;
    // key buffer
    const char* const* str_;
    // key elements number
    size_t str_size_;
    // each key's length
    const size_t* len_;
    // each key's property
    const int* val_;
    // current build progress
    unsigned progress_;
    // used for set next begin check position
    size_t next_check_pos_;
    // indicate whether array buffer have been released
    int no_delete_;

    // compare two elements and return the larger one
    template <class T>
    inline T _Max(T x, T y) {
        return (x > y) ? x : y;
    }

    // reallocate array's storage size
    template <class T>
    inline T* _Resize(T* sarray, size_t old_size, size_t new_size, T  init_val);

    // resize base and check array buffer and used array
    // buffer's size return new_size on success othersize -1
    size_t Resize(const size_t new_size);

    // get parent node's all children nodes in str_ array and store
    // them into vector siblings return children nodes number
    size_t Fetch(const Node& parent, std::vector<Node>* siblings);

    // recursivly insert every node in siblings vector and their
    // children into double array trie and insert their property
    // if current insert nodes root's children nodes, then we always
    // have begin = 1, becase at first 'next_check_pos_ = 0' and
    // begin = pos-siblings[0].code = (siblings[0].code+1)-siblings[0].code
    size_t Insert(const std::vector<Node>& siblings);
};

#endif // DOUBLE_ARRAY_TRIE_H
