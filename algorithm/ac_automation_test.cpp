#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <string>
#include <map>
#include "ac_automation.h"
// 参考http://my.oschina.net/coda/blog/184499
// http://www.cppblog.com/mythit/archive/2009/04/21/80633.html
// http://my.oschina.net/amince/blog/196426
//


int main(int argc, char **argv)
{
    std::map<char, char*> g_map;
    for (char i = 'a'; i < 'z' + 1; ++ i)
    {
        g_map[i] = new char;
        *(g_map[i]) = i;
    }
    //std::tr1::hash<char*> ptr_hash;
    ACAutomation<char> acm;
    std::string a = "abcd";
    std::string b = "abce";
    std::string d = "bcd";
    std::string needle = "abcd";
    std::vector<char *> pa, pb, pd, pneedle;
    for(size_t i = 0; i < a.size(); ++ i)
    {
        char c = a[i];
        pa.push_back(g_map[c]);
    }
    for(size_t i = 0; i < b.size(); ++ i)
    {
        char c = b[i];
        pb.push_back(g_map[c]);
    }
    for(size_t i = 0; i < d.size(); ++ i)
    {
        char c = d[i];
        pd.push_back(g_map[c]);
    }
    for(size_t i = 0; i < needle.size(); ++ i)
    {
        char c = needle[i];
        pneedle.push_back(g_map[c]);
    }
    acm.add(&pd);
    acm.add(&pa);
    acm.add(&pb);

    std::vector< const std::vector<char *> *> match_patterns;
    int32_t ret = acm.search(&match_patterns, &pneedle);
    std::cout << ret << std::endl;
    for (std::vector<const std::vector<char*>* >::const_iterator it = match_patterns.begin(); it != match_patterns.end(); ++ it)
    {
        const std::vector<char *> *pattern = *it;
        for (std::vector<char*>::const_iterator subit = pattern->begin(); subit != pattern->end(); ++ subit)
        {
            std::cout << **subit;
        }
        std::cout << std::endl;
    }
}

