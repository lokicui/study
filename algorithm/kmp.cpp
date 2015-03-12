#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <iostream>

int * get_nextval(const char *T)
{
    // 求模式串T的next函数值并存入数组 next。
    //参考：http://www.cppblog.com/oosky/archive/2006/07/06/9486.html
    /*
     *（1）next[0]= -1  意义：任何串的第一个字符的模式值规定为-1。
     *（2）next[j]= -1   意义：模式串T中下标为j的字符，如果与首字符
     *           相同，且j的前面的1—k个字符与开头的1—k
     *           个字符不等（或者相等但T[k]==T[j]）（1≤k<j）。
     *           如：T=”abCabCad” 则 next[6]=-1，因T[3]=T[6]
     *
     *  next[j] = -1 其实就是说T[k] == T[j], 若haystack[i]与T[j]失配了,那跟T[k]也必然失配,所有i++; j=0
     *
     *
     *（3）next[j]=k    意义：模式串T中下标为j的字符，如果j的前面k个
     *           字符与开头的k个字符相等，且T[j] != T[k] （1≤k<j）。
     *           即T[0]T[1]T[2]。。。T[k-1]==
     *           T[j-k]T[j-k+1]T[j-k+2]…T[j-1]
     *           且T[j] != T[k].（1≤k<j）;
     *(4) next[j]=0   意义：除（1）（2）（3）的其他情况。next[j]=0啥信息没有,i++ && j++
     */
    int *next = new int[strlen(T)];
    int j = 0, k = -1;
    next[0] = -1;
    while ( T[j] != '\0' )
    {
        if (k == -1 || T[j] == T[k])
        {
            ++j;
            ++k;
            if (T[j] != T[k]) // k == -1进来的
                next[j] = 0; // next[j] = k;
            else
                // T[j] == T[k]时, 因为不能出现p[j] = p[next[j]]，所以当出现时需要继续递归，k = next[k] = next[next[k]]
                //  原因在这个blog中说的比较明白http://blog.csdn.net/v_july_v/article/details/7041827
                next[j] = next[k];  // next[j] = next[ next[j]=k ];
        }// if
        else
            k = next[k];
    }

    // 4 debug
    for(int i = 0; i < j; i++)
    {
        std::cout << i << ":" << next[i] << std::endl;
    }
    return next;
}

char *kmp_strstr(const char *haystack, const char *needle)
{
    // 通俗易懂版！！！
    int find_idx(0);
    int *N = get_nextval(needle);
    int i(0), j(0);
    while (haystack[i] != '\0' && needle[j] != '\0')
    {
        if (haystack[i] == needle[j])
        {
            i++;
            j++;
        }
        else
        {
            if (N[j] == 0)
            {
                // needle[0:j] 所有子串的最长公共子串长度为0, needle[j] != needle[0], 模式串必须从头再来,一夜回到解放前!
                // 若needle[0:len(needle)] 所有子串的最长公共子串长度为0, 那KMP毛用都没有
                find_idx = i; // 等价于 find_idx += j(前一次匹配了多长); 等价于 find_idx += j - N[j];
                j = 0;  //  j = N[j]
            }
            else if (N[j] == -1)
            {
                // N[j] == -1 代表 needle[j] 和 needle[0]是一样的,
                // 现在needle[j] != haystack[i],
                // so, haystack可以往前走一步, 模式串要从头再开始匹配
                ++i;
                find_idx = i; // 等价于 find_idx += j+1; 等价于 find_idx += j - N[j]; 你妹的，原来next定义一个-1就是因为这
                j = 0;
            }
            else
            {
                find_idx = i - N[j]; //模式串的前N[j]个字符串和haystack的前N[j]个字符串是一样的
                // 等价于 find_idx += j - N[j];
                // 模式串位置
                j = N[j];
            }
        }
    }
    delete []N;
    if (needle[j] == '\0')
        return const_cast<char *>(&haystack[find_idx]); // 其实 find_idx = j - strlen(needle), 那么麻烦有毛用
    else
        return NULL;
}


int main(int argc, char **argv)
{
    std::cout << argv[1] << ":" << argv[2] << std::endl;
    char *find = kmp_strstr(argv[1], argv[2]);
    assert(strstr(argv[1], argv[2]) == find);
    std::cout << find << std::endl;
}
