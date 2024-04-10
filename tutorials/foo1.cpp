#include <iostream>


int main() {
	int a = 10;
	int* b = &a;
	
	std::cout << &a << std::endl;
	std::cout << b << std::endl;
	std::cout << *b << std::endl;	    
}
