#include <iostream>
#include <thread>


void foring(){
	for (int i=0; i <= 20; i++){
		std::cout << i << std::endl;
	}
}


int main(){
	std::thread a(foring);
	
	
	std::cout << "ending" << std::endl;
	
	a.join();
	
	return 0;
}
