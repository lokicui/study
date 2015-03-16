#include "double_array_trie.h"

template <class T>
T* DATrie::_Resize(T* sarray, size_t old_size, size_t new_size, T   init_val)
{
    T *tmp;
    if (NULL == (tmp = new T[new_size])) return NULL;

    size_t i;
    for (i = 0; i < old_size; ++i) tmp[i] = sarray[i];
    for (i = old_size; i < new_size; ++i) tmp[i] = init_val;
    delete [] sarray;
    return tmp;
}

size_t DATrie::Resize(const size_t new_size)
{
    Unit tmp;
    tmp.base_ = 0;
    tmp.check_ = 0;

    Unit *old_array = array_;
    if (NULL == (array_ = _Resize(array_, alloc_size_, new_size, tmp)))
    {
        array_ = old_array;
        fprintf(stderr, "%s\n", "Not enough memory to allocate!");
        throw -1;
    }
    size_t *old_used = used_;
    if (NULL == (used_ = _Resize(used_, alloc_size_, new_size, (size_t)0)))
    {
        used_ = old_used;
        fprintf(stderr, "%s\n", "Not enough memory to allocate!");
        throw -2;
    }
    alloc_size_ = new_size;
    return new_size;
}

size_t DATrie::Fetch(const Node& parent, std::vector<Node>* siblings)
{
    // previous child's code number plus one
    unsigned prev = 0;
    for (size_t i = parent.left; i < parent.right; ++i)
    {
        // str_[i]'s length small then parent.depth, this means str_[i] doesn't
        // have parent's child so go to next string
        if ((len_ ? len_[i] : strlen(str_[i])) < parent.depth) continue;

        const unsigned char* tmp = (unsigned char*)(str_[i]);

        // current child's code number plus one
        unsigned cur = 0;
        if ((len_ ? len_[i] : strlen(str_[i])) != parent.depth)
        {
            cur = (unsigned)tmp[parent.depth] + 1;
        }

        // order isn't right throw an error code
        if (prev > cur)
        {
            fprintf(stderr, "%s\n", "element's order is not right!");
            throw -3;
        }

        // current node not equal to previous or children vector
        // is empty then we add current node to children vector
        if (cur != prev || siblings->empty())
        {
            Node tmp_node;
            // current node's index in str_[i] plus one
            tmp_node.depth = parent.depth + 1;
            // current node's code number
            tmp_node.code  = cur;
            // current node's start index in str_ array
            tmp_node.left  = i;

            // set previous node's end index in str_ array
            if (!siblings->empty())
            {
                (*siblings)[siblings->size()-1].right = i;
            }

            // add current node into child node vector
            siblings->push_back(tmp_node);
        }

        // set previous code to current node
        prev = cur;
    }
    // set last node's end index in str_ array
    if (! siblings->empty())
    {
        (*siblings)[siblings->size()-1].right = parent.right;
    }

    return siblings->size();
}

