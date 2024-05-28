#include <iostream>
#include <string>

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDF/RInterface.hxx"

class functor{
private:
    std::size_t fNumber = 0;

public:
    void operator()(short a, unsigned long long b){if (fNumber > 500){std::cout << a << "\n";} fNumber++; }
};

int main(){
    ROOT::RDataFrame df("myTree", "4000.root");
    ROOT::Internal::RDF::ChangeBeginAndEndEntries(df, 100, 200);
    auto filtered = df.Filter("b1%2==0","Filters");
    // auto filtered_twice = df.Filter("b1%3==0","AnotherOne");
    // auto reported = filtered_twice.Report();

    // filtered.Foreach([](Short_t a, unsigned long long b){}, std::vector<std::string>{"b1", "b2"});

    // std::cout << filtered.Count().GetValue() << "\n";
    // reported->Print();


    std::size_t processed_events = reported.begin()->GetAll();
    std::size_t passed_events = (reported.end() - 1)->GetPass();

    std::cout << processed_events << "\n";
    std::cout << passed_events << "\n";

    // std::vector<std::string> names = df.GetFilterNames();

    // for(std::string & a: names){
    //     std::cout << a << "\n";
    // }
    // functor f;
    // df.Foreach(f, std::vector<std::string>{"b1","b2"});

    std::cout << df.GetFilterNames().empty() << "\n";
}
