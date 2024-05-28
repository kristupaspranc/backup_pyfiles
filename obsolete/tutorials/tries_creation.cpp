#include <iostream>
#include <map>
#include <algorithm>
#include <optional>
#include <functional>
#include <string>
#include <iterator>

template <typename T>
class trie{
    std::map<T,trie> tries;

public:
    template <typename It>
    void insert(It it, It end_it){
        if (it == end_it){ return; };
        tries[*it].insert(next(it), end_it);
    }

    template <typename C>
    void insert(const C & container){
        insert(std::begin(container), std::end(container));
    }

    void insert(std::initializer_list<T> && il){
        insert(std::begin(il), std::end(il));
    }

    void print(std::vector<T> &&v) const{
        if (tries.empty()){
            std::copy(v.begin(), v.end(), std::ostream_iterator<T>(std::cout, " "));
            std::cout << "\n"; 
        }
        for (const auto & p:tries){
            v.push_back(p.first);
            p.second.print(std::move(v));
            v.pop_back();
        }
    }

    void print() const {
        std::vector<T> v;
        print(std::move(v));
    }

    template <typename It>
    std::optional <std::reference_wrapper<const trie>>
    subtrie(It it, It it_end){
        if (it = it_end) { return ref(*this); }
        auto found (tries.find(*it));
        if (found == it_end){ return {}; }
        return found->second.subtrie(next(it), it_end);
    }

    template<typename C>
    auto subtrie(const C &c){
        return subtrie(begin(c), end(c));
    }
};

int main(){
    trie<std::string> t;

    t.insert({"hi", "how", "are", "you"});
    t.insert({"hi", "i", "am", "great", "thanks"});
    t.insert({"what", "are", "you", "doing"});
    t.insert({"i", "am", "watching", "a", "movie"});

    std::cout << "recorded sentences:\n";
    t.print();

    std::cout << "\n Possible suggestions after \"hi\":\n";
    if (auto st(t.subtrie(std::initializer_list<std::string>{"hi"})); st){
        st->get().print();
    }
}
