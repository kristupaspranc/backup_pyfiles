#include <iostream>


template <typename WhatKind>
void multiples(WhatKind &sum, WhatKind x, int n){
	sum++;
	
	for (int i = 1; i <= n; i++) {
		sum += i*x;
		}
}


int main(){
	int isum = 0;
	int ia = 1;
	double sum = 0;
	double a = 1.5;
	
	multiples<int>(isum, ia, 5);
	multiples<double>(sum, a, 4);
	
	std::cout << "Integer sum is: " << isum << std::endl;
	std::cout << "Double sum is: " << sum << std::endl;
}
