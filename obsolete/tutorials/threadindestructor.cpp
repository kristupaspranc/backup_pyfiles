#include <iostream>
#include <thread>


class A {
	private:
		std::thread a;


	public:
		A(std::thread a_):
		a(std::move(a_))
		{
			std::cout<< "class initiated" << std::endl;
		}
		
		~A(){
			a.join();
			std::cout<< "class destructed" << std::endl;
		}
};


void foring(){
	for (int i = 1; i < 20; i++){
		std::cout << i << std::endl;		
			}
}


int main(){
	std::thread d(foring);
	
	A g(move(d));
	
	return 0;
}
	