size_t DATrie::Insert(const std::vector<Node>& siblings)
{
    size_t begin = 0; // each code's jumping start position
    size_t nonzero_num = 0;   // used spaces between next_check_pos_ and pos
    bool bfirst = true;   // whether this free space is first useable space
    bool bfind = true;    // whether have find a reasonable position

    // get the jump start position
    size_t pos = _Max((size_t)siblings[0].code + 1, next_check_pos_) - 1;

    /* if current buffer's size too small, malloc more spaces */
    if (alloc_size_ <= pos) Resize(pos + 1);

    // find the begin position where we can store all codes
    while (1)
    {
        ++pos;

        if (array_[pos].check_)   // current pos is used
        {
            // record used spaces
            ++nonzero_num;
            continue;
        }
        else if (bfirst)
        {
            // first free space then we set next_check_pos_ to this free position
            next_check_pos_ = pos;
            bfirst = false;
        }

        begin = pos - siblings[0].code;
        // if current allocated space can not store all codes, then enlarge it
        if (alloc_size_ < (begin + siblings[siblings.size()-1].code + 1))
        {
            Resize((size_t)(alloc_size_ * _Max(1.05, 1.0 * str_size_ / progress_)));
        }

        if (used_[begin]) continue;

        // judge whether current begin position is reasonable
        bfind = true;
        for (size_t i = 1; i < siblings.size(); ++i)
        {
            // current begin position is not reasonable
            if (array_[begin + siblings[i].code].check_ != 0)
            {
                bfind = false;
                break;
            }
        }
        if (bfind) break;
    }

    // if the percentage of non-empty contents in check between the index
    // 'next_check_pos_' and 'check' is greater than some constant value
    // (e.g. 0.9), new 'next_check_pos_' index is written by 'check'.
    if ((pos - next_check_pos_ + 1) != 0 &&
        1.0 * nonzero_num/(pos - next_check_pos_ + 1) >= 0.95)
    {
        next_check_pos_ = pos;
    }
    // set the begin position to be used
    used_[begin] = 1;
    // find current array's maximum used index
    size_ = _Max(size_, begin + (size_t)siblings[siblings.size()-1].code + 1);

    // set each code's check num to indicate its jump position
    for (size_t i = 0; i < siblings.size(); ++i)
    {
        array_[begin + siblings[i].code].check_ = (unsigned)begin;
    }

    // recursivly add current nodes and their children nodes
    for (size_t i = 0; i < siblings.size(); ++i)
    {
        std::vector <Node> new_siblings;
        if (!Fetch(siblings[i], &new_siblings))
        {
            int* base_ref = &(array_[begin + siblings[i].code].base_);
            if (val_)
            {
                *base_ref = -(int)val_[siblings[i].left]-1;
            }
            else
            {
                *base_ref = -(int)siblings[i].left-1;
            }
            // current value is a negative value
            if (val_ && (int)(-val_[siblings[i].left]-1) >= 0)
            {
                fprintf(stderr, "%s\n", "key's property value is negative!");
                throw -4;
            }
            ++progress_;
        }
        else
        {
            // insert current node's children nodes and return their jump offset
            size_t start = Insert(new_siblings);
            array_[begin + siblings[i].code].base_ = (int)start;
        }
    }

    // return current children nodes' start position
    return begin;
}

DATrie::DATrie(void) :array_(0), used_(0), size_(0), alloc_size_(0), no_delete_(0)
{
}

DATrie::~DATrie(void)
{
    Clear();
}

void DATrie::Clear (void)
{
    if (!no_delete_) delete []array_;
    delete []used_;

    array_      = 0;
    used_       = 0;
    alloc_size_ = 0;
    size_       = 0;
    no_delete_  = 0;
}

bool DATrie::Build(size_t str_size, const char* const* str,
                   const size_t* len, const int* val)
{
    if (!str_size || !str) return false;

    str_ = str;
    len_ = len;
    str_size_ = str_size;
    val_ = val;
    progress_ = 0;
    Resize(1024 * 10);

    // set all code start position, this position is root position
    array_[0].base_ = 1;
    // initialize next_check_pos_
    next_check_pos_ = 0;

    // create the root node. root node doesn't need code number
    // we need root node to find all str_'s first code as its chilren
    // nodes, and these children nodes all starts from 1
    Node root_node;
    root_node.depth = 0;
    root_node.left  = 0;
    root_node.right = str_size;

    // used for storing root node's children nodes
    std::vector<Node> siblings;
    // get root node's children
    Fetch(root_node, &siblings);
    // recursively insert all str_ elements and their property into double array
    Insert(siblings);

    // set current double array' size to be maximum index plus sizeof(int)
    size_ += sizeof(int);

    // if size larger than allocated size malloc a new
    // size and copy data from old space to new space
    if (size_ > alloc_size_) Resize(size_);

    // release index space
    delete []used_;
    used_  = 0;

    return true;
    if (false)
    {
        delete []used_;
        used_  = 0;
        Clear ();
        return false;
    }
}


bool DATrie::Save(const char* file, const char* mode, size_t offset)
{
    if (!size_) return false;

    FILE *fp = fopen(file, mode);
    if (!fp) return false;
    if (size_ != fwrite(array_,  sizeof(Unit), size_, fp)) return false;
    fclose (fp);

    return true;
}

