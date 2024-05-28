#include <iostream>
#include <vector>
#include <memory>
#include <numeric>

#include "TMVA/RTensor.hxx"

class B{
    std::vector<std::shared_ptr<TMVA::Experimental::RTensor<float>>> & fVec;

public:
    B(std::vector<std::shared_ptr<TMVA::Experimental::RTensor<float>>> & vec):
        fVec(vec)
    {
    }

    void smth(){
        std::shared_ptr<TMVA::Experimental::RTensor<float>> batch;

        for (std::size_t i = 0; i < 3; i++){
            fVec.emplace_back(std::make_shared<TMVA::Experimental::RTensor<float>>(std::vector<std::size_t>{4, 2}));
        }

        for (std::size_t i = 1; i < 4; i++){
            for (std::size_t b = 0; b < 8; b += 2){
                fVec[i-1]->GetData()[b] = b * i;
                fVec[i-1]->GetData()[b+1] = b * i + 10;
            }

            for (float a:*fVec[i-1]){
                std::cout << a << ", ";
            }

            std::cout << "\n";
        }

        batch = fVec[0];
        std::cout << "Batch size: " << fVec[0]->GetSize() << "\n";
        std::cout << "Batch size: " << batch->GetSize() << "\n";
        batch->GetData()[1] = 68;

        for (std::size_t i = 1; i < 4; i++){
            for (float a:*fVec[i-1]){
                std::cout << a << ", ";
            }

            std::cout << "\n";
        }
    }
};

class A{
    std::vector<std::shared_ptr<TMVA::Experimental::RTensor<float>>> vec;

public:
    A(){
        B b(vec);
        b.smth();
    }
};

int main(){
    A a;
}