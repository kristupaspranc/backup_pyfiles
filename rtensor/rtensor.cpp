#include <vector>
#include <string>
#include <algorithm>
#include <iterator>
#include <iostream>

#include "TMVA/RTensor.hxx"
#include "ROOT/RDataFrame.hxx"

int main(){
    auto tensor = TMVA::Experimental::RTensor<float>(std::vector<std::size_t>{3, 3}, TMVA::Experimental::MemoryLayout::ColumnMajor);

    auto df = ROOT::RDataFrame(10).Define("b1", "(int) rdfentry_");

    std::size_t i = 0;

    df.Foreach([&](int a){ tensor.GetData()[i++] = a; }, std::vector<std::string>{"b1"});

    for (std::size_t i = 0; i < 9; i++){
        std::copy(tensor.GetData() + i, tensor.GetData() + i + 1, std::ostream_iterator<int>(std::cout, ", "));
    }
}