#include <iostream>
#include <vector>
#include <string>

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDF/RInterface.hxx"

class Foo{
    std::size_t a = 0;
    
public:
    Foo(){
        std::cout << "I am reinstantiated!\n";
    }
    // Foo(const Foo &) { std::cout << "Copy\n"; }
    void operator()(int b){
        std::cout << "Class native variable: " << a++ << "\n";
        std::cout << "Given parameter: " << b << "\n";
    }
};

int main(){
    // int c{0};
    // auto df = ROOT::RDataFrame(10).Define("b1", [&]()->int{ return c++; });

    // df.Snapshot("myTree", "10.root");

    // int i{0};
    // auto lambda = [&](){std::cout << "Row: " << i++ << "\n";};
    // auto lambda = [](int a){std::cout << a << "\n";};
    // df.Foreach(lambda, std::vector<std::string>{"b1"});

    ROOT::RDataFrame df = ROOT::RDataFrame("myTree", "10.root");

    Foo other_lambda; 

    df.Foreach(other_lambda, std::vector<std::string>{"b1"});

    ROOT::Internal::RDF::ChangeBeginAndEndEntries(df, 4, 6);

    df.Foreach(other_lambda, std::vector<std::string>{"b1"});
}
