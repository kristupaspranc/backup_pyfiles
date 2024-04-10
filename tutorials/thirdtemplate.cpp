#include <iostream>
#include <string>

template <typename T1, typename T2>
T1 init (T1 num1, T1 num2, T2& start){
	start = 1;
	
	return num1 + num2;
}

int main(){
	double a = 2;
	std::cout << "A: " << a << std::endl;
	
	int b = init<int, double>(1, 2, a);
	std::cout << "A: " << a << " ir B: " << b << std::endl;
	
	
	std::string c = "Labas";
	
	double d = init<double, std::string>(1.5, 1.2, c);
	std::cout << "C: " << c << " ir D: " << d << std::endl;
}
