#include <iostream>
#include <vector>
#include <numeric>
#include <iterator>

#include "TMVA/RTensor.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "/home/kristupas/root/tmva/tmva/inc/TMVA/RBatchGenerator.hxx"
#include "ROOT/RLogger.hxx"
#include "ROOT/RDFHelpers.hxx"

namespace TMVA {
namespace Experimental {
namespace Internal {

// // RChunkLoader class used to load content of a RDataFrame onto a RTensor.
// template <typename First, typename... Rest>
// class RChunkLoaderFunctor {

// private:
//    std::size_t fOffset = 0;
//    std::size_t fVecSizeIdx = 0;
//    std::vector<std::size_t> fMaxVecSizes;

//    float fVecPadding;

//    TMVA::Experimental::RTensor<float> &fChunkTensor;

//    /// \brief Load the final given value into fChunkTensor
//    /// \tparam First_T
//    /// \param first
//    template <typename First_T>
//    void AssignToTensor(First_T first)
//    {
//       fChunkTensor.GetData()[fOffset++] = first;
//    }

//    /// \brief Load the final given value into fChunkTensor
//    /// \tparam VecType
//    /// \param first
//    template <typename VecType>
//    void AssignToTensor(const ROOT::RVec<VecType> &first)
//    {
//       AssignVector(first);
//    }

//    /// \brief Recursively loop through the given values, and load them onto the fChunkTensor
//    /// \tparam First_T
//    /// \tparam ...Rest_T
//    /// \param first
//    /// \param ...rest
//    template <typename First_T, typename... Rest_T>
//    void AssignToTensor(First_T first, Rest_T... rest)
//    {
//       fChunkTensor.GetData()[fOffset++] = first;

//       AssignToTensor(std::forward<Rest_T>(rest)...);
//    }

//    /// \brief Recursively loop through the given values, and load them onto the fChunkTensor
//    /// \tparam VecType
//    /// \tparam ...Rest_T
//    /// \param first
//    /// \param ...rest
//    template <typename VecType, typename... Rest_T>
//    void AssignToTensor(const ROOT::RVec<VecType> &first, Rest_T... rest)
//    {
//       AssignVector(first);

//       AssignToTensor(std::forward<Rest_T>(rest)...);
//    }

//    /// \brief Loop through the values of a given vector and load them into the RTensor
//    /// Note: the given vec_size does not have to be the same size as the given vector
//    ///       If the size is bigger than the given vector, zeros are used as padding.
//    ///       If the size is smaller, the remaining values are ignored.
//    /// \tparam VecType
//    /// \param vec
//    template <typename VecType>
//    void AssignVector(const ROOT::RVec<VecType> &vec)
//    {
//       std::size_t max_vec_size = fMaxVecSizes[fVecSizeIdx++];
//       std::size_t vec_size = vec.size();

//       for (std::size_t i = 0; i < max_vec_size; i++) {
//          if (i < vec_size) {
//             fChunkTensor.GetData()[fOffset++] = vec[i];
//          } else {
//             fChunkTensor.GetData()[fOffset++] = fVecPadding;
//          }
//       }
//    }

// public:
//    RChunkLoaderFunctor(TMVA::Experimental::RTensor<float> &chunkTensor,
//                        const std::vector<std::size_t> &maxVecSizes = std::vector<std::size_t>(),
//                        const float vecPadding = 0.0)
//       : fChunkTensor(chunkTensor), fMaxVecSizes(maxVecSizes), fVecPadding(vecPadding)
//    {
//    }

//    /// \brief Loop through all columns of an event and put their values into an RTensor
//    /// \param first
//    /// \param ...rest
//    void operator()(First first, Rest... rest)
//    {
//       fVecSizeIdx = 0;
//       AssignToTensor(std::forward<First>(first), std::forward<Rest>(rest)...);
//    }
// };

// void createIdxs(std::size_t processedEvents, std::vector<std::vector<std::size_t>> fTrainingIdxs, std::vector<std::vector<std::size_t>> fValidationIdxs){
//     // Create a vector of number 1..processedEvents
//     std::vector<std::size_t> row_order = std::vector<std::size_t>(processedEvents);
//     std::iota(row_order.begin(), row_order.end(), 0);

//     // calculate the number of events used for validation
//     std::size_t num_validation = ceil(processedEvents * 0.3);

//     // Devide the vector into training and validation
//     std::vector<std::size_t> valid_idx({row_order.begin(), row_order.begin() + num_validation});
//     std::vector<std::size_t> train_idx({row_order.begin() + num_validation, row_order.end()});

//     fTrainingIdxs.push_back(train_idx);
//     fValidationIdxs.push_back(valid_idx);
// }

void do_things(){
    std::unique_ptr<TMVA::Experimental::RTensor<float>> chunkTensor =
         std::make_unique<TMVA::Experimental::RTensor<float>>(std::vector<std::size_t>{2000, 1});

    TMVA::Experimental::Internal::RChunkLoaderFunctor<double&> func(*chunkTensor);

    ROOT::RDataFrame df(100);
    auto df_with_define = df.Define("b1", "(double) rdfentry_");

    auto x_ranged = df_with_define.Range(2000);
    auto myCount = x_ranged.Count();

    std::vector<std::string> names{"b1"};
    // load data
    x_ranged.Foreach(func, names);

    // get loading info
    std::size_t processed_events = myCount.GetValue();
    std::size_t passed_events = myCount.GetValue();
    
    std::cout << processed_events << "\n";
    std::cout << passed_events << "\n";

    std::vector<std::vector<std::size_t>> fTrainingIdxs;
    std::vector<std::vector<std::size_t>> fValidationIdxs;

    // Create a vector of number 1..processedEvents
    std::vector<std::size_t> row_order = std::vector<std::size_t>(processed_events);
    std::iota(row_order.begin(), row_order.end(), 0);

    // calculate the number of events used for validation
    std::size_t num_validation = ceil(processed_events * 0.3);

    // Devide the vector into training and validation
    std::vector<std::size_t> valid_idx({row_order.begin(), row_order.begin() + num_validation});
    std::vector<std::size_t> train_idx({row_order.begin() + num_validation, row_order.end()});

    fTrainingIdxs.push_back(train_idx);
    fValidationIdxs.push_back(valid_idx);

    std::cout << fTrainingIdxs[0].size() << "\n";
    std::cout << fValidationIdxs[0].size() << "\n";

    // for (auto & idx:fTrainingIdxs[0]){
    //     std::cout << idx << "\n";
    // }
    // for (auto & idx:fValidationIdxs[0]){
    //     std::cout << idx << "\n";
    // }
}
}
}
}

