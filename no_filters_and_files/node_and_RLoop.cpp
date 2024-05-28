#include <iostream>
#include <vector>
#include <string>

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "ROOT/RDF/RLoopManager.hxx"
#include "ROOT/RDF/InterfaceUtils.hxx"
#include "ROOT/RDFHelpers.hxx"

void node_conversion(ROOT::RDF::RNode rdf){
    std::cout << "Conversion worked!" << "\n";
}

void check_it(ROOT::RDF::RInterface<ROOT::Detail::RDF::RLoopManager> f_rdf, std::size_t begin, std::size_t end){
    ROOT::RDF::RInterface<::ROOT::Detail::RDF::RNodeBase, void> noded_rdf = ROOT::RDF::AsRNode(f_rdf);

    ROOT::Internal::RDF::ChangeBeginAndEndEntries(noded_rdf, begin, end);

    std::size_t processed = noded_rdf.Count().GetValue();
    std::cout << "Processed events: " << processed << "\n";
}

void same_as_python(){
    ROOT::RDataFrame df = ROOT::RDataFrame("tree", "file");
    
    ROOT::RDF::RInterface<::ROOT::Detail::RDF::RNodeBase, void> noded_rdf = ROOT::RDF::AsRNode(df);

    ROOT::Internal::RDF::ChangeBeginAndEndEntries(noded_rdf, 10, 17);

    std::cout << noded_rdf.Count().GetValue() << "\n";
    noded_rdf.Display("a", 20)->Print();
}

int main(){
    // ROOT::RDataFrame rdf = ROOT::RDataFrame("myTree", "4000.root");
    // auto filtered = rdf.Filter("b1 < 2000");
    // ROOT::RDF::RInterface<ROOT::Detail::RDF::RLoopManager> f_rdf_no = rdf.template Cache<int, double>(std::vector<std::string>{"b1","b2"});

    // ROOT::RDF::RInterface<::ROOT::Detail::RDF::RNodeBase, void> f_rdf = ROOT::RDF::AsRNode(f_rdf_no);

    // std::size_t processed = f_rdf.Count().GetValue();

    // std::cout << "Processed events: " << processed << "\n";

    // for (int i = 0; i < 4; i++){
    //     check_it(f_rdf, i * 500, (i+1) * 500);
    // }

    // ROOT::Internal::RDF::ChangeBeginAndEndEntries(f_rdf, 0, 500);

    // processed = f_rdf.Count().GetValue();
    // std::cout << "Processed events: " << processed << "\n";

    // ROOT::Internal::RDF::ChangeBeginAndEndEntries(f_rdf, 0, 87);

    // processed = f_rdf.Count().GetValue();
    // std::cout << "Processed events: " << processed << "\n";
    
    // ROOT::Internal::RDF::ChangeBeginAndEndEntries(f_rdf, 500, 569);

    // processed = f_rdf.Count().GetValue();
    // std::cout << "Processed events: " << processed << "\n";
    
    // size_t i = 0;

    // f_rdf.Foreach([&](int first, double second){std::cout << "i: " << i << " first: " << first << "second: " << second << "\n"; i++;}, std::vector<std::string>{"b1","b2"});

    // ROOT::Internal::RDF::ChangeBeginAndEndEntries(f_rdf, 500, 569);

    // f_rdf.Foreach([&](int first, double second){std::cout << "i: " << i << " first: " << first << "second: " << second << "\n"; i++;}, std::vector<std::string>{"b1","b2"});

    // std::cout << "i in the end: " << i << "\n";

    // same_as_python();

    std::size_t fNumChunks;
    std::size_t fValidationRemainder;
    std::size_t fTrainRemainder;
    std::size_t fNumTrainBatches;
    std::size_t fNumValidationBatches;

    std::size_t fBatchSize = 400;
    std::size_t fChunkSize = 2000;
    std::size_t fNumEntries = 4015;
    float fValidationSplit = 0.3;

    fNumChunks = fNumEntries % fChunkSize != 0? fNumEntries / fChunkSize + 1: fNumEntries / fChunkSize;
    fValidationRemainder = (fNumEntries / fChunkSize) * ceil(fChunkSize * fValidationSplit)
        + ceil((fNumEntries % fChunkSize) * fValidationSplit);
    fTrainRemainder = fNumEntries - fValidationRemainder;
    fNumTrainBatches = fTrainRemainder / fBatchSize;
    fNumValidationBatches = fValidationRemainder / fBatchSize;
    fValidationRemainder %= fBatchSize;
    fTrainRemainder %= fBatchSize;

    std::cout << "fNumChunks: " << fNumChunks << "\n";
    std::cout << "fValidationRemainder: " << fValidationRemainder << "\n";
    std::cout << "fTrainRemainder: " << fTrainRemainder << "\n";
    std::cout << "fNumTrainBatches: " << fNumTrainBatches << "\n";
    std::cout << "fNumValidationBatches: " << fNumValidationBatches << "\n";

    return 0;
}