bool DATrie::Open(const char* file, const char* mode, size_t offset,
                  size_t _size)
{
    FILE *fp = fopen(file, mode);
    if (!fp) return false;
    if (fseek(fp, (long)offset, SEEK_SET) != 0) return false;

    // get current file's size
    if (!_size)
    {
        if (fseek(fp, 0L, SEEK_END) != 0) return false;
        _size = ftell (fp);
        if (fseek(fp, (long)offset, SEEK_SET) != 0) return false;
    }

    Clear();
    size_ = _size - offset;
    size_ /= sizeof(Unit);
    array_  = new Unit[size_];
    if (array_ == NULL)
    {
        fprintf(stderr, "%s\n", "Not enough memory to allocate!");
        return false;
    }
    if (size_ != fread ((Unit *)array_,  sizeof(Unit), size_, fp))
    {
        fprintf(stderr, "Read file: %s error!\n", file);
        return false;
    }
    fclose (fp);

    return true;
}

int DATrie::ExactMatch(const char* key, size_t key_len) const
{
    if (!key_len) key_len = strlen(key);
    if (array_ == NULL) return -2;
    register int  b = array_[0].base_;
    register unsigned p;

    for (register size_t i = 0; i < key_len; ++i)
    {
        p = b + (unsigned char)(key[i]) + 1;
        if (p >= size_) return -1;

        if ((unsigned)b == array_[p].check_)
        {
            b = array_[p].base_;
        }
        else
        {
            return -1;
        }
    }

    // test whether last checked code is string's end code
    // if this is true, then store string's property value
    p = b;
    int n = array_[p].base_;
    if ((unsigned)b == array_[p].check_ && n < 0)
        return -n-1;

    return -1;
}

int DATrie::LongestMatch(const char *key,
                               size_t &match_len, size_t key_len) const
{
    if (!key_len) key_len = strlen(key);
    if (array_ == NULL) return -2;

    register int b = array_[0].base_;
    register int n;
    register unsigned p;
    register int match_val = -1;
    match_len = 0;

    for (register size_t i = 0; i < key_len; ++i)
    {
        // test whether last checked code is string's end code
        // if this is true, then store string's property value
        p = b;
        n = array_[p].base_;
        if ((unsigned)b == array_[p].check_ && n < 0)
        {
            // current code is an string's end code
            match_val = -n-1;
            match_len = i;

        }

        // jump from current position to next position
        p = b + (unsigned char)(key[i]) + 1;
        // jump out of double array trie
        if (p >= size_) return match_val;

        // if double array have this arc then jump to next
        // position else return finded common prefix words' number
        if ((unsigned) b == array_[p].check_)
        {
            b = array_[p].base_;
        }
        else
        {
            return match_val;
        }
    }

    // test whether last checked code is string's end code
    // if this is true, then store string's property value
    p = b;
    n = array_[p].base_;
    if ((unsigned)b == array_[p].check_ && n < 0)
    {
        match_val = -n-1;
        match_len = key_len;
        //if (num < result_len) result[num] = -n-1;
        //++num;
    }

    return match_val;
}

size_t DATrie::CommonPrefixSearch(const char* key, int* result,
                                  size_t result_len, size_t key_len) const
{
    if (!key_len) key_len = strlen(key);
    if (array_ == NULL) return -2;

    register int b = array_[0].base_;
    register size_t num = 0;
    register int n;
    register unsigned p;

    for (register size_t i = 0; i < key_len; ++i)
    {
        // test whether last checked code is string's end code
        // if this is true, then store string's property value
        p = b;
        n = array_[p].base_;
        if ((unsigned)b == array_[p].check_ && n < 0)
        {
            // current code is an string's end code
            if (num < result_len) result[num] = -n-1;
            ++num;
        }

        // jump from current position to next position
        p = b + (unsigned char)(key[i]) + 1;
        // jump out of double array trie
        if (p >= size_) return num;

        // if double array have this arc then jump to next
        // position else return finded common prefix words' number
        if ((unsigned) b == array_[p].check_)
        {
            b = array_[p].base_;
        }
        else
        {
            return num;
        }
    }

    // test whether last checked code is string's end code
    // if this is true, then store string's property value
    p = b;
    n = array_[p].base_;
    if ((unsigned)b == array_[p].check_ && n < 0)
    {
        if (num < result_len) result[num] = -n-1;
        ++num;
    }

    return num;
}

