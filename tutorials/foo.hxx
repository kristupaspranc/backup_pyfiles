#include <iostream>

using namespace std;

struct fruit{
	int weigth;
	double price;
} apple, banana;

apple.weight = 2;
banana.weight = 1;
apple.price = 4;
banana.price = 3;

cout << apple;
