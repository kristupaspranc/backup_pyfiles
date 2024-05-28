#include <iostream>
#include <vector>
#include <string>
#include "TChain.h"
#include "ROOT/RDF/RLoopManager.hxx"
#include "ROOT/RDataFrame.hxx"


int main(){
    ROOT::RDataFrame df = ROOT::RDataFrame("myTree","10.root");

    TChain chain;
    chain.Add("10.root");
    std::vector<std::string> defaultColumns{"b1"};
    // auto lm = std::make_shared<ROOT::Detail::RDF::RLoopManager>(std::move(chain), defaultColumns);
}