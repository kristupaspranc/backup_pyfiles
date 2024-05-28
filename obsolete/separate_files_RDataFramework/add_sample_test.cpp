#ifndef TMVA_CHUNKLOADER
#define TMVA_CHUNKLOADER

#include <iostream>
#include <vector>

#include "TMVA/RTensor.hxx"
#include "TMVA/Tools.h"
#include "TRandom3.h"
#include "ROOT/RLogger.hxx"
#include "ROOT/RDataFrame.hxx"

namespace TMVA{
namespace Experimental{
namespace Internal{

// RChunkLoader class used to load content of a RDataFrame onto a RTensor.
template <typename First, typename... Rest>
class RChunkLoaderFunctor {

private:
   std::size_t fOffset = 0;
   std::size_t fVecSizeIdx = 0;
   std::vector<std::size_t> fMaxVecSizes;

   float fVecPadding;

   TMVA::Experimental::RTensor<float> &fChunkTensor;

   /// \brief Load the final given value into fChunkTensor
   /// \tparam First_T
   /// \param first
   template <typename First_T>
   void AssignToTensor(First_T first)
   {
      fChunkTensor.GetData()[fOffset++] = first;
   }

   /// \brief Load the final given value into fChunkTensor
   /// \tparam VecType
   /// \param first
   template <typename VecType>
   void AssignToTensor(const ROOT::RVec<VecType> &first)
   {
      AssignVector(first);
   }

   /// \brief Recursively loop through the given values, and load them onto the fChunkTensor
   /// \tparam First_T
   /// \tparam ...Rest_T
   /// \param first
   /// \param ...rest
   template <typename First_T, typename... Rest_T>
   void AssignToTensor(First_T first, Rest_T... rest)
   {
      fChunkTensor.GetData()[fOffset++] = first;

      AssignToTensor(std::forward<Rest_T>(rest)...);
   }

   /// \brief Recursively loop through the given values, and load them onto the fChunkTensor
   /// \tparam VecType
   /// \tparam ...Rest_T
   /// \param first
   /// \param ...rest
   template <typename VecType, typename... Rest_T>
   void AssignToTensor(const ROOT::RVec<VecType> &first, Rest_T... rest)
   {
      AssignVector(first);

      AssignToTensor(std::forward<Rest_T>(rest)...);
   }

   /// \brief Loop through the values of a given vector and load them into the RTensor
   /// Note: the given vec_size does not have to be the same size as the given vector
   ///       If the size is bigger than the given vector, zeros are used as padding.
   ///       If the size is smaller, the remaining values are ignored.
   /// \tparam VecType
   /// \param vec
   template <typename VecType>
   void AssignVector(const ROOT::RVec<VecType> &vec)
   {
      std::size_t max_vec_size = fMaxVecSizes[fVecSizeIdx++];
      std::size_t vec_size = vec.size();

      for (std::size_t i = 0; i < max_vec_size; i++) {
         if (i < vec_size) {
            fChunkTensor.GetData()[fOffset++] = vec[i];
         } else {
            fChunkTensor.GetData()[fOffset++] = fVecPadding;
         }
      }
   }

public:
   RChunkLoaderFunctor(TMVA::Experimental::RTensor<float> &chunkTensor,
                       const std::vector<std::size_t> &maxVecSizes = std::vector<std::size_t>(),
                       const float vecPadding = 0.0)
      : fChunkTensor(chunkTensor), fMaxVecSizes(maxVecSizes), fVecPadding(vecPadding)
   {
   }

   /// \brief Loop through all columns of an event and put their values into an RTensor
   /// \param first
   /// \param ...rest
   void operator()(First first, Rest... rest)
   {
      fVecSizeIdx = 0;
      AssignToTensor(std::forward<First>(first), std::forward<Rest>(rest)...);
   }
};


template <typename... Args>
class RChunkLoader{
private:
    std::string fTreename;
    std::vector<std::string> fFilename;
    std::vector<std::string> fCols;
    std::size_t fChunkSize;

    std::vector<std::size_t> fvecSizes;
    std::size_t fvecPadding;

public:
    RChunkLoader(const std::string &treeName, const std::vector<std::string> &fileName, const std::vector<std::string> &cols, const std::size_t &chunkSize,
                 const std::vector<std::size_t> &vecSizes = {}, const float vecPadding = 0.0)
    :   fTreename(treeName),
        fFilename(fileName),
        fCols(cols),
        fChunkSize(chunkSize),
        fvecSizes(vecSizes),
        fvecPadding(vecPadding)
    {
    }

    void LoadChunk(TMVA::Experimental::RTensor<float> &chunkTensor, const std::size_t currentRow = 0)
    {
        RChunkLoaderFunctor<Args...> func(chunkTensor, fvecSizes, fvecPadding);

        long long start_l = currentRow;
        ROOT::RDF::Experimental::RDatasetSpec x_spec =
            ROOT::RDF::Experimental::RDatasetSpec()
                .AddSample({"", fTreename, fFilename})
                .WithGlobalRange({start_l, std::numeric_limits<Long64_t>::max()});

        ROOT::RDataFrame x_rdf(x_spec);

        auto x_ranged = x_rdf.Range(fChunkSize);
        x_ranged.Foreach(func, fCols);
    }
};


template <typename... Args>
void testing_assignment(){
   std::unique_ptr<TMVA::Experimental::RTensor<float>> fChunkTensor;
   std::unique_ptr<TMVA::Experimental::Internal::RChunkLoader<Args...>> fChunkLoader;

   std::vector<std::string> cols = {"a1","a2","a3","a4"};
   long unsigned fChunkSize = 400;
   long unsigned fNumColumns = 4;
   std::string treeName = "myTree";
   std::string fileName = "400_rows.root";
   std::vector<std::string> fileNames;
   fileNames.push_back("400_rows.root");
   fileNames.push_back("4000_rows.root");

   std::cout << fileNames[0] << std::endl;
   std::cout << fileNames[1] << std::endl;

   // Create tensor to load the chunk into
   fChunkTensor = std::make_unique<TMVA::Experimental::RTensor<float>>(std::vector<std::size_t>{fChunkSize, fNumColumns});

   fChunkLoader = std::make_unique<TMVA::Experimental::Internal::RChunkLoader<Args...>>(treeName, fileNames, cols, fChunkSize);

   fChunkLoader->LoadChunk(*fChunkTensor);

   // auto entries = 
}

}//namespace Internal
}//namespace Experimental
}//namespace TMVA





int main(){

TMVA::Experimental::Internal::testing_assignment<double&,double&,double&,double&>();
std::cout << "you" << std::endl;

return 0;
}

#endif // TMVA_CHUNKLOADER