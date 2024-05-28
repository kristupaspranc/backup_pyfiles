#include "TTree.h"
#include "ROOT/RDataFrame.hxx"
#include <iostream>
#include <typeinfo>

int main(){
    TTree tree("tree", "title");

    // std::cout << ::std::typeid(tree).name() << "\n";

    ROOT::RDataFrame df(tree);

    std::cout << df.Describe() << "\n";

    return 0;
}