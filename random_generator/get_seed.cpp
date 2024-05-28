#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
#include <iterator>
#include <functional>

#include "TMVA/Tools.h"
#include "TRandom3.h"

template <typename container, typename T = typename container::value_type>
void print_vector(const container & vec){
    std::copy(vec.begin(), vec.end(), std::ostream_iterator<T>(std::cout, ", "));
    std::cout << "\n";
}

int main(){
    TMVA::RandomGenerator<TRandom3> rng = TMVA::RandomGenerator<TRandom3>(0);
    // UInt_t b = rng();
    // std::cout << b << "\n";


    // TMVA::RandomGenerator<TRandom3> fRng = TMVA::RandomGenerator<TRandom3>(b);

    // UInt_t seed_number = fRng.GetSeed();
    // std::cout << seed_number << "\n";

    // std::vector<int> vec(10);
    // std::iota(vec.begin(), vec.end(), 0);

    // std::shuffle(vec.begin(), vec.end(), fRng);

    // print_vector(vec);

    // std::shuffle(vec.begin(), vec.end(), fRng);

    // print_vector(vec);

    // std::sort(vec.begin(), vec.end());

    // fRng.seed(b);

    // std::shuffle(vec.begin(), vec.end(), fRng);

    // print_vector(vec);

    // std::shuffle(vec.begin(), vec.end(), fRng);

    // print_vector(vec);

    std::function<UInt_t(UInt_t)> lambda;
    lambda = [&](UInt_t a)->UInt_t{return a != 0? a: lambda(rng());};
    std::cout << lambda(rng()) << "\n";

    // std::function<void(int)> lambda;
    // lambda = [](int a){std::cout << a << "\n";};
    // lambda(3);
}