int main(){
    // ROOT::RDataFrame df(100);
    // ROOT::RDF::RNode df_with_define = df.Define("b1", "(double) rdfentry_");
    ROOT::RDataFrame dfo("myTree", "40int.root");
    auto dfof = dfo.Filter("b1 < 50");
    ROOT::RDF::RNode df = ROOT::RDF::AsRNode(dfof);
    std::vector<std::string> names{"b1","b2"};

    TMVA::Experimental::Internal::RBatchGenerator<int&, int&> gen{
        df, 20, 4, names, {}, 0.0, 0.3, 0, 0, false, true
    };

    gen.Activate();
    TMVA::Experimental::RTensor<float> a = gen.GetTrainBatch();
    TMVA::Experimental::RTensor<float> b = gen.GetValidationBatch();

    std::vector<double> arg;
    std::vector<double> val;

    // for (int i = 0; i < 12; i++){
    //     std::copy(a.GetData() + i, a.GetData() + i + 1, std::back_inserter(arg));
    // }

    // for (int i = 0; i < 4; i++){
    //     std::copy(b.GetData() + i, b.GetData() + i + 1, std::back_inserter(val));
    // }

    // for (double & a:arg){
    //     std::cout << a << ", ";
    // }

    // std::cout << "\n";

    // for (double & a:val){
    //     std::cout << a << ", ";
    // }

    // std::cout << "\n";

    // for (auto& a : arg){
    //     std::cout << a << ", ";
    // }

    // std::cout << "\n";

    // for (auto& a : arg){
    //     std::cout << a << ", ";
    // }

    // std::cout << "\n";

    // ROOT::RDataFrame df(100);
    // ROOT::RDF::RNode df_with_define = df.Define("b1", "(double) rdfentry_");

    // // auto filtered = df_with_define.Filter("b1 < 50");
    // auto myReport = df_with_define.Report();
    // auto fNumEntries = df_with_define.Count().GetValue();

    // std::cout << fNumEntries << "\n";

    // myReport->Print();

    // std::size_t processed_events = myReport.begin()->GetAll();
    // std::size_t passed_events = (myReport.end() - 1)->GetPass();

    // std::cout << processed_events << "\n";
    // std::cout << passed_events << "\n";

    return 0;
}